from flask import Flask, render_template, request
from PIL import Image
import io
import image2image

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16 MB limit
app.secret_key = 'LN$oaYB9-5KBT7G'

@app.route("/")
def main():
    return render_template("index.html")

@app.route("/make_it",methods=['POST'])
def make_it():
    print('요청을 받았습니다.')
    image_file = request.files.get('image')
    if image_file is None:
        return 'No image provided', 400

    try:
        img = Image.open(io.BytesIO(image_file.read()))
        prompt = 'lion'
        image2image.send_to_api(img, prompt)
        return 'static/output.png'
    except Exception as e:
        print(e)
        return str(e), 500
    
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')