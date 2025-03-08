from flask import Blueprint, request, jsonify
from flask_cors import CORS
import os
from werkzeug.utils import secure_filename
import mysql.connector
from flask import send_from_directory

# Create a Blueprint
blogs_bp = Blueprint("blogs", __name__)
CORS(blogs_bp)

# Database connection configuration
db_config = {
    'user': 'root',
    'password': '0ldTimes!',
    'host': 'localhost',
    'database': 'aisolutionDB',
    'raise_on_warnings': True
}

UPLOAD_FOLDER = "uploads"
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@blogs_bp.route("/blogs/<int:blog_id>", methods=["GET"])
def get_blog(blog_id):
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)

        cursor.execute("""
            SELECT blogs.*, users.name AS writer_name
            FROM blogs
            JOIN users ON blogs.user_id = users.id
            WHERE blogs.id = %s
        """, (blog_id,))

        blog = cursor.fetchone()
        cursor.close()
        conn.close()

        if blog:
            # Ensure correct image paths
            blog["image1"] = f"http://localhost:5000/uploads/{os.path.basename(blog['image1'])}"
            blog["image2"] = f"http://localhost:5000/uploads/{os.path.basename(blog['image2'])}"
            blog["image3"] = f"http://localhost:5000/uploads/{os.path.basename(blog['image3'])}"
            return jsonify(blog), 200

        return jsonify({"error": "Blog not found"}), 404

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# API to get the latest blog ID
@blogs_bp.route("/latest-blog-id", methods=["GET"])
def get_latest_blog_id():
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        cursor.execute("SELECT MAX(id) FROM blogs")
        latest_id = cursor.fetchone()[0]  # Get the latest ID

        cursor.close()
        conn.close()

        if latest_id is None:
            latest_id = 1  # Default to 1 if no blogs exist
        else:
            latest_id += 1  # Increment for the new blog

        return jsonify({"latest_blog_id": latest_id}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Function to create and return the blogs blueprint
def create_blogs_app():
    return blogs_bp

# API to create a blog (User ID from frontend)
@blogs_bp.route("/blogs", methods=["POST"])
def create_blog():
    try:
        data = request.form
        images = request.files.getlist("images")
        user_id = data.get("user_id")  # Get user ID from frontend

        if not user_id:
            return jsonify({"error": "User ID is required"}), 400

        if len(images) != 3:
            return jsonify({"error": "Exactly 3 images required"}), 400

        # Save images and get their filenames
        image_paths = []
        for img in images:
            filename = secure_filename(img.filename)
            filepath = os.path.join(UPLOAD_FOLDER, filename)
            img.save(filepath)
            image_paths.append(filepath)

        # Save blog to database
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        query = """INSERT INTO blogs (user_id, title, paragraph1, paragraph2, paragraph3, image1, image2, image3)
                   VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"""
        cursor.execute(query, (user_id, data["title"], data["paragraph1"], data["paragraph2"], data["paragraph3"],
                               image_paths[0], image_paths[1], image_paths[2]))
        conn.commit()
        cursor.close()
        conn.close()

        return jsonify({"message": "Blog created successfully"}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# API to get all blogs (Anyone can view)
@blogs_bp.route("/blogs", methods=["GET"])
def get_blogs():
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)

        # Fetch blogs in descending order (latest first)
        cursor.execute("""
            SELECT blogs.*, users.name AS writer_name
            FROM blogs
            JOIN users ON blogs.user_id = users.id
            ORDER BY blogs.id DESC
        """)
        
        blogs = cursor.fetchall()
        cursor.close()
        conn.close()

        return jsonify(blogs), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# API to delete a blog (No extra checks, frontend handles admin access)
@blogs_bp.route("/blogs/<int:blog_id>", methods=["DELETE"])
def delete_blog(blog_id):
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        cursor.execute("DELETE FROM blogs WHERE id = %s", (blog_id,))
        conn.commit()

        cursor.close()
        conn.close()

        return jsonify({"message": "Blog deleted successfully"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Serve uploaded images
@blogs_bp.route("/uploads/<filename>")
def serve_image(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)        

# API to upload an image separately
@blogs_bp.route("/upload", methods=["POST"])
def upload_image():
    if "file" not in request.files:
        return jsonify({"error": "No file provided"}), 400

    file = request.files["file"]
    filename = secure_filename(file.filename)
    filepath = os.path.join(UPLOAD_FOLDER, filename).replace("\\", "/")  # Convert \ to /
    file.save(filepath)

    return jsonify({"image_url": filepath}), 200
