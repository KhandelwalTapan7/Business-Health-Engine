"""
Routes module for the Business Health Intelligence Engine
"""

from flask import Blueprint, render_template, jsonify, request

# Import internal modules
from app.data_processing import DataLoader, DataProcessor
from app.model import HealthAnalyzer, InsightGenerator

# --------------------------------------------------
# Blueprint Definition
# --------------------------------------------------

main_bp = Blueprint("main", __name__)

# --------------------------------------------------
# Initialize Core Components
# --------------------------------------------------

data_loader = DataLoader()
data_processor = DataProcessor()
health_analyzer = HealthAnalyzer()
insight_generator = InsightGenerator()

# --------------------------------------------------
# ROUTES
# --------------------------------------------------

@main_bp.route("/")
def index():
    """Home page"""
    return render_template("index.html")


@main_bp.route("/dashboard")
def dashboard():
    """Main dashboard page"""
    try:
        # Load sample data
        df = data_loader.load_sample_data()

        # Process data
        processed_df = data_processor.process_data(df)

        # Calculate health metrics
        health_scores = health_analyzer.calculate_health_scores(processed_df)

        # Detect risks
        risks = health_analyzer.detect_risks(processed_df)

        # Generate insights
        insights = insight_generator.generate_insights(
            processed_df, health_scores, risks
        )

        # Recent metrics
        recent_data = data_processor.get_recent_metrics(processed_df)

        return render_template(
            "dashboard.html",
            health_scores=health_scores,
            risks=risks,
            insights=insights,
            recent_data=recent_data,
        )

    except Exception as e:
        return render_template(
            "dashboard.html",
            error=f"Error loading dashboard: {str(e)}"
        ), 500


@main_bp.route("/upload", methods=["GET", "POST"])
def upload_data():
    """Upload CSV data"""
    if request.method == "POST":

        if "file" not in request.files:
            return render_template("upload.html", error="No file uploaded")

        file = request.files["file"]

        if file.filename == "":
            return render_template("upload.html", error="No file selected")

        if file and file.filename.endswith(".csv"):
            try:
                df = data_loader.load_custom_data(file)
                processed_df = data_processor.process_data(df)

                health_scores = health_analyzer.calculate_health_scores(processed_df)
                risks = health_analyzer.detect_risks(processed_df)
                insights = insight_generator.generate_insights(
                    processed_df, health_scores, risks
                )

                return render_template(
                    "dashboard.html",
                    health_scores=health_scores,
                    risks=risks,
                    insights=insights,
                    recent_data=processed_df.to_dict("records")[:10],
                )

            except Exception as e:
                return render_template("upload.html", error=f"Error: {str(e)}")

    return render_template("upload.html")


@main_bp.route("/about")
def about():
    """About page"""
    return render_template("about.html")


# --------------------------------------------------
# API ENDPOINT
# --------------------------------------------------

@main_bp.route("/api/health-metrics")
def api_health_metrics():
    """API endpoint for health metrics"""
    try:
        df = data_loader.load_sample_data()
        processed_df = data_processor.process_data(df)
        health_scores = health_analyzer.calculate_health_scores(processed_df)

        return jsonify({
            "status": "success",
            "data": health_scores
        })

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500


# --------------------------------------------------
# ERROR HANDLERS
# --------------------------------------------------

@main_bp.errorhandler(404)
def not_found_error(error):
    return render_template("index.html"), 404


@main_bp.errorhandler(500)
def internal_error(error):
    return "<h1>500 - Internal Server Error</h1><p><a href='/'>Go to Home</a></p>", 500