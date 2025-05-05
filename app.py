from flask import Flask, jsonify, request
from bili import BilibiliSearchPlugin
app = Flask(__name__)
plugin = BilibiliSearchPlugin(driver_path='D:/chromedriver-win32/chromedriver.exe')
@app.route('/search', methods=['POST'])
def search():
    data = request.get_json()
    question = data.get('question', '')
    result = plugin.handle_user_question(question)
    return jsonify({'answer': result})
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)