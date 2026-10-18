"""Blind Vow - Sword combat animation set (Sword_CombatIdle, Sword_M1_01..04).

Rebuilds everything from the key poses in bv_poses.py:
  assets/blender/animations/SwordCombat.blend        editable source (actions, rig, sword)
  assets/roblox/animations_fbx/Sword_*.fbx           FBX per animation (R15 skeleton)
  assets/roblox/animations/Sword_*.rbxmx             KeyframeSequence per animation
  docs/animations/sword_combat_report.json           automatic quality checks

Run from the repository root, either with Blender:
  blender --background --python tools/animations/blender/bv_sword_combat.py -- --repo .
or with the Blender Python module (pip install bpy==5.2.2):
  python tools/animations/blender/bv_sword_combat.py --repo .
Add --render to also write preview images to --preview-dir.
"""

import argparse
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import bpy  # noqa: E402

import bv_blender  # noqa: E402
import bv_poses  # noqa: E402
import bv_roblox  # noqa: E402
import bv_sample  # noqa: E402

ORDER = ["Sword_CombatIdle", "Sword_M1_01", "Sword_M1_02", "Sword_M1_03", "Sword_M1_04"]


def parse_args():
    argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else sys.argv[1:]
    ap = argparse.ArgumentParser()
    here = os.path.dirname(os.path.abspath(__file__))
    ap.add_argument("--repo", default=os.path.abspath(os.path.join(here, "..", "..", "..")))
    ap.add_argument("--render", action="store_true")
    ap.add_argument("--preview-dir", default=None)
    return ap.parse_args(argv)


