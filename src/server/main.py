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
import boto3

# Load environment variables from .env file
load_dotenv()

# Get environment variables
UPLOAD_FOLDER = os.getenv('UPLOAD_FOLDER')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
AWS_ACCESS_KEY = os.getenv('AWS_ACCESS_KEY')
AWS_SECRET_KEY = os.getenv('AWS_SECRET_KEY')
S3_BUCKET = os.getenv('S3_BUCKET')
openai.api_key = OPENAI_API_KEY

# MongoDB client setup
DBPASS = os.getenv('DBPASS')
client = MongoClient(f"mongodb+srv://hackdeeznuts:{DBPASS}@htv9mongo.tylcf.mongodb.net/?retryWrites=true&w=majority&appName=htv9mongo")  # Update with your MongoDB connection URI
db = client['htv9db']  # Replace with your database name
users_collection = db['user']
items_collection = db['clothes']

s3_client = boto3.client(
    's3',
    aws_access_key_id=AWS_ACCESS_KEY,
    aws_secret_access_key=AWS_SECRET_KEY
)

UPLOAD_FOLDER = 'uploads/'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Home route to display the upload form
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/feedback', methods=['POST'])
def feedback():
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
    
@app.route('/like', methods=['POST'])
def like_item():
    data = request.get_json()

    # Ensure the user ID and item ID are provided in the request
    if '_id' not in data or 'item_id' not in data:
        return jsonify({"error": "User ID and item ID are required"}), 400

    user_id = data['_id']
    item_id = data['item_id']

    try:
        # Retrieve the user from the database
        user = users_collection.find_one({"_id": ObjectId(user_id)})

        if not user:
            return jsonify({"error": "User not found"}), 404

        # Check if the user has already liked this item
        liked_items = user.get('liked_items', [])
        if item_id in liked_items:
            return jsonify({"message": "Item already liked"}), 200

        # Retrieve the item from the database
        item = items_collection.find_one({"_id": ObjectId(item_id)})

        if not item:
            return jsonify({"error": "Item not found"}), 404

        # Get the tags from the item
        tags = item.get('tags', [])

        # Ensure tags exist
        if not tags:
            return jsonify({"error": "Item has no tags"}), 404

        # Update the user's liked tags map
        liked_tags = user.get('liked_tags', {})

        # Increment the count for each tag in the liked_tags map
        for tag in tags:
            liked_tags[tag] = liked_tags.get(tag, 0) + 1

        # Add the item to liked_items
        liked_items.append(item_id)

        # Update the user document with the new liked_tags map and liked_items array
        users_collection.update_one(
            {"_id": ObjectId(user_id)},
            {"$set": {"liked_tags": liked_tags, "liked_items": liked_items}}
        )

        # Return the updated liked_tags
        return jsonify({"success": True, "liked_tags": liked_tags}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/unlike', methods=['POST'])
def unlike_item():
    data = request.get_json()

    # Ensure the user ID and item ID are provided in the request
    if '_id' not in data or 'item_id' not in data:
        return jsonify({"error": "User ID and item ID are required"}), 400

    user_id = data['_id']
    item_id = data['item_id']

    try:
        # Retrieve the user from the database
        user = users_collection.find_one({"_id": ObjectId(user_id)})

        if not user:
            return jsonify({"error": "User not found"}), 404

        # Check if the user has actually liked this item
        liked_items = user.get('liked_items', [])
        if item_id not in liked_items:
            return jsonify({"message": "Item has not been liked"}), 400

        # Retrieve the item from the database
        item = items_collection.find_one({"_id": ObjectId(item_id)})

        if not item:
            return jsonify({"error": "Item not found"}), 404

        # Get the tags from the item
        tags = item.get('tags', [])

        # Ensure tags exist
        if not tags:
            return jsonify({"error": "Item has no tags"}), 404

        # Update the user's liked tags map
        liked_tags = user.get('liked_tags', {})

        # Decrement the count for each tag in the liked_tags map
        for tag in tags:
            if tag in liked_tags:
                liked_tags[tag] -= 1
                # If the count reaches 0, remove the tag from the map
                if liked_tags[tag] <= 0:
                    del liked_tags[tag]

        # Remove the item from liked_items
        liked_items.remove(item_id)

        # Update the user document with the new liked_tags map and liked_items array
        users_collection.update_one(
            {"_id": ObjectId(user_id)},
            {"$set": {"liked_tags": liked_tags, "liked_items": liked_items}}
        )

        # Return the updated liked_tags
        return jsonify({"success": True, "liked_tags": liked_tags}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    if file and allowed_file(file.filename):
        try:
            # Secure the filename and save it temporarily
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)

            # Determine the Content-Type of the file (MIME type)
            content_type = file.content_type  # This should correctly identify the MIME type

            # Upload the image to S3 with public-read ACL and correct Content-Type
            s3_client.upload_file(
                file_path,
                S3_BUCKET,
                filename,
                ExtraArgs={
                    'ACL': 'public-read',
                    'ContentType': content_type  # Set the correct MIME type
                }
            )

            # Generate a public URL for the uploaded image
            s3_url = f"https://{S3_BUCKET}.s3.amazonaws.com/{filename}"

            # Remove the file from the local server after upload
            os.remove(file_path)

            return jsonify({"success": True, "s3_url": s3_url}), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    else:
        return jsonify({"error": "File not allowed"}), 400

if __name__ == '__main__':
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    app.run(debug=True)
