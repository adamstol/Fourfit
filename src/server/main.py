from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename
import os
import openai
from dotenv import load_dotenv
import base64
from io import BytesIO
from PIL import Image

# Load environment variables from .env file
load_dotenv()

# Get environment variables
UPLOAD_FOLDER = os.getenv('UPLOAD_FOLDER')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Set OpenAI API Key from environment variable
openai.api_key = OPENAI_API_KEY

# Home route to display the upload form
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    data = request.get_json()

    if 'image_url' not in data:     
        return jsonify({"error": "No image URL provided"}), 400
    
    try:
        # Sending a message to GPT-4 using an image URL
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",  # Specify the model you want to use
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": "Analyze the following persons outfit and give recomendations based on their current style including tops, bottoms, shoes, and any accessories the person may be wearing in the photo. Do not give advice to change the style, for example if the person is wearing a casual fit mention what clothes or accessories are popular right now in that fashion. Your output must be no longer than five sentences long."},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": data['image_url'],
                            },
                        },
                    ],
                }
            ],
            max_tokens=300,
        )

        feedback = response['choices'][0]['message']['content'].strip()

        return jsonify({"success": True, "feedback": feedback}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == '__main__':
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    app.run(debug=True)
