"""Blind Vow - interpolate key poses, solve IK per frame, and run quality checks."""

import math
from mathutils import Matrix, Quaternion, Vector

from bv_rig import (
    I3, JOINTS, PARTS, fk, solve_pose, tip_and_pommel,
)

STOP_LABELS = ("inout", "out", "stop")


def _as_list(v):
    if isinstance(v, Quaternion):
        return [v.w, v.x, v.y, v.z]
    return list(v)


def _hermite(p0, p1, m0, m1, s, h):
    s2, s3 = s * s, s * s * s
    h00 = 2 * s3 - 3 * s2 + 1
    h10 = s3 - 2 * s2 + s
    h01 = -2 * s3 + 3 * s2
    h11 = s3 - s2
    return [h00 * a + h10 * h * c + h01 * b + h11 * h * d for a, b, c, d in zip(p0, p1, m0, m1)]


def _channel_series(keys, name):
    vals = []
    prev = None
    for _, pose, _ in keys:
        v = _as_list(pose[name])
        if isinstance(pose[name], Quaternion) and prev is not None:
            if sum(a * b for a, b in zip(v, prev)) < 0:
                v = [-a for a in v]
        vals.append(v)
        prev = v
    return vals


def sample_keys(keys, length):
    """keys: [(frame, pose, label)] -> list of poses for frames 0..length (inclusive)."""
    times = [k[0] for k in keys]
    stops = [k[2] in STOP_LABELS for k in keys]
    stops[0] = stops[-1] = True
    names = list(keys[0][1].keys())
    series = {n: _channel_series(keys, n) for n in names}
    tangents = {}
    for n in names:
        vals = series[n]
        tl = []
        for i in range(len(keys)):
            if stops[i] or i == 0 or i == len(keys) - 1:
                tl.append([0.0] * len(vals[i]))
            else:
                dt = times[i + 1] - times[i - 1]
                tl.append([(b - a) / dt for a, b in zip(vals[i - 1], vals[i + 1])])
        tangents[n] = tl
    out = []
    for f in range(length + 1):
        i = 0
        while i < len(times) - 2 and f > times[i + 1]:
            i += 1
        t0, t1 = times[i], times[i + 1]
        h = max(t1 - t0, 1e-6)
        s = min(max((f - t0) / h, 0.0), 1.0)
        pose = {}
        for n in names:
            v = _hermite(series[n][i], series[n][i + 1], tangents[n][i], tangents[n][i + 1], s, h)
            ref = keys[0][1][n]
            if isinstance(ref, Quaternion):
                q = Quaternion(v)
                q.normalize()
                pose[n] = q
            else:
                vec = Vector(v)
                if n.endswith("_pole"):
                    vec.normalize()
                pose[n] = vec
        out.append(pose)
    return out


def sample_fk_keys(fk_keys, length):
    """Looping FK clip (idle): smooth (cosine) blend between joint Transforms."""
    out = []
    for f in range(length + 1):
        i = 0
        while i < len(fk_keys) - 2 and f > fk_keys[i + 1][0]:
            i += 1
        (t0, A), (t1, B) = fk_keys[i], fk_keys[i + 1]
        s = (f - t0) / (t1 - t0)
        s = 0.5 - 0.5 * math.cos(math.pi * s)
        T = {}
        for j in A:
            qa, qb = A[j][0].to_quaternion(), B[j][0].to_quaternion()
            T[j] = (qa.slerp(qb, s).to_matrix(), A[j][1].lerp(B[j][1], s))
        out.append(T)
    return out


def bake_clip(clip):
    """-> list of per-frame Transform dicts, list of per-frame diagnostics."""
    if "fk_keys" in clip:
        frames = sample_fk_keys(clip["fk_keys"], clip["length"])
        return frames, [{} for _ in frames]
    poses = sample_keys(clip["keys"], clip["length"])
    if clip.get("override"):
        poses = [clip["override"](f, p) for f, p in enumerate(poses)]
    frames, diags = [], []
    for p in poses:
        T, d = solve_pose(p)
        frames.append(T)
        diags.append(d)
    return frames, diags


