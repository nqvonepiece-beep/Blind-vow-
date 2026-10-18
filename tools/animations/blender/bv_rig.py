"""Blind Vow - R15 rig math for sword animations (no Blender scene code here).

Everything is in Roblox space: X = right, Y = up, -Z = forward, floor at y = 0.
A joint "Transform" is exactly what a Roblox KeyframeSequence Pose.CFrame stores:
    Part1.CFrame = Part0.CFrame * C0 * Transform * C1:Inverse()
R15 rig attachments have no rotation, so C0/C1 are pure offsets to the joint pivot.

Part sizes and pivots approximate the default blocky R15 rig. Only joint ROTATIONS
(and the LowerTorso offset) are exported, so small size differences only change the
preview, not what Roblox plays.
"""

import math
from mathutils import Matrix, Quaternion, Vector

I3 = Matrix.Identity(3)


def rad(d):
    return math.radians(d)


def rx(d):
    return Matrix.Rotation(rad(d), 3, "X")


def ry(d):
    return Matrix.Rotation(rad(d), 3, "Y")


def rz(d):
    return Matrix.Rotation(rad(d), 3, "Z")


def angles(x, y, z):
    """Roblox CFrame.Angles(x, y, z) in degrees = Rx * Ry * Rz."""
    return rx(x) @ ry(y) @ rz(z)


def ypr(yaw=0.0, pitch=0.0, roll=0.0):
    """Yaw (turn left +), then pitch (lean back +), then roll."""
    return ry(yaw) @ rx(pitch) @ rz(roll)


# name: (center, size) at rest
PARTS = {
    "HumanoidRootPart": ((0.0, 3.0, 0.0), (2.0, 2.0, 1.0)),
    "LowerTorso": ((0.0, 2.2, 0.0), (2.0, 0.4, 1.0)),
    "UpperTorso": ((0.0, 3.2, 0.0), (2.0, 1.6, 1.0)),
    "Head": ((0.0, 4.6, 0.0), (1.2, 1.2, 1.2)),
    "RightUpperArm": ((1.5, 3.4, 0.0), (1.0, 1.2, 1.0)),
    "RightLowerArm": ((1.5, 2.65, 0.0), (1.0, 0.7, 1.0)),
    "RightHand": ((1.5, 2.15, 0.0), (1.0, 0.3, 1.0)),
    "LeftUpperArm": ((-1.5, 3.4, 0.0), (1.0, 1.2, 1.0)),
    "LeftLowerArm": ((-1.5, 2.65, 0.0), (1.0, 0.7, 1.0)),
    "LeftHand": ((-1.5, 2.15, 0.0), (1.0, 0.3, 1.0)),
    "RightUpperLeg": ((0.5, 1.55, 0.0), (1.0, 0.9, 1.0)),
    "RightLowerLeg": ((0.5, 0.7, 0.0), (1.0, 0.8, 1.0)),
    "RightFoot": ((0.5, 0.15, 0.0), (1.0, 0.3, 1.0)),
    "LeftUpperLeg": ((-0.5, 1.55, 0.0), (1.0, 0.9, 1.0)),
    "LeftLowerLeg": ((-0.5, 0.7, 0.0), (1.0, 0.8, 1.0)),
    "LeftFoot": ((-0.5, 0.15, 0.0), (1.0, 0.3, 1.0)),
}

# (child, parent, pivot) ordered root -> leaves. Child names = Motor6D Part1 names.
JOINTS = [
    ("LowerTorso", "HumanoidRootPart", (0.0, 2.0, 0.0)),
    ("UpperTorso", "LowerTorso", (0.0, 2.4, 0.0)),
    ("Head", "UpperTorso", (0.0, 4.0, 0.0)),
    ("RightUpperArm", "UpperTorso", (1.0, 3.763, 0.0)),
    ("RightLowerArm", "RightUpperArm", (1.5, 3.0, 0.0)),
    ("RightHand", "RightLowerArm", (1.5, 2.3, 0.0)),
    ("LeftUpperArm", "UpperTorso", (-1.0, 3.763, 0.0)),
    ("LeftLowerArm", "LeftUpperArm", (-1.5, 3.0, 0.0)),
    ("LeftHand", "LeftLowerArm", (-1.5, 2.3, 0.0)),
    ("RightUpperLeg", "LowerTorso", (0.5, 2.0, 0.0)),
    ("RightLowerLeg", "RightUpperLeg", (0.5, 1.1, 0.0)),
    ("RightFoot", "RightLowerLeg", (0.5, 0.3, 0.0)),
    ("LeftUpperLeg", "LowerTorso", (-0.5, 2.0, 0.0)),
    ("LeftLowerLeg", "LeftUpperLeg", (-0.5, 1.1, 0.0)),
    ("LeftFoot", "LeftLowerLeg", (-0.5, 0.3, 0.0)),
]
PARENT = {c: p for c, p, _ in JOINTS}
PIVOT = {c: Vector(v) for c, _, v in JOINTS}
CHILDREN = {}
for _c, _p, _ in JOINTS:
    CHILDREN.setdefault(_p, []).append(_c)

