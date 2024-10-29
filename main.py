from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/")
def main():
    return render_template("index.html")

#TODO: 강의 듣고 프로그램 다 만들기, css 수정 검토하기, api로 사진 분석 -> 프롬포트 도출 -> 다시 api? 검토

@app.route("/make_idk",methods=['POST'])
def make_idk():
    f = request.files.get('img')
    print(f"eawefawe{f.filename}")

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')