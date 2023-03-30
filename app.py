import os
import openai
from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit
from config import OPEN_AI_KEY
app = Flask(__name__)
socketio = SocketIO(app)

openai.api_key = OPEN_AI_KEY

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('message')
def handle_message(data):
    user_message = data['message']
    messages = data['messages']

    messages.append({"role": "user", "content": user_message})
    
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages
    )
    
    assistant_message = response.choices[0].message.content
    messages.append({"role": "assistant", "content": assistant_message})
    print(messages)
    emit('response', {'message': assistant_message, 'messages': messages})

if __name__ == '__main__':
    socketio.run(app, debug=True)
