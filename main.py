from flask import Flask, render_template, request, send_file
from utility import *
import image2image

app = Flask(__name__)
app.secret_key = 'LN$oaYB9-5KBT7G'

@app.route("/")
def main():
    return render_template("index.html")

#TODO: api?로 사진 분석 -> 프롬포트 도출 -> 다시 api? 검토, js 로 이미지 받아서 python POST로 보내기
@app.route("/make_it",methods=['POST'])
def make_it():
    print('요청을 받았습니다.')
    encode_image = request.form.get('image')
    try:
        img = base64_to_img(encode_image)
        image2image.send_to_api(img,'lion')
        return send_file('static/output.png', mimetype="image/png")
    except Exception as e:
        print(e)
        return str(e), 500
    
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')