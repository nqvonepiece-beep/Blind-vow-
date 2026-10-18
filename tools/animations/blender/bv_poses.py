"""Blind Vow - key poses and timing for the sword combat set (Roblox space, see bv_rig.py).

Motion reference: Deepwoken PvP clip supplied by Vinny (only timing / body mechanics were
studied; nothing is copied). Observed pattern, used here:
  - forehand diagonal cut, high-right -> low-left (clip ~1.47-1.80 s and ~3.40-3.87 s)
  - backhand horizontal cut, left -> right at waist height (clip ~2.43-2.83 s and ~3.87-4.33 s)
  - sword re-raised upright beside the right shoulder between cuts (clip ~2.97 s, ~3.40 s)
  - one wide, high backhand sweep left -> right (clip ~9.95-10.25 s)
  - strike itself ~0.10-0.15 s, a new swing every ~0.4-0.5 s, wide low stance, little stepping.

Timing is locked to the current server combat config (WeaponConfig.Sword):
  windup 0.15 s -> contact frame 5 (0.167 s) at 30 fps; cooldown 0.6 s -> 18 frame clips.
"""

import math
from mathutils import Matrix, Quaternion, Vector

from bv_rig import angles, frame_from, pose_from_fk, ypr

FPS = 30


def J(x, y, z, py=0.0):
    return (angles(x, y, z), Vector((0.0, py, 0.0)))


# Studio-tested ready stance from feat/sword-ready-idle (tools/animations/Build-SwordAnimations.ps1):
# SwordHold (right arm) + SwordReadyIdle (rest of the body). Do not change without Vinny.
READY_FK = {
    "LowerTorso": J(0, -8, 0, -0.14),
    "UpperTorso": J(-4, -4, 0),
    "Head": J(3, 12, 0),
    "LeftUpperArm": J(10, 0, -20),
    "LeftLowerArm": J(75, 0, 0),
    "LeftHand": J(-10, 0, 0),
    "LeftUpperLeg": J(35, 0, -12),
    "LeftLowerLeg": J(-40, 0, 0),
    "LeftFoot": J(5, 0, 0),
    "RightUpperLeg": J(-12, 0, 14),
    "RightLowerLeg": J(-26, 0, 0),
    "RightFoot": J(38, 0, 0),
    "RightUpperArm": J(-10, 0, 12),
    "RightLowerArm": J(15, 0, 0),
    "RightHand": J(0, 0, 0),
}
READY_BREATH_FK = dict(READY_FK)
READY_BREATH_FK.update(
    {
        "LowerTorso": J(0, -8, 0, -0.12),
        "UpperTorso": J(-2.5, -4, 0),
        "Head": J(1.5, 12, 0),
        "LeftUpperArm": J(12, 0, -20),
        "LeftLowerArm": J(72, 0, 0),
        "RightUpperArm": J(-9, 0, 12),
    }
)

READY = pose_from_fk(READY_FK)


def P(base, **kw):
    """Copy a pose and override channels. Euler helpers: pelvis=(yaw,pitch,roll), chest=..., head=..."""
    p = {k: (v.copy() if hasattr(v, "copy") else v) for k, v in base.items()}
    for k, v in kw.items():
        if k == "pelvis":
            p["pelvis_q"] = ypr(*v).to_quaternion()
        elif k == "chest":
            p["chest_q"] = ypr(*v).to_quaternion()
        elif k == "head":
            p["head_q"] = ypr(*v).to_quaternion()
        elif k == "sword":
            blade, edge = v
            p["rhandle_q"] = frame_from(blade, edge).to_quaternion()
        elif k in ("lfoot_q", "rfoot_q", "lhand_q") and isinstance(v, tuple):
            p[k] = ypr(*v).to_quaternion()
        else:
            p[k] = Vector(v) if isinstance(v, tuple) else v
    return p


def _blend(a, b, t):
    """Pose between a and b (positions lerp, rotations slerp)."""
    out = {}
    for k in a:
        if isinstance(a[k], Quaternion):
            out[k] = a[k].slerp(b[k], t)
        else:
            out[k] = Vector(a[k]).lerp(Vector(b[k]), t)
    return out


