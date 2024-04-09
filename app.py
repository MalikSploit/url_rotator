import json

from flask import Flask, render_template, request, jsonify, url_for, redirect
from flask_socketio import SocketIO

app = Flask(__name__)
socketio = SocketIO(app)
urls_file = 'urls.json'


@app.route('/')
def index():
    return redirect(url_for('admin'))


@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        urls = request.form.get('urls')
        try:
            json.loads(urls)  # Validate JSON format
            with open(urls_file, 'w') as file:
                file.write(urls)
        except json.JSONDecodeError:
            return "Invalid JSON", 400
        return redirect(url_for('admin'))
    else:
        try:
            with open(urls_file, 'r') as file:
                urls = file.read()
        except FileNotFoundError:
            urls = '[]'
        return render_template('admin.html', urls=urls)


@app.route('/display')
def display():
    try:
        with open(urls_file, 'r') as file:
            urls = json.load(file)
    except FileNotFoundError:
        urls = []
    return render_template('display.html', urls=urls)


@app.route('/update-urls', methods=['POST'])
def update_urls():
    data = request.get_json()
    urls = data.get('urls', [])
    try:
        with open(urls_file, 'w') as file:
            json.dump(urls, file)
        socketio.emit('update', {'urls': urls})
        return jsonify({'message': 'URL mis à jour avec succès'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/get-urls', methods=['GET'])
def get_urls():
    try:
        with open(urls_file, 'r') as file:
            urls = json.load(file)
    except FileNotFoundError:
        urls = []
    return jsonify(urls)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
