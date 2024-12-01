import requests
from dotenv import load_dotenv
import os
import base64
import random
from PIL import Image
from io import BytesIO  # 바이트 데이터를 메모리에서 처리

load_dotenv()

def img_file_to_base64(img_path):
    with open(img_path, 'rb') as f:
        img_data = f.read()
    return base64.b64encode(img_data).decode('utf8')

API_KEY = os.getenv("SEGMIND_API_KEY")
url = "https://api.segmind.com/v1/ssd-img2img"
random_seed = random.randint(1, 99999999)
img_path = "imgs/lion.png"

data = {
    "image": img_file_to_base64(img_path),
    "prompt": "scary lion",
    "samples": 1,
    "scheduler": "Euler a",
    "num_interface_steps": 30,
    "guidance_scale": 7.5,
    "seed": random_seed,
    "strength": 0.9,
    "base64": False,
}

headers = {'x-api-key': API_KEY}
response = requests.post(url, json=data, headers=headers)

if response.status_code == 200:
    try:
        # BytesIO를 통해 바이트 데이터를 PIL 이미지로 변환
        img = Image.open(BytesIO(response.content))  # 이미지 객체 생성
        output_path = "imgs/output.png"
        img.save(output_path)  # 이미지 저장
        print(f"이미지가 저장되었습니다: {output_path}")
    except Exception as e:
        print(f"이미지 처리 중 오류가 발생했습니다: {e}")
else:
    print(f"API 요청 실패: {response.status_code}")
    print(f"응답 내용: {response.text}")