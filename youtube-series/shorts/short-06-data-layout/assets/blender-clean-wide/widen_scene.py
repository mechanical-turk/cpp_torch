"""Extend the existing camera by exactly 100 pixels per side, without scaling content."""
import bpy, json
from pathlib import Path
from mathutils import Vector
from bpy_extras.object_utils import world_to_camera_view

root = Path('/Users/keremkazan/Documents/Codex/2026-09-05/go-t')
out = root / 'outputs/short-06-blender-wide'
s = bpy.context.scene
old_w, old_h = s.render.resolution_x, s.render.resolution_y
assert (old_w, old_h) == (2160, 2352)
camera = s.camera.data
old_scale = camera.ortho_scale
old_height = max(v.y for v in camera.view_frame(scene=s)) * 2
points = []
for f in range(1, 457):
    s.frame_set(f)
    for o in s.objects:
        if o.type in {'MESH', 'FONT', 'CURVE'} and not o.hide_render:
            for corner in o.bound_box:
                pos = o.matrix_world @ Vector(corner)
                p = world_to_camera_view(s, s.camera, pos)
                points.append((pos.copy(), p.x * old_w, p.y * old_h))
s.render.resolution_x = old_w + 200
new_height = max(v.y for v in camera.view_frame(scene=s)) * 2
camera.ortho_scale *= old_height / new_height
error = 0.0
for pos, x, y in points:
    p = world_to_camera_view(s, s.camera, pos)
    error = max(error, abs(p.x * s.render.resolution_x - x - 100), abs(p.y * old_h - y))
assert error < 0.02, error
s.render.engine = 'BLENDER_EEVEE'
s.eevee.taa_render_samples = 32
s.render.resolution_percentage = 100
s.render.use_border = False
s.render.image_settings.file_format = 'PNG'
s.render.image_settings.color_mode = 'RGB'
s['README'] = 'Wide derivative of simplified v2: 2360x2352, 100 extra background pixels on each side. All model, code, light, material and animation data retained; original content has unchanged pixel scale. 24 fps, 19 seconds, silent.'
s.frame_set(1)
report = {'source_resolution': [old_w, old_h], 'resolution': [s.render.resolution_x, old_h], 'added_left_px': 100, 'added_right_px': 100, 'old_ortho_scale': old_scale, 'new_ortho_scale': camera.ortho_scale, 'projected_points_checked': len(points), 'maximum_projection_error_px': error, 'duration_seconds': 19, 'fps': 24, 'frames': 456, 'background': 'Original Blender stage, materials and studio lighting; extended camera view.'}
(out / 'camera-verification.json').write_text(json.dumps(report, indent=2))
if bpy.data.texts.get('About this scene'):
    bpy.data.texts['About this scene'].clear()
    bpy.data.texts['About this scene'].write(s['README'])
bpy.ops.wm.save_as_mainfile(filepath=str(out / 'cpp-data-layout-clean-wide.blend'))
s.render.filepath = str(root / 'work/short-06-blender-wide/test-frame.png')
bpy.ops.render.render(write_still=True)
print('WIDENED', json.dumps(report), flush=True)
