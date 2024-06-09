import base64

import cv2
import numpy as np
import torch
from injector import inject

from src.api.domain_features.dcgan.dcgan import Generator


class GenerationService:
    @inject
    def __init__(self, generator: Generator):
        # self.latent_size = latent_size
        # self.ngf = ngf
        # self.output_channels_size = output_channels_size
        self.model = generator

    @staticmethod
    def __sample_spherical__(npoints, ndim=3, seed=None):
        if seed is not None:
            np.random.seed(seed)

        vec = np.random.randn(ndim, npoints)
        vec /= np.linalg.norm(vec, axis=0)

        return vec

    @staticmethod
    def interpolate_along_great_circle(latent_dim, num_steps, device='cpu', seed=None):
        """
        Generates a series of latent vectors interpolated along a great circle in the latent space.

        Parameters:
            latent_dim (int): Dimension of the latent space.
            num_steps (int): Number of interpolation steps along the great circle.
            device (str): Device to which the latent vectors will be sent ('cpu' or 'cuda').

        Returns:
            torch.Tensor: Interpolated latent vectors shaped (num_steps, latent_dim, 1, 1).
        """
        # Generate two points on the unit sphere in latent space
        points = torch.tensor(
            GenerationService.__sample_spherical__(2, latent_dim, seed=seed),
            dtype=torch.float,
            device=device).t()
        start, end = points[0], points[1]

        # Compute the angle between them
        dot = torch.dot(start, end)
        theta = torch.acos(dot)

        # Generate the steps
        steps = torch.linspace(0, 1, num_steps, device=device)
        sin_t = torch.sin(theta)

        # Perform the interpolation
        latent_vectors = []
        for step in steps:
            alpha = torch.sin((1 - step) * theta) / sin_t
            beta = torch.sin(step * theta) / sin_t
            interpolated_point = alpha * start + beta * end
            latent_vectors.append(interpolated_point.unsqueeze(0).unsqueeze(-1).unsqueeze(-1))

        # Concatenate all interpolated points
        return torch.cat(latent_vectors, dim=0)

    @staticmethod
    def tensor_to_image(tensor):
        """
        Converts a tensor to a base64-encoded image.

        Parameters:
            tensor (torch.Tensor): A tensor with shape (C, H, W) and values in the range [-1, 1].

        Returns:
            str: A base64-encoded string of the image.
        """
        # Normalize the tensor to [0, 1]
        tensor = (tensor + 1) / 2 * 255
        tensor = tensor.clamp(0, 255)

        # Convert to numpy and ensure type is uint8
        numpy_image = tensor.cpu().detach().numpy().astype(np.uint8)

        # If it's a grayscale image (1 channel), convert it to 3 channels
        if numpy_image.shape[0] == 1:
            numpy_image = np.repeat(numpy_image, 3, axis=0)

        # Transpose from (C, H, W) to (H, W, C)
        numpy_image = numpy_image.transpose(1, 2, 0)

        # Encode as JPEG
        _, buffer = cv2.imencode('.jpg', numpy_image)
        jpg_as_text = base64.b64encode(buffer).decode('utf-8')

        return jpg_as_text

    def generate(self, latent_vector):
        return self.model(latent_vector)
