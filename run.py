"""
Entry point for Business Health Intelligence Engine
"""

from app import create_app

# Create application instance
app = create_app()

if __name__ == "__main__":
    # Only used for local development
    app.run(host="0.0.0.0", port=5000, debug=True)