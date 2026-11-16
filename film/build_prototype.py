import bpy
import math
from mathutils import Vector

# Clear scene
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)

# Render settings
scene = bpy.context.scene
scene.render.engine = 'BLENDER_EEVEE_NEXT'
scene.render.resolution_x = 1920
scene.render.resolution_y = 1080
scene.render.resolution_percentage = 100
scene.render.fps = 24
scene.frame_end = 1440

# Materials
def material(name, color, metallic=0):
    mat = bpy.data.materials.new(name)
    mat.diffuse_color = (*color, 1)
    mat.metallic = metallic
    return mat

ocean_mat = material("Deep blue ocean", (0.015, 0.12, 0.28))
seaweed_mat = material("Sargassum seaweed", (0.28, 0.22, 0.035))
skin_mat = material("Warm skin", (0.72, 0.42, 0.25))
shirt_mat = material("Explorer blue shirt", (0.04, 0.18, 0.65))
shirt2_mat = material("Explorer orange shirt", (0.9, 0.25, 0.04))
white_mat = material("White", (0.9, 0.9, 0.9))
black_mat = material("Black", (0.01, 0.01, 0.01))

# Ocean
bpy.ops.mesh.primitive_plane_add(size=200, location=(0, 0, 0))
ocean = bpy.context.object
ocean.name = "Sargasso Ocean"
ocean.data.materials.append(ocean_mat)

# Seaweed
for i in range(35):
    x = (i % 7 - 3) * 2.2
    y = (i // 7 - 2) * 2.0
    bpy.ops.mesh.primitive_uv_sphere_add(
        segments=12, ring_count=8,
        radius=0.35,
        location=(x, y, 0.35)
    )
    weed = bpy.context.object
    weed.name = "Floating Sargassum"
    weed.scale = (1.4, 0.25, 0.2)
    weed.data.materials.append(seaweed_mat)

# Character creator
def make_character(name, x, y, shirt):
    # Body
    bpy.ops.mesh.primitive_cylinder_add(
        vertices=24, radius=0.45, depth=1.4,
        location=(x, y, 1.15)
    )
    body = bpy.context.object
    body.name = name + " Body"
    body.data.materials.append(shirt)

    # Head
    bpy.ops.mesh.primitive_uv_sphere_add(
        segments=24, ring_count=16,
        radius=0.48, location=(x, y, 2.25)
    )
    head = bpy.context.object
    head.name = name + " Head"
    head.data.materials.append(skin_mat)

    # Eyes
    for dx in [-0.16, 0.16]:
        bpy.ops.mesh.primitive_uv_sphere_add(
            segments=16, ring_count=8,
            radius=0.055,
            location=(x + dx, y - 0.42, 2.32)
        )
        eye = bpy.context.object
        eye.name = name + " Eye"
        eye.data.materials.append(black_mat)

    # Smile
    bpy.ops.mesh.primitive_uv_sphere_add(
        segments=16, ring_count=8,
        radius=0.07,
        location=(x, y - 0.46, 2.12)
    )
    mouth = bpy.context.object
    mouth.name = name + " Smile"
    mouth.scale = (1.5, 0.35, 0.35)
    mouth.data.materials.append(black_mat)

    # Arms
    for side in [-1, 1]:
        bpy.ops.mesh.primitive_cylinder_add(
            vertices=16, radius=0.12, depth=1.0,
            location=(x + side * 0.58, y, 1.35)
        )
        arm = bpy.context.object
        arm.name = name + " Arm"
        arm.rotation_euler[1] = side * math.radians(25)
        arm.data.materials.append(shirt)

# Two explorers
make_character("Ayan the smart explorer", -1.2, -4, shirt_mat)
make_character("Dani the confident explorer", 1.2, -4, shirt2_mat)

# Lighting
bpy.ops.object.light_add(type='AREA', location=(0, -4, 10))
light = bpy.context.object
light.data.energy = 1800
light.data.shape = 'DISK'
light.data.size = 8

# Camera
bpy.ops.object.camera_add(location=(0, -12, 6))
camera = bpy.context.object
camera.rotation_euler = (math.radians(68), 0, 0)
scene.camera = camera

# World
scene.world.color = (0.08, 0.12, 0.2)

# Camera movement
camera.location = (0, -15, 7)
camera.keyframe_insert(data_path="location", frame=1)
camera.location = (0, -10, 5)
camera.keyframe_insert(data_path="location", frame=1440)

# Output
scene.render.image_settings.file_format = 'PNG'
scene.render.filepath = "//sargasso_frame"

# Save Blender project
bpy.ops.wm.save_as_mainfile(filepath="//sargasso_prototype.blend")

print("Sargasso Sea prototype created!")
