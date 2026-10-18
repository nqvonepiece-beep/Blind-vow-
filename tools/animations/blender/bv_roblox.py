"""Blind Vow - write Roblox KeyframeSequence (.rbxmx) files.

Same XML layout as tools/animations/Build-SwordAnimations.ps1 (feat/sword-ready-idle),
which was tested in Studio through AnimationClipProvider:RegisterAnimationClip.
"""

from mathutils import Vector

from bv_rig import I3

TREE = {
    "HumanoidRootPart": {
        "LowerTorso": {
            "UpperTorso": {
                "Head": {},
                "RightUpperArm": {"RightLowerArm": {"RightHand": {}}},
                "LeftUpperArm": {"LeftLowerArm": {"LeftHand": {}}},
            },
            "LeftUpperLeg": {"LeftLowerLeg": {"LeftFoot": {}}},
            "RightUpperLeg": {"RightLowerLeg": {"RightFoot": {}}},
        }
    }
}

# Enum values
EASING = {"Linear": 0, "Constant": 1, "Elastic": 2, "Cubic": 3, "Bounce": 4}
DIRECTION = {"In": 0, "Out": 1, "InOut": 2}


def _f(v):
    s = f"{round(v, 6):.6f}".rstrip("0").rstrip(".")
    return "0" if s in ("-0", "") else s


class _Refs:
    def __init__(self):
        self.n = 0

    def next(self):
        self.n += 1
        return f"RBX{self.n}"


def _cframe(R, p):
    s = f'<CoordinateFrame name="CFrame"><X>{_f(p.x)}</X><Y>{_f(p.y)}</Y><Z>{_f(p.z)}</Z>'
    names = ["R00", "R01", "R02", "R10", "R11", "R12", "R20", "R21", "R22"]
    vals = [R[i][j] for i in range(3) for j in range(3)]
    for n, v in zip(names, vals):
        s += f"<{n}>{_f(v)}</{n}>"
    return s + "</CoordinateFrame>"


def _pose_xml(refs, name, children, T, easing, direction):
    animated = name in T and name != "HumanoidRootPart"
    R, p = T.get(name, (I3, Vector()))
    s = f'<Item class="Pose" referent="{refs.next()}"><Properties>'
    s += f'<string name="Name">{name}</string>'
    s += _cframe(R, p)
    s += f'<token name="EasingStyle">{EASING[easing]}</token><token name="EasingDirection">{DIRECTION[direction]}</token>'
    s += f'<float name="Weight">{1 if animated else 0}</float>'
    s += "</Properties>"
    for c, sub in children.items():
        s += _pose_xml(refs, c, sub, T, easing, direction)
    return s + "</Item>"


def write_keyframe_sequence(path, name, keyframes, loop, priority, markers=None,
                            easing="Linear", direction="In"):
    """keyframes: [(time_seconds, {joint: (R, p)})]; markers: {marker_name: time_seconds}."""
    refs = _Refs()
    markers = markers or {}
    xml = '<roblox xmlns:xmime="http://www.w3.org/2005/05/xmlmime" version="4">'
    xml += f'<Item class="KeyframeSequence" referent="{refs.next()}"><Properties>'
    xml += f'<string name="Name">{name}</string><bool name="Loop">{"true" if loop else "false"}</bool>'
    xml += f'<token name="Priority">{priority}</token>'
    xml += "</Properties>"
    for t, T in keyframes:
        xml += f'<Item class="Keyframe" referent="{refs.next()}"><Properties>'
        xml += f'<string name="Name">Keyframe</string><float name="Time">{_f(t)}</float></Properties>'
        for root, sub in TREE.items():
            xml += _pose_xml(refs, root, sub, T, easing, direction)
        for m_name, m_time in markers.items():
            if abs(m_time - t) < 1e-4:
                xml += f'<Item class="KeyframeMarker" referent="{refs.next()}"><Properties>'
                xml += f'<string name="Name">{m_name}</string><string name="Value"></string>'
                xml += "</Properties></Item>"
        xml += "</Item>"
    xml += "</Item></roblox>"
    with open(path, "w", encoding="utf-8", newline="") as fh:
        fh.write(xml)
    return path
