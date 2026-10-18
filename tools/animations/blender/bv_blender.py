"""Blind Vow - build the Blender scene (R15 armature + Starter Longsword), write actions,
render previews, and export FBX / Roblox KeyframeSequence files."""

import math
import os

import bpy
from mathutils import Matrix, Vector

from bv_rig import (
    HANDLE_IN_HAND, HANDLE_POS_IN_HAND, JOINTS, PARENT, PARTS, PIVOT, fk, tip_and_pommel,
)

# Blender world = RX90 * Roblox space (Z up). Same convention as StarterLongsword.blend/.fbx.
RX90 = Matrix.Rotation(math.radians(90), 4, "X")
RX90_3 = RX90.to_3x3()
ARMATURE_NAME = "BV_R15_Rig"
BONES = ["HumanoidRootPart"] + [c for c, _, _ in JOINTS]

COLORS = {
    "Head": (0.85, 0.72, 0.6, 1),
    "UpperTorso": (0.12, 0.12, 0.14, 1),
    "LowerTorso": (0.2, 0.08, 0.08, 1),
    "Arm": (0.16, 0.16, 0.19, 1),
    "Hand": (0.85, 0.72, 0.6, 1),
    "Leg": (0.22, 0.2, 0.18, 1),
    "Foot": (0.35, 0.25, 0.15, 1),
}


def _color_for(part):
    for key in ("Head", "UpperTorso", "LowerTorso", "Hand", "Foot"):
        if part.endswith(key):
            return COLORS[key]
    return COLORS["Arm"] if "Arm" in part else COLORS["Leg"]


def to_bl(v):
    return RX90_3 @ Vector(v)


def _bone_head_tail(name):
    if name == "HumanoidRootPart":
        c = Vector(PARTS[name][0])
        return c, c + Vector((0, 0.6, 0))
    piv = PIVOT[name]
    c = Vector(PARTS[name][0])
    return piv, c + (c - piv)


def new_scene(fps):
    bpy.ops.wm.read_factory_settings(use_empty=True)
    sc = bpy.context.scene
    sc.render.fps = fps
    sc.unit_settings.system = "METRIC"
    sc.unit_settings.scale_length = 1.0
    return sc


def _collection(name):
    col = bpy.data.collections.new(name)
    bpy.context.scene.collection.children.link(col)
    return col


def build_rig():
    col = _collection("Rig")
    arm_data = bpy.data.armatures.new(ARMATURE_NAME)
    arm = bpy.data.objects.new(ARMATURE_NAME, arm_data)
    col.objects.link(arm)
    bpy.context.view_layer.objects.active = arm
    bpy.ops.object.mode_set(mode="EDIT")
    for name in BONES:
        b = arm_data.edit_bones.new(name)
        h, t = _bone_head_tail(name)
        b.head = to_bl(h)
        b.tail = to_bl(t)
        b.roll = 0.0
        b.use_connect = False
        b.use_deform = True
    for name in BONES[1:]:
        arm_data.edit_bones[name].parent = arm_data.edit_bones[PARENT[name]]
    bpy.ops.object.mode_set(mode="OBJECT")
    arm_data.display_type = "STICK"
    for pb in arm.pose.bones:
        pb.rotation_mode = "QUATERNION"

    # Rigid R15 block parts (preview only, not exported to the animation FBX)
    body = _collection("Body_Preview")
    for name in BONES:
        if name == "HumanoidRootPart":
            continue
        size = PARTS[name][1]
        me = bpy.data.meshes.new("Mesh_" + name)
        hx, hy, hz = (s / 2 for s in size)
        verts = [(x, y, z) for x in (-hx, hx) for y in (-hy, hy) for z in (-hz, hz)]
        faces = [(0, 1, 3, 2), (4, 6, 7, 5), (0, 4, 5, 1), (2, 3, 7, 6), (0, 2, 6, 4), (1, 5, 7, 3)]
        me.from_pydata(verts, [], faces)
        ob = bpy.data.objects.new("Body_" + name, me)
        ob.color = _color_for(name)
        body.objects.link(ob)
        ob.parent = arm
        ob.parent_type = "BONE"
        ob.parent_bone = name
        ob.matrix_world = RX90 @ Matrix.Translation(PARTS[name][0])
    # face marker (preview only) so the facing direction is readable
    face = _box("FaceMarker_PreviewOnly", (0.7, 0.25, 0.08), (0.1, 0.1, 0.1, 1), body)
    face.parent = arm
    face.parent_type = "BONE"
    face.parent_bone = "Head"
    face.matrix_world = RX90 @ Matrix.Translation((0, 4.7, -0.62))
    return arm


