"""
Application factory for Business Health Intelligence Engine
"""

from flask import Flask


def create_app(config_object=None):
    """
    Application Factory
    Allows flexible configuration for development, testing, and production.
    """

    app = Flask(
        __name__,
        template_folder="templates",
        static_folder="static"
    )

    # --------------------------------------------------
    # Configuration
    # --------------------------------------------------

    app.config.update(
        SECRET_KEY="super-secret-key-change-in-production",
        JSON_SORT_KEYS=False
    )

    # Optional: Load external config if provided
    if config_object:
        app.config.from_object(config_object)

    # --------------------------------------------------
    # Register Blueprints
    # --------------------------------------------------

    from app.routes import main_bp
    app.register_blueprint(main_bp)

    # --------------------------------------------------
    # Health Check Route (important for Render)
    # --------------------------------------------------

    @app.route("/health")
    def health_check():
        return {"status": "ok"}, 200

    return app