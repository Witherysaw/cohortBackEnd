from flask import Flask
from flask_jwt_extended import JWTManager
from flask_mail import Mail
from User import create_user_app
from Inquiry import create_inquiries_app
from Blogs import create_blogs_app
from Chat import create_chat_app

# Initialize Flask app
def create_main_app():
    app = Flask(__name__)

    # Flask-Mail Configuration
    app.config["MAIL_SERVER"] = "smtp.gmail.com"
    app.config["MAIL_PORT"] = 587
    app.config["MAIL_USERNAME"] = "thureinrichard3@gmail.com"
    app.config["MAIL_PASSWORD"] = "jwov kqpe qkag jepb"
    app.config["MAIL_USE_TLS"] = True
    app.config["MAIL_USE_SSL"] = False

    # JWT Configuration
    app.config["JWT_SECRET_KEY"] = "ilovemaynyeinkyaw"

    # Initialize Mail and JWT
    mail = Mail(app)
    jwt = JWTManager(app)

    # Register blueprints
    app.register_blueprint(create_user_app())
    app.register_blueprint(create_inquiries_app(mail))
    app.register_blueprint(create_blogs_app())
    app.register_blueprint(create_chat_app())  # ✅ Added this line

    return app

if __name__ == "__main__":
    app = create_main_app()
    app.run(debug=True)