def swing(normal, start_blade, deg, tilt=0.0):
    """Blade/edge for a cut in the plane with this normal.

    The blade starts at start_blade (projected into the plane) and rotates by deg about the
    normal; the cutting edge always faces the direction of travel. tilt leans the tip out of
    the plane toward +normal (wrist roll at the ends of a cut).
    """
    n = Vector(normal).normalized()
    b0 = Vector(start_blade)
    b0 = (b0 - n * b0.dot(n)).normalized()
    b = Matrix.Rotation(math.radians(deg), 3, n) @ b0
    e = n.cross(b)
    if tilt:
        b = Matrix.Rotation(math.radians(tilt), 3, e) @ b
    return (tuple(b), tuple(e))


# ---------------------------------------------------------------------------
# Cut planes (normal vectors). Character faces -Z, right is +X.
FWD = (0.0, 0.0, -1.0)
# forehand diagonal, ~38 deg from horizontal: travels from upper-right to lower-left
PLANE_DIAG = (-math.sin(math.radians(38)), math.cos(math.radians(38)), 0.12)
# backhand horizontal at waist: travels left -> right (tip sweeps through the front)
PLANE_FLAT = (0.0, -1.0, 0.0)
# steep forehand (~62 deg) for attack 3
PLANE_STEEP = (-math.sin(math.radians(62)), math.cos(math.radians(62)), 0.15)
# finisher: high backhand, slightly rising toward the right shoulder
PLANE_HIGH = (0.12, -1.0, -0.18)

HEAD_FWD = (0.0, -4.0, 0.0)


def _attack1():
    base = READY
    raise_ = P(
        base,
        pelvis_pos=(0.0, -0.16, 0.03),
        pelvis=(-10, 1, 0),
        chest=(-12, 1, 3),
        rgrip=(1.95, 3.35, 0.45),
        sword=((0.8, 0.5, 0.35), (-0.1, -0.2, -1.0)),
    )
    chamber = P(
        base,
        pelvis_pos=(0.0, -0.17, 0.06),
        pelvis=(-16, 2, 0),
        chest=(-22, 2, 5),
        head=(-6, -2, 0),
        rgrip=(1.45, 4.3, 0.35),
        sword=((0.22, 0.92, 0.4), (-0.45, 0.0, -1.0)),
        relbow_pole=(1.0, -0.5, 0.6),
        lwrist=(-1.3, -0.2, -1.1),
        lelbow_pole=(-0.5, -0.6, 0.6),
    )
    pre = P(  # blade just before contact (shapes the arc)
        chamber,
        pelvis_pos=(0.0, -0.2, -0.04),
        pelvis=(-4, 0, 0),
        chest=(-6, -4, 0),
        rgrip=(0.95, 3.75, -1.05),
        sword=swing(PLANE_DIAG, FWD, -45),
        relbow_pole=(1.0, -0.8, 0.4),
    )
    contact = P(
        chamber,
        pelvis_pos=(0.0, -0.24, -0.14),
        pelvis=(6, -2, -2),
        chest=(10, -9, -7),
        head=(2, -5, -3),
        rgrip=(0.25, 3.05, -1.5),
        sword=swing(PLANE_DIAG, FWD, 0),
        relbow_pole=(0.8, -1.0, 0.2),
        lwrist=(-1.5, -0.55, -0.35),
        lelbow_pole=(-0.5, -0.4, 0.8),
    )
    follow = P(
        contact,
        pelvis_pos=(0.0, -0.27, -0.16),
        pelvis=(14, -3, -3),
        chest=(18, -10, -8),
        head=(6, -5, -3),
        rgrip=(-0.55, 2.55, -0.95),
        sword=swing(PLANE_DIAG, FWD, 70, tilt=-18),
        relbow_pole=(0.2, -1.0, 0.3),
        lwrist=(-1.55, -0.75, 0.15),
    )
    settle = P(
        follow,
        pelvis_pos=(0.0, -0.24, -0.12),
        pelvis=(13, -2, -2),
        chest=(17, -8, -6),
        rgrip=(-0.5, 2.6, -0.9),
        sword=swing(PLANE_DIAG, FWD, 68, tilt=-20),
    )
    end = P(  # settled chain pose = start of attack 2
        follow,
        pelvis_pos=(0.0, -0.22, -0.1),
        pelvis=(12, -2, -2),
        chest=(16, -7, -5),
        head=(4, -4, -2),
        rgrip=(-0.45, 2.65, -0.85),
        sword=swing(PLANE_DIAG, FWD, 66, tilt=-22),
        lwrist=(-1.55, -0.7, 0.05),
    )
    keys = [
        (0, base, "inout"),
        (2, raise_, "lin"),
        (3, chamber, "out"),
        (4, pre, "in"),
        (5, contact, "lin"),
        (8, follow, "out"),
        (12, settle, "lin"),
        (18, end, "inout"),
    ]
    return keys, end