# ---------------------------------------------------------------------------
# Starter Longsword grip. Copied from src/shared/Config/WeaponModelConfig.luau
# (branch feat/sword-ready-idle). Directions are in the right hand's frame.
GRIP_BLADE_DIR = Vector((0.74, -0.63, 0.22))
GRIP_EDGE_DIR = Vector((0.17, -0.14, -0.98))
GRIP_OFFSET_Y = -0.2  # gripOffset (studs, Handle space)
GRIP_ATTACHMENT = Vector((0.0, -0.15, 0.0))  # RightGripAttachment in RightHand (R15)
# Sword part centers relative to the Grip part (from assets/roblox/weapons/StarterLongsword.rbxmx)
SWORD_TIP_FROM_HANDLE = (9.1259 - 6.9009) + 3.3 / 2  # 3.875 studs along the blade
SWORD_POMMEL_FROM_HANDLE = (6.2919 - 6.9009) - 0.308 / 2


def frame_from(blade, edge):
    """Rotation whose Y axis = blade (tip) direction and X axis = cutting edge."""
    b = Vector(blade).normalized()
    e = Vector(edge)
    e = (e - b * e.dot(b)).normalized()
    z = e.cross(b)
    return Matrix((e, b, z)).transposed()  # columns e, b, z


HANDLE_IN_HAND = frame_from(GRIP_BLADE_DIR, GRIP_EDGE_DIR)
# Handle center relative to the hand's grip attachment point, in hand space
HANDLE_POS_IN_HAND = GRIP_ATTACHMENT + HANDLE_IN_HAND @ Vector((0.0, -GRIP_OFFSET_Y, 0.0))
WRIST_TO_GRIP = GRIP_ATTACHMENT + Vector((0.0, PARTS["RightHand"][0][1] - PIVOT["RightHand"].y, 0.0))


def handle_world(hand_R, hand_c):
    R = hand_R @ HANDLE_IN_HAND
    c = hand_c + hand_R @ HANDLE_POS_IN_HAND
    return R, c


# ---------------------------------------------------------------------------
def fk(T):
    """T: {joint: (Matrix3 R, Vector p)} -> {part: (R world, center world)}."""
    world = {"HumanoidRootPart": (I3.copy(), Vector(PARTS["HumanoidRootPart"][0]))}
    for child, parent, pivot in JOINTS:
        R0, c0 = world[parent]
        Rt, pt = T.get(child, (I3, Vector()))
        piv0 = Vector(pivot) - Vector(PARTS[parent][0])
        piv1 = Vector(pivot) - Vector(PARTS[child][0])
        R1 = R0 @ Rt
        c1 = c0 + R0 @ piv0 + R0 @ pt - R1 @ piv1
        world[child] = (R1, c1)
    return world


def pivot_world(world, joint):
    """World position of a joint pivot (seen from the child part)."""
    R, c = world[joint]
    return c + R @ (PIVOT[joint] - Vector(PARTS[joint][0]))


def point_world(world, part, local_from_center):
    R, c = world[part]
    return c + R @ Vector(local_from_center)


# ---------------------------------------------------------------------------
def _rot_between(a, b):
    a = a.normalized()
    b = b.normalized()
    return a.rotation_difference(b).to_matrix()


def _signed_angle(u, v, axis):
    return math.atan2(axis.dot(u.cross(v)), u.dot(v))


def solve_hinge_chain(root_R_parent, root_pivot, u, v, target, pole, hinge_sign):
    """Two segment limb with a hinge about the upper segment's local X axis.

    u: pivot1 -> pivot2 in upper segment space; v: pivot2 -> end point in lower segment space.
    Lower = Upper @ Rx(hinge_sign * theta). Returns (R_upper_world, theta_deg, reach_error).
    """
    D = target - root_pivot
    dist = D.length
    L2 = v.length
    # |u + Rx(s*th) v|^2 = |u|^2 + |v|^2 + 2 u . Rx(s*th) v ; solve numerically (robust to offsets)
    best = None
    for i in range(0, 1501):
        th = i * 0.1
        r = (u + rx(hinge_sign * th) @ v).length
        err = abs(r - dist)
        if best is None or err < best[1]:
            best = (th, err)
    th, err = best
    a = u + rx(hinge_sign * th) @ v
    R0 = _rot_between(a, D)
    # twist about D so the middle pivot points toward the pole
    axis = D.normalized()
    mid = R0 @ u
    m = mid - axis * mid.dot(axis)
    n = pole - axis * pole.dot(axis)
    psi = 0.0
    if m.length > 1e-6 and n.length > 1e-6:
        psi = _signed_angle(m, n, axis)
    R = Matrix.Rotation(psi, 3, axis) @ R0
    return R, th, err


