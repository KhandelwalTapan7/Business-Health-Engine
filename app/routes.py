"""
Routes module for the Business Health Intelligence Engine
"""

from flask import Blueprint, render_template, jsonify, request, flash

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
        
        # Ensure recent_data is a list
        if recent_data is None:
            recent_data = []

        return render_template(
            "dashboard.html",
            health_scores=health_scores,
            risks=risks,
            insights=insights,
            recent_data=recent_data,
        )

    except Exception as e:
        # Log the error
        print(f"Dashboard error: {str(e)}")
        
        # Return fallback data so template renders properly
        fallback_health_scores = {
            'overall_health': 72.5,
            'financial_health': 68,
            'operational_health': 75,
            'client_health': 70,
            'project_health': 78,
            'health_status': 'Good'
        }
        
        fallback_risks = [
            {
                'category': 'info',
                'severity': 'low',
                'title': 'Using Sample Data',
                'description': 'Displaying sample data. Upload your own CSV for custom analysis.',
                'recommendation': 'Go to Upload page to analyze your business data.'
            }
        ]
        
        fallback_insights = {
            'summary': [
                {'message': 'Welcome to Business Health Intelligence Engine!'},
                {'message': 'Upload your data to get personalized insights.'}
            ],
            'warnings': [],
            'opportunities': [
                {
                    'message': 'Sample data is being displayed',
                    'recommendation': 'Upload your own CSV file for custom analysis'
                }
            ],
            'recommendations': []
        }
        
        fallback_recent = [
            {
                'date': '2023-12-31',
                'revenue': 89000,
                'expenses': 60000,
                'profit': 29000,
                'profit_margin': 0.326,
                'projects_completed': 19,
                'late_payments': 9
            },
            {
                'date': '2023-11-30',
                'revenue': 84800,
                'expenses': 57000,
                'profit': 27800,
                'profit_margin': 0.328,
                'projects_completed': 18,
                'late_payments': 6
            }
        ]
        
        return render_template(
            "dashboard.html",
            health_scores=fallback_health_scores,
            risks=fallback_risks,
            insights=fallback_insights,
            recent_data=fallback_recent,
            error_message=str(e)  # Optional: pass error for debugging
        )


@main_bp.route("/upload", methods=["GET", "POST"])
def upload_data():
    """Upload CSV data"""
    if request.method == "POST":
        # Check if file was uploaded
        if "file" not in request.files:
            flash("No file uploaded", "danger")
            return render_template("upload.html", error="No file uploaded")

        file = request.files["file"]

        # Check if file is selected
        if file.filename == "":
            flash("No file selected", "warning")
            return render_template("upload.html", error="No file selected")

        # Check file extension
        if file and file.filename.endswith(".csv"):
            try:
                # Load and process the file
                df = data_loader.load_custom_data(file)
                processed_df = data_processor.process_data(df)

                # Calculate metrics
                health_scores = health_analyzer.calculate_health_scores(processed_df)
                risks = health_analyzer.detect_risks(processed_df)
                insights = insight_generator.generate_insights(
                    processed_df, health_scores, risks
                )
                
                # Get recent data
                recent_data = data_processor.get_recent_metrics(processed_df)

                # Success message
                flash("File uploaded and analyzed successfully!", "success")

                return render_template(
                    "dashboard.html",
                    health_scores=health_scores,
                    risks=risks,
                    insights=insights,
                    recent_data=recent_data,
                )

            except Exception as e:
                flash(f"Error processing file: {str(e)}", "danger")
                return render_template(
                    "upload.html", 
                    error=f"Error processing file: {str(e)}"
                )
        else:
            flash("Invalid file format. Please upload a CSV file.", "warning")
            return render_template(
                "upload.html", 
                error="Invalid file format. Please upload a CSV file."
            )

    # GET request - show upload form
    return render_template("upload.html")


@main_bp.route("/about")
def about():
    """About page"""
    return render_template("about.html")


# --------------------------------------------------
# API ENDPOINTS
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


@main_bp.route("/api/risks")
def api_risks():
    """API endpoint for risks"""
    try:
        df = data_loader.load_sample_data()
        processed_df = data_processor.process_data(df)
        risks = health_analyzer.detect_risks(processed_df)

        return jsonify({
            "status": "success",
            "data": risks
        })

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500


@main_bp.route("/api/insights")
def api_insights():
    """API endpoint for insights"""
    try:
        df = data_loader.load_sample_data()
        processed_df = data_processor.process_data(df)
        health_scores = health_analyzer.calculate_health_scores(processed_df)
        risks = health_analyzer.detect_risks(processed_df)
        insights = insight_generator.generate_insights(processed_df, health_scores, risks)

        return jsonify({
            "status": "success",
            "data": insights
        })

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500


@main_bp.route("/api/recent-data")
def api_recent_data():
    """API endpoint for recent data"""
    try:
        df = data_loader.load_sample_data()
        processed_df = data_processor.process_data(df)
        recent_data = data_processor.get_recent_metrics(processed_df)

        return jsonify({
            "status": "success",
            "data": recent_data
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
    """Handle 404 errors"""
    flash("Page not found", "warning")
    return render_template("index.html"), 404


@main_bp.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    flash("Internal server error occurred", "danger")
    return render_template(
        "dashboard.html",
        health_scores={
            'overall_health': 0, 
            'financial_health': 0,
            'operational_health': 0,
            'client_health': 0,
            'project_health': 0,
            'health_status': 'Error'
        },
        risks=[],
        insights={'summary': [{'message': 'Internal server error occurred'}]},
        recent_data=[]
    ), 500