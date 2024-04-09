from flask import Flask, render_template, request, make_response
import os

app = Flask(__name__)
URLS_FILE = "C:/Users/malik/Desktop/urls.txt"


@app.route('/')
def index():
    return render_template('admin.html')


@app.route('/get-urls', methods=['GET'])
def get_urls():
    if os.path.exists(URLS_FILE):
        with open(URLS_FILE, 'r') as file:
            urls = file.read()
    else:
        urls = ''
    return make_response(urls, 200)


@app.route('/update-urls', methods=['POST'])
def update_urls():
    data = request.data.decode('utf-8')
    with open(URLS_FILE, 'w') as file:
        file.write(data)
    return make_response('URLs successfully updated', 200)


if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0')
