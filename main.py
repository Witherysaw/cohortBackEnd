from flask import Flask
from flask_jwt_extended import JWTManager
from flask_mail import Mail
from User import create_user_app
from Inquiry import create_inquiries_app  # Corrected import

# Initialize Flask app
def create_main_app():
    app = Flask(__name__)

    # Flask-Mail Configuration
    app.config["MAIL_SERVER"] = "smtp.gmail.com"
    app.config["MAIL_PORT"] = 587
    app.config["MAIL_USERNAME"] = "thureinrichard3@gmail.com"  # Replace with your email
    app.config["MAIL_PASSWORD"] = "jwov kqpe qkag jepb"  # Use correct App Password
    app.config["MAIL_USE_TLS"] = True
    app.config["MAIL_USE_SSL"] = False

     # JWT Configuration
    app.config["JWT_SECRET_KEY"] = "ilovemaynyeinkyaw" 

    # Initialize Mail
    mail = Mail(app)
    jwt = JWTManager(app) 

    # Register blueprints
    user_app = create_user_app()
    inquiries_app = create_inquiries_app(mail)  # Pass mail instance

    app.register_blueprint(user_app)
    app.register_blueprint(inquiries_app)
    

    return app

if __name__ == "__main__":
    app = create_main_app()
    app.run(debug=True)
