from diffusers import StableDiffusionPipeline, EulerDiscreteScheduler
import torch
from PIL import Image
import torchvision.transforms as transforms
import time

def k2img(prompt):
    model_id = "Falah/babylon"
    scheduler = EulerDiscreteScheduler.from_pretrained(model_id, subfolder="scheduler")
    pipe = StableDiffusionPipeline.from_pretrained(model_id, scheduler=scheduler, torch_dtype=torch.float16)
    pipe = pipe.to("cuda")
    image = pipe(prompt).images[0]
    # Generate timestamp for the filename
    timestamp = time.strftime("%Y%m%d%H%M%S")
    # Save the image with the timestamp as the filename
    image.save(f"out_{timestamp}.png")
    print("Image saved ")
    # Display the image
    image.show()
    # Upscale the image to high resolution
    upscale_transform = transforms.Resize((1024, 1024))
    upscaled_image = upscale_transform(image)
    # Save the upscaled image with the timestamp as the filename
    upscaled_image.save(f"out_upscale_{timestamp}.png")
    print("Upscaled image saved ")
    # Display the upscaled image
    upscaled_image.show()
