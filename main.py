from flask import Flask, render_template, request
from utility import *

app = Flask(__name__)
app.secret_key = 'LN$oaYB9-5KBT7G'

@app.route("/")
def main():
    return render_template("index.html")

#TODO: api?로 사진 분석 -> 프롬포트 도출 -> 다시 api? 검토, js 로 이미지 받아서 python POST로 보내기
@app.route("/make_it",methods=['POST'])
def make_it():
    encode_image = request.form.get('image')
    try:
        img = base64_to_img(encode_image)
        #img.save("imgs/saved_img.png")
    except:
        return 500
    
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')