"""Blind Vow - verify the exported sword animations match the source data.

Checks, for every animation:
  1. the .blend action reproduces the Roblox joint Transforms (Blender pose == rig math)
  2. the FBX re-imports into an empty Blender scene with the same bone motion
  3. the .rbxmx parses and holds the same Transforms, keyframe count and markers
Run from the repo root: python tools/animations/blender/bv_verify.py --repo .
"""
import argparse, math, os, re, sys, xml.etree.ElementTree as ET
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bpy
from mathutils import Matrix, Vector
import bv_poses, bv_sample
from bv_rig import fk, I3
from bv_blender import RX90_3, BONES

ORDER = ["Sword_CombatIdle", "Sword_M1_01", "Sword_M1_02", "Sword_M1_03", "Sword_M1_04"]


def part_rots_from_armature(arm, rest):
    """Roblox-space world rotation of every part from an evaluated Blender armature."""
    out = {}
    aw = arm.matrix_world.to_3x3()
    for name in BONES:
        pb = arm.pose.bones.get(name)
        if pb is None:
            continue
        M = aw @ pb.matrix.to_3x3() @ rest[name].inverted()
        out[name] = RX90_3.inverted() @ M @ RX90_3
    return out


def max_err(a, b):
    worst = 0.0
    for k in a:
        if k in b:
            worst = max(worst, math.degrees(a[k].to_quaternion().rotation_difference(b[k].to_quaternion()).angle))
    return worst


def _ang(A, B):
    qa = A.to_3x3().normalized().to_quaternion()
    qb = B.to_3x3().normalized().to_quaternion()
    return math.degrees(qa.rotation_difference(qb).angle)


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--repo", default=".")
    args = ap.parse_args(sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else sys.argv[1:])
    repo = os.path.abspath(args.repo)
    clips = bv_poses.build_clips()
    baked = {n: bv_sample.bake_clip(clips[n])[0] for n in ORDER}
    ok = True
    # 1. blend
    bpy.ops.wm.open_mainfile(filepath=os.path.join(repo, "assets/blender/animations/SwordCombat.blend"))
    arm = bpy.data.objects["BV_R15_Rig"]
    rest = {b.name: (arm.matrix_world.to_3x3() @ b.matrix_local.to_3x3()) for b in arm.data.bones}
    print("blend actions:", sorted(a.name for a in bpy.data.actions))
    for n in ORDER:
        arm.animation_data.action = bpy.data.actions[n]
        worst = 0.0
        for f, T in enumerate(baked[n]):
            bpy.context.scene.frame_set(f)
            w = fk(T)
            got = part_rots_from_armature(arm, rest)
            worst = max(worst, max_err({k: w[k][0] for k in got}, got))
        print(f"  [blend] {n}: frames {len(baked[n])}, max rotation error {worst:.4f} deg")
        ok &= worst < 0.05
    # 2. fbx: re-import and compare posed bone matrices with the .blend, plus the rest pose
    blend_path = os.path.join(repo, "assets/blender/animations/SwordCombat.blend")
    for n in ORDER:
        bpy.ops.wm.open_mainfile(filepath=blend_path)
        a0 = bpy.data.objects["BV_R15_Rig"]
        a0.animation_data.action = bpy.data.actions[n]
        rest0 = {b.name: a0.matrix_world @ b.matrix_local for b in a0.data.bones}
        orig = []
        for f in range(len(baked[n])):
            bpy.context.scene.frame_set(f)
            orig.append({pb.name: a0.matrix_world @ pb.matrix for pb in a0.pose.bones})
        path = os.path.join(repo, "assets/roblox/animations_fbx", n + ".fbx")
        size = os.path.getsize(path)
        bpy.ops.wm.read_factory_settings(use_empty=True)
        bpy.ops.import_scene.fbx(filepath=path)
        a = [o for o in bpy.context.scene.objects if o.type == "ARMATURE"][0]
        f0, f1 = (int(v) for v in a.animation_data.action.frame_range)
        rest_err = max(_ang(rest0[b.name], a.matrix_world @ b.matrix_local) for b in a.data.bones)
        rest_pos = max((rest0[b.name].translation - (a.matrix_world @ b.matrix_local).translation).length for b in a.data.bones)
        rot_err = pos_err = 0.0
        for i in range(f1 - f0 + 1):
            bpy.context.scene.frame_set(f0 + i)
            for pb in a.pose.bones:
                M = a.matrix_world @ pb.matrix
                rot_err = max(rot_err, _ang(orig[min(i, len(orig) - 1)][pb.name], M))
                pos_err = max(pos_err, (orig[min(i, len(orig) - 1)][pb.name].translation - M.translation).length)
        nframes = f1 - f0 + 1
        print(f"  [fbx]   {n}: {size} bytes, bones {len(a.data.bones)}, frames {nframes}, rest pose diff {rest_err:.4f} deg / {rest_pos:.4f}, motion diff {rot_err:.4f} deg / {pos_err:.4f}")
        ok &= size > 0 and len(a.data.bones) == 16 and nframes == len(baked[n]) and rest_err < 0.05 and rot_err < 0.05 and pos_err < 0.001
    # 3. rbxmx
    for n in ORDER:
        path = os.path.join(repo, "assets/roblox/animations", n + ".rbxmx")
        root = ET.parse(path).getroot()
        seq = root.find("Item")
        kfs = [it for it in seq.findall("Item") if it.get("class") == "Keyframe"]
        markers = []
        worst = 0.0
        for idx, kf in enumerate(kfs):
            T = {}
            for pose in kf.iter("Item"):
                if pose.get("class") == "KeyframeMarker":
                    markers.append((pose.find("Properties/string[@name='Name']").text, round(float(kf.find("Properties/float[@name='Time']").text) * 30)))
                if pose.get("class") != "Pose":
                    continue
                props = pose.find("Properties")
                nm = props.find("string[@name='Name']").text
                cf = props.find("CoordinateFrame")
                v = {c.tag: float(c.text) for c in cf}
                R = Matrix(((v["R00"], v["R01"], v["R02"]), (v["R10"], v["R11"], v["R12"]), (v["R20"], v["R21"], v["R22"])))
                T[nm] = (R, Vector((v["X"], v["Y"], v["Z"])))
            if "fk_keys" in clips[n]:
                ref = clips[n]["fk_keys"][idx][1]
            else:
                ref = baked[n][idx]
            for j, (R, p) in ref.items():
                if j in T:
                    worst = max(worst, math.degrees(R.to_quaternion().rotation_difference(T[j][0].to_quaternion()).angle))
        prio = seq.find("Properties/token[@name='Priority']").text
        loop = seq.find("Properties/bool[@name='Loop']").text
        print(f"  [rbxmx] {n}: {os.path.getsize(path)} bytes, keyframes {len(kfs)}, poses/keyframe {sum(1 for x in kfs[0].iter('Item') if x.get('class')=='Pose')}, priority {prio}, loop {loop}, markers {markers}, max rotation error {worst:.4f} deg")
        ok &= worst < 0.01
    print("ALL CHECKS PASSED" if ok else "SOME CHECKS FAILED")


if __name__ == "__main__":
    main()