def twist_about_y(Rrel):
    """Twist angle (rad) of a rotation about its local Y axis (swing-twist split)."""
    q = Rrel.to_quaternion()
    t = Quaternion((q.w, 0.0, q.y, 0.0))
    if t.magnitude < 1e-9:
        return 0.0
    t.normalize()
    ang = 2.0 * math.atan2(t.y, t.w)
    if ang > math.pi:
        ang -= 2 * math.pi
    if ang < -math.pi:
        ang += 2 * math.pi
    return ang


FOREARM_TWIST_SHARE = 0.75  # how much of the hand's twist the forearm takes
# 0 = hand goes exactly where the key pose says; 1 = move the hand so the wrist stays straight.
NEUTRAL_WRIST_BLEND = 0.8
UPPER_ARM_LEN = (PIVOT["RightLowerArm"] - PIVOT["RightUpperArm"]).length
HAND_TO_GRIP = -WRIST_TO_GRIP.y + (PIVOT["RightHand"] - PIVOT["RightLowerArm"]).length  # elbow->grip, straight wrist


def solve_pose(p):
    """Pose spec (dict, see bv_poses.py) -> {joint: (R, pos)} Transforms + diagnostics."""
    T = {}
    diag = {}
    T["LowerTorso"] = (p["pelvis_q"].to_matrix(), Vector(p["pelvis_pos"]))
    T["UpperTorso"] = (p["chest_q"].to_matrix(), Vector())
    w = fk(T)
    R_ut, c_ut = w["UpperTorso"]
    T["Head"] = (R_ut.inverted() @ p["head_q"].to_matrix(), Vector())

    # --- right arm: grip point + sword orientation drive the hand ---
    R_handle = p["rhandle_q"].to_matrix()
    R_hand = R_handle @ HANDLE_IN_HAND.inverted()
    s = c_ut + R_ut @ (PIVOT["RightUpperArm"] - Vector(PARTS["UpperTorso"][0]))
    g_target = Vector(p["rgrip"])
    down = R_hand @ Vector((0.0, -HAND_TO_GRIP, 0.0))  # elbow -> grip with a straight wrist
    g_neutral = s + (g_target - down - s).normalized() * UPPER_ARM_LEN + down
    g = g_target.lerp(g_neutral, NEUTRAL_WRIST_BLEND)
    elbow_wanted = g - down
    wrist = g - R_hand @ WRIST_TO_GRIP
    axis = (wrist - s).normalized()
    pole = (elbow_wanted - s) - axis * (elbow_wanted - s).dot(axis)
    if pole.length < 1e-4:
        pole = Vector(p["relbow_pole"])
    T_arm, d = _solve_arm("Right", w, wrist, R_hand, pole.normalized())
    d["grip_shift"] = (g - g_target).length
    T.update(T_arm)
    diag["right_arm"] = d

    # --- left arm: wrist target moves with the chest ---
    lw = c_ut + R_ut @ Vector(p["lwrist"])
    lpole = R_ut @ Vector(p["lelbow_pole"])
    T_l, d = _solve_arm("Left", w, lw, None, lpole, hand_rel=p["lhand_q"].to_matrix())
    T.update(T_l)
    diag["left_arm"] = d

    # --- legs: feet are world placed ---
    w = fk(T)
    for side in ("Right", "Left"):
        key = "rfoot" if side == "Right" else "lfoot"
        R_foot = p[key + "_q"].to_matrix()
        foot_c = Vector(p[key + "_pos"])
        ankle = foot_c + R_foot @ (PIVOT[side + "Foot"] - Vector(PARTS[side + "Foot"][0]))
        T_leg, d = _solve_leg(side, w, ankle, R_foot, Vector(p[key[0] + "knee_pole"]))
        T.update(T_leg)
        diag[side.lower() + "_leg"] = d
    return T, diag