def _attack2(start):
    coil = P(
        start,
        pelvis_pos=(0.0, -0.23, -0.06),
        pelvis=(16, -1, -1),
        chest=(24, -5, -3),
        head=(2, -4, 0),
        rgrip=(-0.75, 2.75, -0.55),
        sword=swing(PLANE_FLAT, (-1.0, 0.0, 0.25), 0, tilt=6),
        relbow_pole=(0.2, -1.0, -0.2),
        lwrist=(-1.5, -0.7, 0.25),
    )
    pre = P(
        coil,
        pelvis=(8, -1, 0),
        chest=(12, -5, 0),
        rgrip=(-0.25, 2.85, -1.3),
        sword=swing(PLANE_FLAT, (-1.0, 0.0, 0.25), 55, tilt=4),
        relbow_pole=(0.4, -1.0, 0.0),
    )
    contact = P(
        coil,
        pelvis_pos=(0.0, -0.26, -0.16),
        pelvis=(-2, -2, 0),
        chest=(-6, -7, 2),
        head=(-2, -5, 0),
        rgrip=(0.55, 2.95, -1.45),
        sword=swing(PLANE_FLAT, (-1.0, 0.0, 0.25), 98),
        relbow_pole=(0.9, -1.0, 0.1),
        lwrist=(-1.55, -0.35, -0.7),
        lelbow_pole=(-0.5, -0.5, 0.7),
    )
    follow = P(
        contact,
        pelvis_pos=(0.0, -0.25, -0.1),
        pelvis=(-14, -1, 1),
        chest=(-20, -5, 4),
        head=(-6, -4, 0),
        rgrip=(1.55, 3.0, -0.75),
        sword=swing(PLANE_FLAT, (-1.0, 0.0, 0.25), 165, tilt=-8),
        relbow_pole=(1.0, -0.6, 0.6),
        lwrist=(-1.5, -0.15, -1.0),
    )
    end = P(
        follow,
        pelvis_pos=(0.0, -0.22, -0.06),
        pelvis=(-12, 0, 1),
        chest=(-16, -4, 3),
        head=(-4, -4, 0),
        rgrip=(1.55, 3.05, -0.55),
        sword=swing(PLANE_FLAT, (-1.0, 0.0, 0.25), 168, tilt=-14),
        lwrist=(-1.55, -0.1, -0.95),
    )
    keys = [
        (0, start, "lin"),
        (3, coil, "inout"),
        (4, pre, "in"),
        (5, contact, "lin"),
        (8, follow, "out"),
        (12, _blend(follow, end, 0.65), "lin"),
        (18, end, "inout"),
    ]
    return keys, end