def attach_sword(arm, sword_blend):
    """Append the Starter Longsword meshes (source file stays untouched) and hold them with
    the same Tool.Grip as the game (WeaponModelConfig)."""
    col = _collection("StarterLongsword")
    with bpy.data.libraries.load(sword_blend, link=False) as (src, dst):
        dst.objects = [n for n in src.objects if n in ("Grip", "Blade", "Guard", "Pommel")]
    handle = bpy.data.objects.new("SwordHandle_RightGrip", None)
    handle.empty_display_type = "ARROWS"
    handle.empty_display_size = 0.4
    col.objects.link(handle)
    handle.parent = arm
    handle.parent_type = "BONE"
    handle.parent_bone = "RightHand"
    hand_c = Vector(PARTS["RightHand"][0])
    H = Matrix.Translation(hand_c + HANDLE_POS_IN_HAND) @ HANDLE_IN_HAND.to_4x4()
    handle.matrix_world = RX90 @ H
    grip_obj = next(o for o in dst.objects if o.name.startswith("Grip"))
    vs = [v.co for v in grip_obj.data.vertices]
    grip_center = Vector([(min(v[i] for v in vs) + max(v[i] for v in vs)) / 2 for i in range(3)])
    for ob in dst.objects:
        col.objects.link(ob)
        ob.parent = handle
        ob.matrix_world = handle.matrix_world @ RX90.inverted() @ Matrix.Translation(-grip_center)
    # bright, slightly thicker stand-in for the blade so previews read at small sizes
    prev = _collection("Preview_Only")
    proxy = _box("BladeProxy_PreviewOnly", (0.16, 3.3, 0.16), (1.0, 0.42, 0.08, 1), prev)
    proxy.parent = handle
    proxy.matrix_world = handle.matrix_world @ Matrix.Translation((0, 2.225, 0))
    return handle


def _box(name, size, color, col):
    me = bpy.data.meshes.new(name)
    hx, hy, hz = (s / 2 for s in size)
    verts = [(x, y, z) for x in (-hx, hx) for y in (-hy, hy) for z in (-hz, hz)]
    faces = [(0, 1, 3, 2), (4, 6, 7, 5), (0, 4, 5, 1), (2, 3, 7, 6), (0, 2, 6, 4), (1, 5, 7, 3)]
    me.from_pydata(verts, [], faces)
    ob = bpy.data.objects.new(name, me)
    ob.color = color
    col.objects.link(ob)
    return ob


def build_stage():
    col = _collection("Stage_Preview")
    me = bpy.data.meshes.new("Ground")
    s = 8
    me.from_pydata([(-s, -s, 0), (s, -s, 0), (s, s, 0), (-s, s, 0)], [], [(0, 1, 2, 3)])
    g = bpy.data.objects.new("Ground", me)
    g.color = (0.32, 0.36, 0.3, 1)
    col.objects.link(g)
    # target marker 3.5 studs in front (center of the server hitbox)
    me2 = bpy.data.meshes.new("TargetMarker")
    hx, hy, hz = 0.35, 2.5, 0.35
    verts = [(x, y, z) for x in (-hx, hx) for y in (-hy, hy) for z in (-hz, hz)]
    faces = [(0, 1, 3, 2), (4, 6, 7, 5), (0, 4, 5, 1), (2, 3, 7, 6), (0, 2, 6, 4), (1, 5, 7, 3)]
    me2.from_pydata(verts, [], faces)
    t = bpy.data.objects.new("TargetMarker_Dummy", me2)
    t.color = (0.55, 0.42, 0.25, 0.35)
    t.display_type = "WIRE"
    col.objects.link(t)
    t.matrix_world = RX90 @ Matrix.Translation((0, 2.5, -5.5))
    return col


# ---------------------------------------------------------------------------
def _desired_bone_mats(T):
    """Armature-space 4x4 matrices for each bone from Roblox joint Transforms."""
    w = fk(T)
    rest = {}
    out = {}
    for name in BONES:
        R, c = w[name]
        head, tail = _bone_head_tail(name)
        # bone rest in Roblox space: rotation from Y axis to (tail-head), roll 0, Blender convention
        rest_rbx_head = head
        pos = c + R @ (rest_rbx_head - Vector(PARTS[name][0]))
        out[name] = (R, pos)
    return out


def apply_frames(arm, action_name, frames, fps):
    """Write baked Roblox Transforms to a Blender action (one key per frame)."""
    act = bpy.data.actions.new(action_name)
    act.use_fake_user = True
    if arm.animation_data is None:
        arm.animation_data_create()
    arm.animation_data.action = act
    rest = {b.name: b.matrix_local.copy() for b in arm.data.bones}
    for f, T in enumerate(frames):
        des = _desired_bone_mats(T)
        pose_mats = {}
        for name in BONES:
            R, pos = des[name]
            rest_m = rest[name]
            M = Matrix.Translation(to_bl(pos)) @ (RX90_3 @ R @ RX90_3.inverted() @ rest_m.to_3x3()).to_4x4()
            pose_mats[name] = M
            pb = arm.pose.bones[name]
            if name == "HumanoidRootPart":
                basis = rest_m.inverted() @ M
            else:
                par = PARENT[name]
                basis = (pose_mats[par] @ rest[par].inverted() @ rest_m).inverted() @ M
            loc, rot, _ = basis.decompose()
            pb.location = loc
            pb.rotation_quaternion = rot
            pb.keyframe_insert("location", frame=f, group=name)
            pb.keyframe_insert("rotation_quaternion", frame=f, group=name)
    # keep quaternion signs continuous and use linear interpolation between baked frames
    for fc in _fcurves(act):
        for kp in fc.keyframe_points:
            kp.interpolation = "LINEAR"
    act.frame_range = (0, len(frames) - 1)
    return act


