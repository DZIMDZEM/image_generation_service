import torch

from src.api.domain_features.dcgan.dcgan import Generator


def load_dcgan_model(path: str) -> Generator:
    checkpoint = torch.load(path)

    dcgan_model = Generator(latent_size=100, ngf=64, output_channels_size=3)
    print(checkpoint.keys())
    dcgan_model.load_state_dict(checkpoint['generator_state_dict'])

    return dcgan_model
