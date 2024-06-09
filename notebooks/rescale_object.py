import os

import numpy as np
import trimesh


def generate_filename(name, modifier, extension):
    if name:
        return f'{name}_angle_{modifier}.{extension}'
    else:
        return f'unnamed_angle_{modifier}.{extension}'


def voxelise_and_save_obj(obj_file, output_folder, grid_size=(13, 13, 15), name=''):
    # Load the mesh
    mesh = trimesh.load(obj_file, force='mesh')

    # Calculate the pitch for voxelization
    extents = mesh.extents
    pitch = max(extents) / (max(grid_size) - 1)  # Adjusted to prevent exceeding the grid size

    # Voxelization
    voxels = mesh.voxelized(pitch=pitch)

    # Get the voxel grid matrix and ensure it matches the desired dimensions
    matrix = voxels.matrix
    if matrix.shape != grid_size:
        trimmed = np.zeros(grid_size, dtype=bool)  # Initialize a zero grid of the target size
        # Calculate the regions to copy from the original matrix to the new grid
        slice_to_use = tuple(slice(0, min(gs, ms)) for gs, ms in zip(grid_size, matrix.shape))
        target_slice = tuple(slice(0, s.stop) for s in slice_to_use)
        trimmed[target_slice] = matrix[slice_to_use]

        matrix = trimmed  # Replace the original matrix with the trimmed/padded matrix

    # Save the voxel data
    voxel_filename = generate_filename(name, 'voxel', 'npy')
    np.save(os.path.join(output_folder, voxel_filename), matrix)

    # Save the mesh
    # voxel_mesh = trimesh.voxel.ops.matrix_to_marching_cubes(matrix, pitch=pitch)
    # obj_filename = generate_filename(name, 'voxel', 'obj')
    # voxel_mesh.export(os.path.join(output_folder, obj_filename))


# Example usage of the function
# obj_file_path = r'C:\Users\dzmit\Downloads\3d-objects\2024-05-09_state\in\obj_59__angle_000.obj'
# output_folder_path = r'C:\Users\dzmit\Downloads\3d-objects\2024-05-09_state\out'
#
# voxelise_and_save_obj(obj_file_path, output_folder_path, name='example_name')


# Example usage
source_folder = r'C:\Users\dzmit\Downloads\3d-objects\2024-05-14_state\objs'
output_folder = r'C:\Users\dzmit\Downloads\3d-objects\2024-05-14_state\tarin_3d\scaled'


def process_all_obj_files(source_folder, output_folder):
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
                voxelise_and_save_obj(obj_file_path, output_folder, name=str(file))
            except ModuleNotFoundError:
                continue


# Ensure subfolders for images and objs exist
os.makedirs(os.path.join(output_folder, 'scaled'), exist_ok=True)

process_all_obj_files(source_folder, output_folder)
