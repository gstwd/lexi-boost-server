from flask import Blueprint

def register_routes(app):
    from app.routes.words import words_bp
    app.register_blueprint(words_bp, url_prefix='/api')