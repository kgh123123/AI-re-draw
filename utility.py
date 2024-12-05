from PIL import Image
import io
import base64

def img_to_base64(image):
    buffered = io.BytesIO()
    image.save(buffered, format="JPEG")
    encode_image = base64.b64encode(buffered.getvalue()).decode('utf8')
    return encode_image

def base64_to_img(encode_image:str):
    _, code = encode_image.split(",")

    binary = base64.b64decode(code)
    image = Image.open(io.BytesIO(binary))
    return image
