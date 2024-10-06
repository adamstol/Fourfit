import random
from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename
import os
import openai
from dotenv import load_dotenv
from pymongo import MongoClient
from bson.objectid import ObjectId
from flask_cors import CORS
import base64
import boto3

load_dotenv()

UPLOAD_FOLDER = os.getenv("UPLOAD_FOLDER")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
AWS_ACCESS_KEY = os.getenv("AWS_ACCESS_KEY")
AWS_SECRET_KEY = os.getenv("AWS_SECRET_KEY")
S3_BUCKET = os.getenv("S3_BUCKET")
openai.api_key = OPENAI_API_KEY

DBPASS = os.getenv("DBPASS")
client = MongoClient(
    f"mongodb+srv://hackdeeznuts:{DBPASS}@htv9mongo.tylcf.mongodb.net/?retryWrites=true&w=majority&appName=htv9mongo"
)
db = client["htv9db"]
users_collection = db["user"]
items_collection = db["clothes"]

s3_client = boto3.client(
    "s3", aws_access_key_id=AWS_ACCESS_KEY, aws_secret_access_key=AWS_SECRET_KEY
)

UPLOAD_FOLDER = "uploads/"
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
CORS(app, origins=["http://localhost:3000"])

seen_items = set()


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/")
def index():
    return render_template("index.html")


def feedback(filename):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": "Analyze the following persons outfit and give recomendations based on their current style including tops, bottoms, shoes, and any accessories the person may be wearing in the photo. Do not give advice to change the style, for example if the person is wearing a casual fit mention what clothes or accessories are popular right now in that fashion. Your output must be no longer than five sentences long.",
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"https://htv9bucket.s3.us-east-2.amazonaws.com/{filename}",
                            },
                        },
                    ],
                }
            ],
            max_tokens=300,
        )

        feedback = response["choices"][0]["message"]["content"].strip()

        return jsonify({"success": True, "feedback": feedback}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 400


@app.route("/search", methods=["POST"])
def search_similar_items():
    data = request.get_json()

    if "_id" not in data:
        return jsonify({"error": "No user ID provided"}), 400

    user_id = data["_id"]

    try:
        user = users_collection.find_one({"_id": ObjectId(user_id)})

        if not user:
            return jsonify({"error": "User not found"}), 404

        liked_tags = user.get("liked_tags", {})

        tags_array = [
            tag for tag, weight in liked_tags.items() for _ in range(weight or 1)
        ]

        if not tags_array:
            return jsonify({"error": "No liked tags found for user"}), 404

        random_items = []
        for _ in range(5):
            random_tag = random.choice(tags_array)

            matching_item = items_collection.find_one(
                {
                    "tags": {"$eq": random_tag},
                    "_id": {"$nin": list(seen_items)},
                }
            )

            if matching_item:
                item_id = matching_item["_id"]
                random_items.append(matching_item)
                seen_items.add(ObjectId(item_id))
            else:
                print("No matching item found")

        item_list = [{**item, "_id": str(item["_id"])} for item in random_items]

        if not item_list:
            return jsonify({"message": "No matching items found"}), 200

        for item in item_list:
            seen_items.add(ObjectId(item["_id"]))

        return jsonify({"success": True, "items": item_list}), 200

    except Exception as e:
        print(str(e))
        return jsonify({"error": str(e)}), 500


@app.route("/like", methods=["POST"])
def like_item():
    data = request.get_json()

    if "_id" not in data or "item_id" not in data:
        return jsonify({"error": "User ID and item ID are required"}), 400

    user_id = data["_id"]
    item_id = data["item_id"]

    try:
        user = users_collection.find_one({"_id": ObjectId(user_id)})

        if not user:
            return jsonify({"error": "User not found"}), 404

        liked_items = user.get("liked_items", [])
        if item_id in liked_items:
            return jsonify({"message": "Item already liked"}), 200

        item = items_collection.find_one({"_id": ObjectId(item_id)})

        if not item:
            return jsonify({"error": "Item not found"}), 404

        tags = item.get("tags", [])

        if not tags:
            return jsonify({"error": "Item has no tags"}), 404

        liked_tags = user.get("liked_tags", {})

        for tag in tags:
            liked_tags[tag] = liked_tags.get(tag, 0) + 1

        liked_items.append(item_id)

        users_collection.update_one(
            {"_id": ObjectId(user_id)},
            {"$set": {"liked_tags": liked_tags, "liked_items": liked_items}},
        )

        return jsonify({"success": True, "liked_tags": liked_tags}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/unlike", methods=["POST"])
def unlike_item():
    data = request.get_json()

    if "_id" not in data or "item_id" not in data:
        return jsonify({"error": "User ID and item ID are required"}), 400

    user_id = data["_id"]
    item_id = data["item_id"]

    try:
        user = users_collection.find_one({"_id": ObjectId(user_id)})

        if not user:
            return jsonify({"error": "User not found"}), 404

        liked_items = user.get("liked_items", [])
        if item_id not in liked_items:
            return jsonify({"message": "Item has not been liked"}), 400

        item = items_collection.find_one({"_id": ObjectId(item_id)})

        if not item:
            return jsonify({"error": "Item not found"}), 404

        tags = item.get("tags", [])

        if not tags:
            return jsonify({"error": "Item has no tags"}), 404

        liked_tags = user.get("liked_tags", {})

        for tag in tags:
            if tag in liked_tags:
                liked_tags[tag] -= 1
                if liked_tags[tag] <= 0:
                    del liked_tags[tag]

        liked_items.remove(item_id)

        users_collection.update_one(
            {"_id": ObjectId(user_id)},
            {"$set": {"liked_tags": liked_tags, "liked_items": liked_items}},
        )

        return jsonify({"success": True, "liked_tags": liked_tags}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/upload", methods=["POST"])
def upload_file():
    if "file" not in request.json:
        return jsonify({"error": "No file part"}), 400

    base64_data = request.json["file"]

    try:
        if "," in base64_data:
            header, base64_data = base64_data.split(",")
            file_ext = header.split(";")[0].split("/")[1]
        else:
            return jsonify({"error": "Invalid base64 data"}), 400

        if not allowed_file(f"file.{file_ext}"):
            return jsonify({"error": "File type not allowed"}), 400

        file_data = base64.b64decode(base64_data)

        filename = secure_filename(f"uploaded_file.{file_ext}")

        print(filename)
        file_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)

        os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

        with open(file_path, "wb") as f:
            f.write(file_data)

        s3_client.upload_file(
            file_path,
            S3_BUCKET,
            filename,
            ExtraArgs={
                "ACL": "public-read",
            },
        )

        os.remove(file_path)

        return feedback(filename)

    except Exception as e:
        print(str(e))
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    app.run(debug=True, port=5000)