# ---------------------------------------------------------------------------
# Quality checks
BODY_PARTS_FOR_SWORD = [
    "Head", "UpperTorso", "LowerTorso", "LeftUpperArm", "LeftLowerArm", "LeftHand",
    "RightUpperArm", "LeftUpperLeg", "LeftLowerLeg", "LeftFoot",
    "RightUpperLeg", "RightLowerLeg", "RightFoot",
]


def _inside(world, part, pt, pad=0.0):
    R, c = world[part]
    local = R.transposed() @ (pt - c)
    hx, hy, hz = (s / 2 + pad for s in PARTS[part][1])
    return abs(local.x) < hx and abs(local.y) < hy and abs(local.z) < hz


def check_clip(name, frames, diags):
    report = {"name": name, "issues": [], "stats": {}}
    tip_min = 99.0
    foot_paths = {"LeftFoot": [], "RightFoot": []}
    max_wrist = 0.0
    max_reach = 0.0
    for f, T in enumerate(frames):
        w = fk(T)
        tip, pommel, R, c = tip_and_pommel(w)
        tip_min = min(tip_min, tip.y)
        if tip.y < 0.05:
            report["issues"].append(f"f{f}: sword tip below ground (y={tip.y:.2f})")
        # blade from just past the guard to the tip
        hits = set()
        for k in range(1, 21):
            pt = c + R @ Vector((0, 0.55 + (3.875 - 0.55) * k / 20, 0))
            for part in BODY_PARTS_FOR_SWORD:
                if _inside(w, part, pt, pad=0.02):
                    hits.add(part)
        if hits:
            report["issues"].append(f"f{f}: blade passes through {sorted(hits)}")
        for foot in foot_paths:
            R_f, c_f = w[foot]
            corners = [c_f + R_f @ Vector((sx * 0.5, -0.15, sz * 0.5)) for sx in (-1, 1) for sz in (-1, 1)]
            foot_paths[foot].append((c_f.copy(), min(v.y for v in corners)))
        d = diags[f] if f < len(diags) else {}
        for limb, info in d.items():
            max_reach = max(max_reach, info.get("reach_err", 0.0))
            if info.get("reach_err", 0) > 0.03:
                report["issues"].append(f"f{f}: {limb} cannot reach target (off by {info['reach_err']:.2f})")
            if limb == "right_arm":
                max_wrist = max(max_wrist, info["wrist_deg"])
            if "elbow_deg" in info and not (0 <= info["elbow_deg"] <= 145):
                report["issues"].append(f"f{f}: {limb} elbow {info['elbow_deg']:.0f} deg")
            if "knee_deg" in info and info["knee_deg"] > 125:
                report["issues"].append(f"f{f}: {limb} knee {info['knee_deg']:.0f} deg")
    for foot, path in foot_paths.items():
        lows = [y for _, y in path]
        report["stats"][foot + "_lowest_y"] = round(min(lows), 3)
        # sliding: horizontal movement while the foot is on the ground
        slide = 0.0
        for (a, ya), (b, yb) in zip(path, path[1:]):
            if ya < 0.06 and yb < 0.06:
                slide = max(slide, math.hypot(b.x - a.x, b.z - a.z))
        report["stats"][foot + "_max_slide_per_frame"] = round(slide, 4)
        if slide > 0.01:
            report["issues"].append(f"{foot} slides {slide:.3f} studs in one frame while planted")
    report["stats"]["tip_lowest_y"] = round(tip_min, 3)
    report["stats"]["max_right_wrist_bend_deg"] = round(max_wrist, 1)
    report["stats"]["max_ik_reach_error"] = round(max_reach, 4)
    return report


def continuity(frames_a, frames_b):
    """Largest joint rotation jump (deg) between the last frame of A and the first of B."""
    A, B = frames_a[-1], frames_b[0]
    worst = 0.0
    for j in A:
        qa = A[j][0].to_quaternion()
        qb = B.get(j, (I3, Vector()))[0].to_quaternion()
        worst = max(worst, math.degrees(qa.rotation_difference(qb).angle))
    return worst
