import torch
from flask_restful import Resource, reqparse
from injector import inject

from src.api.domain_features.dcgan.dcgan_service import GenerationService
from src.api.logger import get_logger

logger = get_logger(__name__)


class GenerateImageResource(Resource):
    cache_images: torch.Tensor = torch.zeros(24, 3, 64, 64)
    last_random_seed: int = None
    @inject
    def __init__(self, service: GenerationService):
        self.service = service

        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument(
            'random_seed',
            type=int,
            required=True,
            help='Random seed is required',
            location='json'
        )
        self.reqparse.add_argument(
            'number_steps',
            type=int,
            required=True,
            help='Number of interpolation steps is required',
            location='json'
        )

    def post(self):
        args = self.reqparse.parse_args()
        random_seed = args['random_seed']
        number_steps = args['number_steps']
        print(random_seed)

        if random_seed != GenerateImageResource.last_random_seed or random_seed is None:
            input_tensor = self.service.interpolate_along_great_circle(100, 24, seed=random_seed)
            with torch.no_grad():
                GenerateImageResource.cache_images = self.service.generate(input_tensor)

        generated_image = self.cache_images[number_steps - 1:number_steps]
        GenerateImageResource.last_random_seed = random_seed

        processed_images = []
        for i in range(24):
            generated_image = self.cache_images[i:i + 1]
            if generated_image is not None and generated_image.nelement() != 0:
                # Assuming generated_image is a single tensor with dimensions (C, H, W)
                # Normalize and encode the tensor to a base64 string
                processed_image = GenerationService.tensor_to_image(generated_image.squeeze())

            processed_images.append(processed_image)

        if processed_images is not None:
            return {"success": True, "generated_images": processed_images}, 200
        else:
            # Handle the case where the generated image is invalid or the generation failed
            return {"success": False, "message": "Failed to generate image"}, 500
