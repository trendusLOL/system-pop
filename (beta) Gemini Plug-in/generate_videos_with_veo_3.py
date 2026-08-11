import time
from google import genai
from google.genai import types

def generate_videos_with_veo_3(prompt: str, aspect_ratio: str = "16:9", reference_image_path: str = None):
    """
    Executes the Veo 3 video generation request via the Gemini API.
    """
    client = genai.Client()
    
    # Configure parameters
    config = types.GenerateVideosConfig(
        aspect_ratio=aspect_ratio,
    )
    
    # Handle optional image input if provided
    image_input = None
    if reference_image_path:
        # Load image bytes if passing local file reference
        with open(reference_image_path, "rb") as f:
            image_bytes = f.read()
        image_input = types.Image(image_bytes=image_bytes)
        config.image = image_input

    print(f"Initiating Veo 3 video generation for prompt: '{prompt}'...")
    
    # Trigger the asynchronous video generation operation
    operation = client.models.generate_videos(
        model="veo-3.1-generate-preview",
        prompt=prompt,
        config=config
    )
    
    # Poll until the background generation task completes
    while not operation.done:
        print("Rendering video and audio (this may take 1-2 minutes)...")
        time.sleep(10)
        operation = client.operations.get(operation)
        
    # Retrieve and save the generated asset
    generated_video = operation.response.generated_videos[0]
    output_filename = "veo_output_video.mp4"
    
    client.files.download(file=generated_video.video)
    generated_video.video.save(output_filename)
    
    print(f"Success! Video saved locally as {output_filename}")
    return output_filename

# Example Local Execution Test
if __name__ == "__main__":
    test_prompt = "A cinematic drone shot sweeping over a neon-lit cyberpunk city at night, rain slicked streets reflecting vibrant billboards, low humming synthwave soundtrack playing."
    generate_videos_with_veo_3(prompt=test_prompt, aspect_ratio="16:9")