def _fcurves(act):
    if hasattr(act, "fcurves") and len(getattr(act, "fcurves", [])) > 0:
        return list(act.fcurves)
    out = []
    for layer in getattr(act, "layers", []):
        for strip in layer.strips:
            for bag in strip.channelbags:
                out.extend(bag.fcurves)
    return out


def tip_trail(name, frames):
    pts = []
    for T in frames:
        tip, _, _, _ = tip_and_pommel(fk(T))
        pts.append(to_bl(tip))
    cu = bpy.data.curves.new("TipTrail_" + name, "CURVE")
    cu.dimensions = "3D"
    sp = cu.splines.new("POLY")
    sp.points.add(len(pts) - 1)
    for p, co in zip(sp.points, pts):
        p.co = (co.x, co.y, co.z, 1)
    cu.bevel_depth = 0.03
    ob = bpy.data.objects.new("TipTrail_" + name, cu)
    ob.color = (1.0, 0.45, 0.1, 1)
    bpy.data.collections["Stage_Preview"].objects.link(ob)
    return ob


# ---------------------------------------------------------------------------
def setup_render(res=360):
    sc = bpy.context.scene
    sc.render.engine = "BLENDER_WORKBENCH"
    sc.display.shading.light = "STUDIO"
    sc.display.shading.color_type = "OBJECT"
    sc.display.shading.show_shadows = True
    sc.display.shading.show_cavity = True
    sc.display.shading.show_object_outline = True
    sc.render.resolution_x = res
    sc.render.resolution_y = res
    sc.render.film_transparent = False
    sc.world = bpy.data.worlds.new("World") if sc.world is None else sc.world
    sc.render.image_settings.file_format = "PNG"


def add_camera(name, loc_rbx, look_rbx, ortho=None, lens=35):
    cam_d = bpy.data.cameras.new(name)
    if ortho:
        cam_d.type = "ORTHO"
        cam_d.ortho_scale = ortho
    else:
        cam_d.lens = lens
    cam = bpy.data.objects.new(name, cam_d)
    bpy.context.scene.collection.objects.link(cam)
    loc = to_bl(loc_rbx)
    cam.location = loc
    direction = to_bl(look_rbx) - loc
    cam.rotation_euler = direction.to_track_quat("-Z", "Y").to_euler()
    return cam


def render_frames(arm, action, frames_idx, cam, out_dir, prefix):
    sc = bpy.context.scene
    sc.camera = cam
    arm.animation_data.action = action
    os.makedirs(out_dir, exist_ok=True)
    paths = []
    for f in frames_idx:
        sc.frame_set(f)
        p = os.path.join(out_dir, f"{prefix}_{f:03d}.png")
        sc.render.filepath = p
        bpy.ops.render.render(write_still=True)
        paths.append(p)
    return paths


# ---------------------------------------------------------------------------
REST_FRAME = -10  # outside every clip; the export copy holds the R15 rest pose here


def export_fbx(arm, action, path):
    """Armature only, one action, baked every frame. Axis/scale match StarterLongsword.fbx.

    Blender writes each bone's default (Lcl) transform from the pose at the current frame
    when there is no skinned mesh. A temporary copy of the action gets a rest-pose key at
    REST_FRAME and the export starts from that frame, so the FBX skeleton is the true R15 rest
    pose and only frames 0..N are baked as animation.
    """
    bpy.ops.object.select_all(action="DESELECT")
    arm.select_set(True)
    bpy.context.view_layer.objects.active = arm
    start, end = (int(v) for v in action.frame_range)
    tmp = action.copy()
    tmp.name = action.name + "_fbx"
    arm.animation_data.action = tmp
    for pb in arm.pose.bones:
        pb.location = (0.0, 0.0, 0.0)
        pb.rotation_quaternion = (1.0, 0.0, 0.0, 0.0)
        pb.keyframe_insert("location", frame=REST_FRAME, group=pb.name)
        pb.keyframe_insert("rotation_quaternion", frame=REST_FRAME, group=pb.name)
    sc = bpy.context.scene
    sc.frame_start, sc.frame_end = start, end
    sc.frame_set(REST_FRAME)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    try:
        bpy.ops.export_scene.fbx(
            filepath=path,
            use_selection=True,
            object_types={"ARMATURE"},
            apply_unit_scale=True,
            apply_scale_options="FBX_SCALE_ALL",
            axis_forward="-Z",
            axis_up="Y",
            add_leaf_bones=False,
            primary_bone_axis="Y",
            secondary_bone_axis="X",
            armature_nodetype="NULL",
            bake_anim=True,
            bake_anim_use_all_bones=True,
            bake_anim_use_nla_strips=False,
            bake_anim_use_all_actions=False,
            bake_anim_force_startend_keying=True,
            bake_anim_step=1.0,
            bake_anim_simplify_factor=0.0,
        )
    finally:
        arm.animation_data.action = action
        bpy.data.actions.remove(tmp)
        sc.frame_set(start)
    return path
