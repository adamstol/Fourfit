from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename
import os
import openai
import json
from dotenv import load_dotenv
import base64
from io import BytesIO
from PIL import Image
from pymongo import MongoClient
from bson.objectid import ObjectId

# Load environment variables from .env file
load_dotenv()

# Get environment variables
UPLOAD_FOLDER = os.getenv('UPLOAD_FOLDER')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# MongoDB client setup
DBPASS = os.getenv('DBPASS')
client = MongoClient(f"mongodb+srv://hackdeeznuts:{DBPASS}@htv9mongo.tylcf.mongodb.net/?retryWrites=true&w=majority&appName=htv9mongo")  # Update with your MongoDB connection URI
db = client['htv9db']  # Replace with your database name
users_collection = db['user']
items_collection = db['clothes']

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

@app.route('/search', methods=['POST'])
def search_similar_items():
    data = request.get_json()

    # Ensure the user ID is provided in the request
    if '_id' not in data:
        return jsonify({"error": "No user ID provided"}), 400

    user_id = data['_id']

    try:
        # Retrieve the user from the database
        user = users_collection.find_one({"_id": ObjectId(user_id)})

        if not user:
            return jsonify({"error": "User not found"}), 404

        # Get the user's liked tags (hash map)
        liked_tags = user.get('liked_tags', {})

        # Extract the keys from the hash map to use as an array
        tags_array = list(liked_tags.keys())

        if not tags_array:
            return jsonify({"error": "No liked tags found for user"}), 404

        # Find items that match any of the user's liked tags
        matching_items = items_collection.find({"tags": {"$in": tags_array}})

        # Convert the matching items to a list and serialize ObjectId to string
        item_list = [{**item, "_id": str(item["_id"])} for item in matching_items]

        # If no items are found, return a message
        if not item_list:
            return jsonify({"message": "No matching items found"}), 200

        # Return the matching items
        return jsonify({"success": True, "items": item_list}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
if __name__ == '__main__':
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    app.run(debug=True)
