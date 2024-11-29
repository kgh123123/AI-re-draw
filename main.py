from flask import Flask, render_template, request
from PIL import Image
import io
import base64

app = Flask(__name__)

@app.route("/")
def main():
    return render_template("index.html")

def base64toimg(encode_image):
    _, code = encode_image.split(",")

    binary = base64.b64decode(code)
    img = Image.open(io.BytesIO(binary))
    return img

#TODO: api?로 사진 분석 -> 프롬포트 도출 -> 다시 api? 검토, js 로 이미지 받아서 python POST로 보내기
@app.route("/make_it",methods=['POST'])
def make_it():
    encode_image = request.form.get('image')
    img = base64toimg(encode_image)
    img.save("saved_img.png")
    
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')