def _solve_arm(side, w, wrist, R_hand, pole, hand_rel=None):
    up, lo, hd = side + "UpperArm", side + "LowerArm", side + "Hand"
    R_par, c_par = w["UpperTorso"]
    s = c_par + R_par @ (PIVOT[up] - Vector(PARTS["UpperTorso"][0]))
    u = PIVOT[lo] - PIVOT[up]
    v = PIVOT[hd] - PIVOT[lo]
    R_u, th, err = solve_hinge_chain(R_par, s, u, v, wrist, pole, +1)
    R_l0 = R_u @ rx(th)
    if R_hand is None:
        R_l = R_l0
        R_h = R_l @ hand_rel
    else:
        tw = twist_about_y(R_l0.inverted() @ R_hand)
        R_l = R_l0 @ Matrix.Rotation(tw * FOREARM_TWIST_SHARE, 3, "Y")
        R_h = R_hand
    T = {
        up: (R_par.inverted() @ R_u, Vector()),
        lo: (R_u.inverted() @ R_l, Vector()),
        hd: (R_l.inverted() @ R_h, Vector()),
    }
    # visible wrist bend = angle between forearm axis and hand axis (twist is hidden on blocks)
    bend = math.degrees((R_l @ Vector((0, -1, 0))).angle(R_h @ Vector((0, -1, 0))))
    return T, {"elbow_deg": th, "reach_err": err, "wrist_deg": bend}


def _solve_leg(side, w, ankle, R_foot, pole):
    up, lo, ft = side + "UpperLeg", side + "LowerLeg", side + "Foot"
    R_par, c_par = w["LowerTorso"]
    h = c_par + R_par @ (PIVOT[up] - Vector(PARTS["LowerTorso"][0]))
    u = PIVOT[lo] - PIVOT[up]
    v = PIVOT[ft] - PIVOT[lo]
    R_u, th, err = solve_hinge_chain(R_par, h, u, v, ankle, pole, -1)
    R_l = R_u @ rx(-th)
    T = {
        up: (R_par.inverted() @ R_u, Vector()),
        lo: (R_u.inverted() @ R_l, Vector()),
        ft: (R_l.inverted() @ R_foot, Vector()),
    }
    ankle_rel = (R_l.inverted() @ R_foot).to_quaternion()
    return T, {"knee_deg": th, "reach_err": err, "ankle_deg": math.degrees(ankle_rel.angle)}


# ---------------------------------------------------------------------------
def pose_from_fk(T):
    """Express an FK pose (e.g. the Studio-tested ready stance) as an IK pose spec."""
    w = fk(T)
    p = {}
    p["pelvis_pos"] = Vector(T.get("LowerTorso", (I3, Vector()))[1])
    p["pelvis_q"] = T.get("LowerTorso", (I3, Vector()))[0].to_quaternion()
    p["chest_q"] = T.get("UpperTorso", (I3, Vector()))[0].to_quaternion()
    p["head_q"] = w["Head"][0].to_quaternion()
    Rh, ch = w["RightHand"]
    p["rgrip"] = ch + Rh @ GRIP_ATTACHMENT
    p["rhandle_q"] = (Rh @ HANDLE_IN_HAND).to_quaternion()
    p["relbow_pole"] = _pole(w, "RightUpperArm", "RightLowerArm", "RightHand", "UpperTorso")
    R_ut, c_ut = w["UpperTorso"]
    p["lwrist"] = R_ut.inverted() @ (pivot_world(w, "LeftHand") - c_ut)  # chest space
    p["lelbow_pole"] = R_ut.inverted() @ _pole(w, "LeftUpperArm", "LeftLowerArm", "LeftHand", "UpperTorso")
    p["lhand_q"] = T.get("LeftHand", (I3, Vector()))[0].to_quaternion()
    for side, key in (("Right", "r"), ("Left", "l")):
        Rf, cf = w[side + "Foot"]
        p[key + "foot_pos"] = cf.copy()
        p[key + "foot_q"] = Rf.to_quaternion()
        p[key + "knee_pole"] = _pole(w, side + "UpperLeg", side + "LowerLeg", side + "Foot", "LowerTorso")
    return p


def _pole(w, up, lo, end, parent):
    R_par, c_par = w[parent]
    s = c_par + R_par @ (PIVOT[up] - Vector(PARTS[parent][0]))
    e = pivot_world(w, lo)
    t = pivot_world(w, end)
    axis = (t - s).normalized()
    m = (e - s) - axis * (e - s).dot(axis)
    return m.normalized() if m.length > 1e-6 else Vector((0, 0, -1))


def tip_and_pommel(world):
    R, c = handle_world(*world["RightHand"])
    return (
        c + R @ Vector((0, SWORD_TIP_FROM_HANDLE, 0)),
        c + R @ Vector((0, SWORD_POMMEL_FROM_HANDLE, 0)),
        R,
        c,
    )