def _attack3(start):
    chamber = P(
        start,
        pelvis_pos=(0.0, -0.16, 0.06),
        pelvis=(-18, 3, 0),
        chest=(-24, 4, 6),
        head=(-6, -1, 0),
        rgrip=(1.15, 4.55, 0.15),
        sword=swing(PLANE_STEEP, FWD, -130),
        relbow_pole=(1.0, -0.3, 0.5),
        lwrist=(-1.3, -0.15, -1.15),
        lelbow_pole=(-0.5, -0.6, 0.6),
    )
    pre = P(
        chamber,
        pelvis_pos=(0.0, -0.22, -0.06),
        pelvis=(-6, 0, 0),
        chest=(-8, -6, 2),
        rgrip=(0.8, 4.0, -1.0),
        sword=swing(PLANE_STEEP, FWD, -50),
        relbow_pole=(1.0, -0.7, 0.3),
    )
    contact = P(
        chamber,
        pelvis_pos=(0.0, -0.32, -0.18),
        pelvis=(6, -4, -3),
        chest=(8, -14, -9),
        head=(2, -8, -3),
        rgrip=(0.3, 3.0, -1.45),
        sword=swing(PLANE_STEEP, FWD, 0),
        relbow_pole=(0.8, -1.0, 0.2),
        lwrist=(-1.5, -0.6, -0.3),
        lelbow_pole=(-0.5, -0.4, 0.8),
    )
    follow = P(
        contact,
        pelvis_pos=(0.0, -0.36, -0.2),
        pelvis=(12, -5, -3),
        chest=(14, -16, -9),
        head=(4, -8, -3),
        rgrip=(-0.35, 2.4, -1.05),
        sword=swing(PLANE_STEEP, FWD, 58, tilt=-30),
        relbow_pole=(0.3, -1.0, 0.3),
        lwrist=(-1.55, -0.8, 0.15),
    )
    end = P(
        follow,
        pelvis_pos=(0.0, -0.28, -0.14),
        pelvis=(12, -3, -2),
        chest=(16, -10, -6),
        head=(4, -5, -2),
        rgrip=(-0.45, 2.6, -0.9),
        sword=swing(PLANE_STEEP, FWD, 60, tilt=-36),
        lwrist=(-1.55, -0.7, 0.1),
    )
    keys = [
        (0, start, "lin"),
        (3, chamber, "out"),
        (4, pre, "in"),
        (5, contact, "lin"),
        (8, follow, "out"),
        (12, _blend(follow, end, 0.65), "lin"),
        (18, end, "inout"),
    ]
    return keys, end


STEP_LIFT = (1, 5)  # left foot steps in (frames)
STEP_BACK = (19, 24)  # and back to the stance
STEP_OFFSET = Vector((-0.1, 0.0, -0.5))


def _attack4_feet(frame, pose):
    """Left foot step-in and step-back with a lifted arc (no sliding while planted)."""
    a = READY["lfoot_pos"]
    b = a + STEP_OFFSET

    def arc(p0, p1, s):
        s2 = s * s * (3 - 2 * s)
        pos = p0.lerp(p1, s2)
        pos.y += 0.32 * math.sin(math.pi * s)
        return pos

    if frame <= STEP_LIFT[0]:
        pos = a
    elif frame < STEP_LIFT[1]:
        pos = arc(a, b, (frame - STEP_LIFT[0]) / (STEP_LIFT[1] - STEP_LIFT[0]))
    elif frame <= STEP_BACK[0]:
        pos = b
    elif frame < STEP_BACK[1]:
        pos = arc(b, a, (frame - STEP_BACK[0]) / (STEP_BACK[1] - STEP_BACK[0]))
    else:
        pos = a
    pose["lfoot_pos"] = pos.copy()
    return pose


