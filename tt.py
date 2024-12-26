# AIzaSyD-nRtrIpgkScXR9HRaCSNY7akLnRzLPks

from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

# API key của bạn
API_KEY = 'AIzaSyD-nRtrIpgkScXR9HRaCSNY7akLnRzLPks'

# URL API Gemini
url = f'https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent?key={API_KEY}'

# Lưu lịch sử trò chuyện
chat_history = []

@app.route('/')
def home():
    return render_template('indexx.html')

@app.route('/chat', methods=['POST'])
def chat():
    global chat_history
    user_message = request.json.get('message')

    # Thêm câu hỏi vào lịch sử
    chat_history.append({"role": "user", "content": user_message})

    # Gửi yêu cầu đến API Gemini
    data = {
        "contents": [
            {
                "parts": [{"text": msg["content"]} for msg in chat_history]
            }
        ]
    }
    response = requests.post(url, headers={'Content-Type': 'application/json'}, json=data)

    if response.status_code == 200:
        response_data = response.json()
        answer = response_data.get("candidates", [{}])[0].get("content", {}).get("parts", [{}])[0].get("text", "Không có phản hồi.")
    else:
        answer = f"Lỗi {response.status_code}: {response.text}"

    # Thêm phản hồi của chatbot vào lịch sử
    chat_history.append({"role": "assistant", "content": answer})

    return jsonify({"response": answer})

if __name__ == '__main__':
    app.run(debug=True)