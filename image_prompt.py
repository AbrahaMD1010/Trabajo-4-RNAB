import requests
from urllib.parse import quote
import base64

def generate_image_pollinations(prompt):
    # Codificar prompt para URL
    encoded_prompt = quote(prompt)
    url = f"https://image.pollinations.ai/prompt/{encoded_prompt}"

    try:
        response = requests.get(url)
        if response.status_code == 200:
            # Convertir imagen a base64 para enviarla al frontend
            img_base64 = base64.b64encode(response.content).decode("utf-8")
            return img_base64
        else:
            print(f"❌ Error: {response.status_code}")
            return None
    except Exception as e:
        print(f"❌ Error: {e}")
        return None