def _attack4(start):
    """Finisher: wide high backhand with a short left-foot step-in, then back to the stance."""
    coil = P(
        start,
        pelvis_pos=(0.0, -0.25, 0.06),
        pelvis=(18, 0, -1),
        chest=(28, -3, -4),
        head=(4, -3, 0),
        rgrip=(-0.85, 3.35, -0.35),
        sword=swing(PLANE_HIGH, (-1.0, 0.15, 0.35), 0, tilt=8),
        relbow_pole=(0.0, -1.0, -0.4),
        lwrist=(-1.5, -0.7, 0.3),
    )
    plant = P(
        coil,
        pelvis_pos=(0.0, -0.37, -0.16),
        pelvis=(12, -2, 0),
        chest=(20, -6, -2),
        rgrip=(-0.6, 3.4, -1.0),
        sword=swing(PLANE_HIGH, (-1.0, 0.15, 0.35), 30, tilt=6),
        relbow_pole=(0.2, -1.0, -0.2),
    )
    contact = P(
        plant,
        pelvis_pos=(0.0, -0.35, -0.18),
        pelvis=(-4, -3, 1),
        chest=(-8, -8, 3),
        head=(-2, -5, 0),
        rgrip=(0.55, 3.45, -1.55),
        sword=swing(PLANE_HIGH, (-1.0, 0.15, 0.35), 100),
        relbow_pole=(0.9, -1.0, 0.0),
        lwrist=(-1.55, -0.4, -0.6),
        lelbow_pole=(-0.5, -0.5, 0.7),
    )
    follow = P(
        contact,
        pelvis_pos=(0.0, -0.33, -0.15),
        pelvis=(-20, -2, 2),
        chest=(-28, -5, 6),
        head=(-8, -4, 0),
        rgrip=(1.7, 3.35, -0.55),
        sword=swing(PLANE_HIGH, (-1.0, 0.15, 0.35), 175, tilt=-10),
        relbow_pole=(1.0, -0.4, 0.6),
        lwrist=(-1.5, -0.15, -1.0),
    )
    hold = P(
        follow,
        pelvis_pos=(0.0, -0.31, -0.13),
        pelvis=(-18, -1, 2),
        chest=(-24, -4, 5),
        rgrip=(1.75, 3.2, -0.35),
        sword=swing(PLANE_HIGH, (-1.0, 0.15, 0.35), 182, tilt=-22),
    )
    lift_back = P(
        hold,
        pelvis_pos=(0.0, -0.2, -0.08),
        pelvis=(-12, 0, 1),
        chest=(-12, -4, 2),
    )
    lower = P(  # sword comes down with the tip still above the ground
        READY,
        pelvis_pos=(0.0, -0.17, -0.04),
        pelvis=(-10, 0, 0),
        chest=(-8, -4, 1),
        rgrip=(1.95, 2.45, 0.1),
        sword=((0.93, -0.12, 0.35), (0.12, -0.2, -1.0)),
    )
    keys = [
        (0, start, "lin"),
        (3, coil, "inout"),
        (5, plant, "inout"),
        (6, contact, "in"),
        (10, follow, "out"),
        (15, hold, "inout"),
        (20, lift_back, "lin"),
        (23, lower, "lin"),
        (27, READY, "inout"),
    ]
    return keys


def build_clips():
    """name -> dict(keys or fk, length frames, loop, markers {name: frame})."""
    k1, e1 = _attack1()
    k2, e2 = _attack2(e1)
    k3, e3 = _attack3(e2)
    k4 = _attack4(e3)
    return {
        "Sword_CombatIdle": {
            "fk_keys": [(0, READY_FK), (48, READY_BREATH_FK), (96, READY_FK)],
            "length": 96,
            "loop": True,
            "priority": 2,  # Action (same as SwordReadyIdle)
            "markers": {},
        },
        "Sword_M1_01": {"keys": k1, "length": 18, "loop": False, "priority": 3,
                         "markers": {"Hit": 5, "ComboWindow": 10}},
        "Sword_M1_02": {"keys": k2, "length": 18, "loop": False, "priority": 3,
                         "markers": {"Hit": 5, "ComboWindow": 10}},
        "Sword_M1_03": {"keys": k3, "length": 18, "loop": False, "priority": 3,
                         "markers": {"Hit": 5, "ComboWindow": 10}},
        "Sword_M1_04": {"keys": k4, "length": 27, "loop": False, "priority": 3,
                         "override": _attack4_feet,
                         "markers": {"Hit": 6, "Recover": 15}},
    }
