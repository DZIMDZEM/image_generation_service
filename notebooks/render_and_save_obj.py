import os

import trimesh
from PIL import Image
from trimesh.geometry import align_vectors


def auto_camera_setup(mesh):
    # Calculate the bounding box of the mesh
    bbox = mesh.bounding_box
    center = bbox.centroid
    extents = bbox.extents
    max_dim = max(extents)

    # Set the camera to look at the center of the mesh
    # Distance depends on the maximum dimension of the bounding box
    distance = max_dim * 3  # Adjust this factor based on desired framing
    camera_pose = np.array([
        [1, 0, 0, 0],
        [0, 1, 0, 0],
        [0, 0, 1, distance],
        [0, 0, 0, 1]
    ])

    return camera_pose, center


def auto_camera_setup(mesh, vertical_angle_degrees=-30):
    # Calculate the bounding box of the mesh
    bbox = mesh.bounding_box
    center = bbox.centroid
    extents = bbox.extents
    max_dim = max(extents)

    # Convert vertical angle to radians
    vertical_angle = np.radians(vertical_angle_degrees)

    # Set the camera distance based on the object size
    distance = max_dim * 2.5  # Adjust multiplier based on desired framing

    # Calculate camera's translation
    camera_translation = np.array([0, 0, distance])

    # Rotation matrix for tilting the camera
    # Rotating around the X-axis
    rotation_matrix = np.array([
        [1, 0, 0, 0],
        [0, np.cos(vertical_angle), -np.sin(vertical_angle), 0],
        [0, np.sin(vertical_angle), np.cos(vertical_angle), 0],
        [0, 0, 0, 1]
    ])

    # Translation matrix to move the camera back
    translation_matrix = np.array([
        [1, 0, 0, 0],
        [0, 1, 0, 1.5],
        [0, 0, 1, -1 - center[2] + distance],  # Move camera to 'distance' along Z-axis from the center
        [0, 0, 0, 1]
    ])

    # Combine rotation and translation into a single transformation matrix
    # First apply rotation, then translation
    camera_pose = rotation_matrix @ translation_matrix

    return camera_pose, center


import numpy as np
import pyrender


def setup_lighting_with_directional(scene, intensity=2.0, light_direction=np.array([0, -1, -1])):
    # Directional light
    directional_light = pyrender.DirectionalLight(color=np.ones(3), intensity=intensity)
    light_node = pyrender.Node(light=directional_light, matrix=np.eye(4))
    light_node.matrix[:3, :3] = align_vectors([0, 0, 1], light_direction)[:3, :3]

    scene.add_node(light_node)
    return scene


# Generate a filename using a specified name and angle
def generate_filename(name, angle, extension):
    if name:
        return f'{name}_angle_{int(angle):03d}.{extension}'
    else:
        return f'unnamed_angle_{int(angle):03d}.{extension}'


def render_and_save_obj(obj_file, output_folder, num_images=3, name=''):
    # Load the mesh
    mesh = trimesh.load(obj_file, force='mesh')
    scene = pyrender.Scene()

    # Create a mesh node from trimesh and add to scene
    mesh_node = pyrender.Node(mesh=pyrender.Mesh.from_trimesh(mesh), matrix=np.eye(4))
    scene.add_node(mesh_node)

    # Setup camera and lighting
    camera = pyrender.PerspectiveCamera(yfov=np.pi / 5.0, aspectRatio=1.0)
    camera_pose, center = auto_camera_setup(mesh)
    scene.add(camera, pose=camera_pose)
    scene = setup_lighting_with_directional(scene)

    # Offscreen rendering setup
    r = pyrender.OffscreenRenderer(224, 224)

    for angle in np.linspace(0, 360, num_images, endpoint=False):
        # Calculate the rotation transformation matrix
        rotation_matrix = trimesh.transformations.rotation_matrix(
            np.radians(angle), [0, 1, 0], mesh.centroid)

        # Apply rotation to the node
        scene.set_pose(mesh_node, pose=rotation_matrix)

        # Render the scene
        color, _ = r.render(scene)

        # Save the image
        image = Image.fromarray(color)
        image_filename = generate_filename(name, angle, 'png')
        image.save(os.path.join(output_folder, 'images', image_filename))

        # if name:
        #     image_filename = f'{os.path.splitext(os.path.basename(obj_file))[0]}_angle_{int(angle):03d}_{name}.png'
        # else:
        #     image_filename = f'{os.path.splitext(os.path.basename(obj_file))[0]}_angle_{int(angle):03d}.png'
        # image.save(os.path.join(output_folder, 'images', image_filename))

        # Save the rotated mesh
        rotated_mesh = mesh.copy()
        rotated_mesh.apply_transform(rotation_matrix)
        obj_filename = generate_filename(name, angle, 'obj')
        rotated_mesh.export(os.path.join(output_folder, 'objs', obj_filename))

        # if name:
        #     obj_filename = f'{os.path.splitext(os.path.basename(obj_file))[0]}_angle_{int(angle):03d}_{name}.obj'
        # else:
        #     obj_filename = f'{os.path.splitext(os.path.basename(obj_file))[0]}_angle_{int(angle):03d}.obj'
        # rotated_mesh.export(os.path.join(output_folder, 'objs', obj_filename))

    # Clean up rendering objects
    r.delete()


def process_all_obj_files(source_folder, output_folder, num_images=10):
    # Ensure the output folder exists
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # List all files in the source folder
    for i, file in enumerate(os.listdir(source_folder)):
        if file.lower().endswith('.obj'):
            obj_file_path = os.path.join(source_folder, file)
            print(f"Processing {obj_file_path}...")
            object_name = f'obj_{i}_'

            # Call the existing rendering function for each .obj file
            try:
                render_and_save_obj(obj_file_path, output_folder, num_images, name=object_name)
            except ModuleNotFoundError:
                continue


# Example usage
source_folder = r'C:\Users\dzmit\Downloads\3d-objects\2024-05-09_state\init_3d'
output_folder = r'C:\Users\dzmit\Downloads\3d-objects\2024-05-14_state'

# Ensure subfolders for images and objs exist
os.makedirs(os.path.join(output_folder, 'images'), exist_ok=True)
os.makedirs(os.path.join(output_folder, 'objs'), exist_ok=True)

process_all_obj_files(source_folder, output_folder, num_images=16)
