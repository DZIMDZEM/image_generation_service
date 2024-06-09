import os
import matplotlib.pyplot as plt
from PIL import Image

def create_image_grid(directory, output_filename='image_grid.png', n_images=25, grid_size=(5, 5)):
    """
    Reads images from a specified directory, displays them in a grid, and saves the grid as an image.

    Parameters:
    - directory: Path to the directory containing the images.
    - output_filename: Name of the file to save the grid image.
    - n_images: Number of images to include in the grid.
    - grid_size: Tuple specifying the grid size (rows, columns).
    """
    if not os.path.exists(directory):
        raise ValueError(f"Directory {directory} does not exist")

    # Get image files from the directory
    image_files = [os.path.join(directory, file) for file in os.listdir(directory) if file.lower().endswith(('.png', '.jpg', '.jpeg'))]
    if len(image_files) < n_images:
        raise ValueError(f"Directory contains fewer than {n_images} images")

    # Select the first n_images files
    selected_files = image_files[:n_images]

    # Create a figure with subplots in a grid
    fig, axes = plt.subplots(*grid_size, figsize=(10, 10))
    axes = axes.flatten()

    for ax, img_path in zip(axes, selected_files):
        # Open the image and plot it on the axis
        with Image.open(img_path) as img:
            ax.imshow(img)
            ax.axis('off')  # Hide axes for cleaner look

    plt.tight_layout()
    plt.savefig(output_filename)
    plt.show()
    # plt.close(fig)
    print(f"Grid image saved as {output_filename}")

# Example usage:
create_image_grid(r"C:\Users\dzmit\Downloads\cat_images\cats_224x224\CAT_00")
