import bpy
from os.path import join, basename
import sys
import pathlib

# print(bpy.data.filepath)
home = pathlib.Path.home()

if sys.platform == "win32":
    home = home / "AppData/Roaming"
elif sys.platform == "linux":
    home = home / ".local/share"
elif sys.platform == "darwin":
    home = home / "Library/Application Support"

C = bpy.context

scene = C.scene
render = scene.render
render.engine = 'BLENDER_WORKBENCH'
render.resolution_x = 128
render.resolution_y = 128
render.film_transparent = True

scene.display.render_aa = 'FXAA'  # OFF
scene.display.shading.color_type = 'RANDOM'

def override(ctx):
    for window in ctx.window_manager.windows:
        for area in window.screen.areas:
            if area.type == 'VIEW_3D':
                for region in area.regions:
                    if region.type == 'WINDOW':
                        return {
                            'window': window,
                            'area': area,
                            'region': region
                        }
    return None


context = override(C)
if context:
    if not C.scene.camera:
        cam = bpy.data.cameras.new('ThumbnailCamera')
        cam_obj = bpy.data.objects.new('ThumbnailCamera', cam)
        C.scene.collection.objects.link(cam_obj)
        C.scene.camera = cam_obj
    try:
        bpy.ops.view3d.camera_to_view(context)
    except RuntimeError:
        pass
    # bpy.ops.view3d.camera_to_view_selected(context)


'''
space_data = None
for window in C.window_manager.windows:
    for area in window.screen.areas:
        if area.type == 'VIEW_3D':
            for space in area.spaces:
                if space.type == 'VIEW_3D':
                    space_data = space
                    break
            break

if space_data:
    space_data.shading.type = 'SOLID'
    space_data.shading.color_type = 'RANDOM'
    space_data.overlay.show_overlays = False
    bpy.ops.render.opengl()
else:
    bpy.ops.render.render()
'''

bpy.ops.render.render()

img = bpy.data.images.get('Render Result', None)
if img:
    thumbnails = home / "BlenderHub" / "thumbnails"
    path = join(str(thumbnails), basename(bpy.data.filepath).replace('.blend', '.png'))
    # print(path)
    img.save_render(path, scene=C.scene)
