import torch
from src.api.domain_features.dcgan.dcgan import Generator

def load_dcgan_model(path: str, save_path: str) -> Generator:
    # Load the checkpoint with map_location set to 'cpu' to ensure it loads on the CPU
    checkpoint = torch.load(path, map_location=torch.device('cpu'))

    # Initialize the model
    dcgan_model = Generator(latent_size=100, ngf=64, output_channels_size=3)
    dcgan_model.load_state_dict(checkpoint['generator_state_dict'])

    # Optionally, save the model back to disk with all tensors on CPU
    torch.save({'generator_state_dict': dcgan_model.state_dict()}, save_path)

    return dcgan_model

# Example usage
model = load_dcgan_model(
    r"C:\Users\dzmit\JOB\catnet\src\model_weights\dcgan_cat_299.pth",
    r"C:\Users\dzmit\JOB\catnet\src\model_weights\dcgan_cat_299_cpu.pth")