def main():
    args = parse_args()
    repo = os.path.abspath(args.repo)
    fps = bv_poses.FPS
    clips = bv_poses.build_clips()

    baked, reports = {}, []
    for name in ORDER:
        frames, diags = bv_sample.bake_clip(clips[name])
        baked[name] = frames
        reports.append(bv_sample.check_clip(name, frames, diags))
    chain = [ORDER[0], ORDER[1], ORDER[2], ORDER[3], ORDER[4], ORDER[0]]
    cont = {f"{a}->{b}": round(bv_sample.continuity(baked[a], baked[b]), 4) for a, b in zip(chain, chain[1:])}

    # --- Blender scene ---
    bv_blender.new_scene(fps)
    arm = bv_blender.build_rig()
    bv_blender.attach_sword(arm, os.path.join(repo, "assets", "blender", "weapons", "StarterLongsword.blend"))
    bv_blender.build_stage()
    actions = {}
    for name in ORDER:
        actions[name] = bv_blender.apply_frames(arm, name, baked[name], fps)
        if name != "Sword_CombatIdle":
            trail = bv_blender.tip_trail(name, baked[name])
            trail.hide_render = True
    arm.animation_data.action = actions["Sword_CombatIdle"]

    # --- Roblox KeyframeSequences ---
    rbx_dir = os.path.join(repo, "assets", "roblox", "animations")
    os.makedirs(rbx_dir, exist_ok=True)
    outputs = {}
    for name in ORDER:
        clip = clips[name]
        path = os.path.join(rbx_dir, name + ".rbxmx")
        if "fk_keys" in clip:
            # Same 3-key cubic loop as the Studio-tested SwordReadyIdle, right arm included.
            keys = [(f / fps, T) for f, T in clip["fk_keys"]]
            bv_roblox.write_keyframe_sequence(path, name, keys, clip["loop"], clip["priority"],
                                              easing="Cubic", direction="InOut")
        else:
            keys = [(f / fps, T) for f, T in enumerate(baked[name])]
            markers = {m: f / fps for m, f in clip["markers"].items()}
            bv_roblox.write_keyframe_sequence(path, name, keys, clip["loop"], clip["priority"], markers)
        outputs[name] = {"rbxmx": os.path.relpath(path, repo)}

    # --- FBX ---
    fbx_dir = os.path.join(repo, "assets", "roblox", "animations_fbx")
    for name in ORDER:
        path = os.path.join(fbx_dir, name + ".fbx")
        bv_blender.export_fbx(arm, actions[name], path)
        outputs[name]["fbx"] = os.path.relpath(path, repo)

    # --- editable .blend (texture paths made relative to the new file) ---
    blend_path = os.path.join(repo, "assets", "blender", "animations", "SwordCombat.blend")
    os.makedirs(os.path.dirname(blend_path), exist_ok=True)
    src_tex = os.path.join(repo, "assets", "blender", "weapons")
    for img in bpy.data.images:
        if img.filepath.startswith("//"):
            img.filepath = os.path.normpath(os.path.join(src_tex, img.filepath[2:]))
    arm.animation_data.action = actions["Sword_CombatIdle"]
    bpy.context.scene.frame_start, bpy.context.scene.frame_end = 0, 96
    bpy.ops.wm.save_as_mainfile(filepath=blend_path)
    bpy.ops.file.make_paths_relative()
    bpy.ops.wm.save_as_mainfile(filepath=blend_path)
    if os.path.exists(blend_path + "1"):  # Blender's automatic backup copy, not needed in the repo
        os.remove(blend_path + "1")

    # --- report ---
    info = {}
    for name in ORDER:
        clip = clips[name]
        n = clip["length"]
        info[name] = {
            "fps": fps,
            "frames": f"0-{n}",
            "duration_s": round(n / fps, 3),
            "loop": clip["loop"],
            "priority": {2: "Action", 3: "Action2"}[clip["priority"]],
            "markers": {m: {"frame": f, "time_s": round(f / fps, 3)} for m, f in clip["markers"].items()},
            **outputs[name],
        }
    report = {"animations": info, "checks": reports, "continuity_deg": cont,
              "blend": os.path.relpath(blend_path, repo),
              "images": [i.filepath for i in bpy.data.images]}
    doc_dir = os.path.join(repo, "docs", "animations")
    os.makedirs(doc_dir, exist_ok=True)
    with open(os.path.join(doc_dir, "sword_combat_report.json"), "w", encoding="utf-8") as fh:
        json.dump(report, fh, indent=2, ensure_ascii=False)
    print(json.dumps({"continuity_deg": cont, "issues": {r["name"]: r["issues"] for r in reports}}, indent=1))

    if args.render:
        render_previews(arm, actions, args.preview_dir or os.path.join(repo, "preview"))


def render_previews(arm, actions, out):
    bv_blender.setup_render(360)
    cams = {
        "back": bv_blender.add_camera("Cam_Back34", (4.8, 6.3, 8.8), (0.2, 2.7, -1.6), lens=30),
        "front": bv_blender.add_camera("Cam_Front34", (7.5, 5.0, -8.0), (0.0, 2.6, -1.2), lens=30),
        "side": bv_blender.add_camera("Cam_Side", (-12.0, 3.0, -1.5), (0.0, 3.0, -1.5), ortho=9.5),
        "top": bv_blender.add_camera("Cam_Top", (0.0, 20.0, -1.0), (0.0, 0.0, -0.99), ortho=12.5),
    }
    for name, act in actions.items():
        n = int(act.frame_range[1])
        frames = list(range(0, n + 1)) if name != "Sword_CombatIdle" else [0, 24, 48, 72]
        for view in ("back", "front", "side"):
            bv_blender.render_frames(arm, act, frames, cams[view], os.path.join(out, name), view)
        if name != "Sword_CombatIdle":
            trail = bpy.data.objects["TipTrail_" + name]
            trail.hide_render = False
            bv_blender.render_frames(arm, act, [0], cams["top"], os.path.join(out, name), "toptrail")
            bv_blender.render_frames(arm, act, [0], cams["back"], os.path.join(out, name), "backtrail")
            trail.hide_render = True


if __name__ == "__main__":
    main()
