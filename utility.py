from PIL import Image
import io
import base64

def img_to_base64(img_path):
    with open(img_path, 'rb') as f:
        img_data = f.read()
    return base64.b64encode(img_data).decode('utf8')

def base64_to_img(encode_image:str):
    _, code = encode_image.split(",")

    binary = base64.b64decode(code)
    img = Image.open(io.BytesIO(binary))
    return img
