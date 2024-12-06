import requests
from dotenv import load_dotenv
import os
from utility import *
import random
from PIL import Image
from io import BytesIO  # 바이트 데이터를 메모리에서 처리

load_dotenv()

API_KEY = os.getenv("SEGMIND_API_KEY")
url = "https://api.segmind.com/v1/ssd-img2img"
img = Image.open("imgs/lion.png")

def send_to_api(image, prompt:str):
    random_seed = random.randint(1, 99999999)
    data = {
        "image": img_to_base64(image),
        "prompt": prompt,
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
            raise e
    else:
        print(f"API 요청 실패: {response.status_code}")
        print(f"응답 내용: {response.text}")
        raise Exception("API에서 잘못된 응답을 보냈습니다.")