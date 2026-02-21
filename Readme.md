# Business Health Engine

## Overview

Business Health Engine is a Flask-based web application designed to analyze and visualize key business performance indicators for small and medium enterprises (SMEs). The system processes financial and operational data, generates derived business metrics, and presents insights through an interactive dashboard.

The application supports both sample-generated data and user-uploaded CSV datasets, making it suitable for demonstration, academic projects, and early-stage business analytics prototyping.

---

## Key Features

* Automated data loading and preprocessing
* Time-series business data simulation
* Financial metrics calculation:

  * Revenue
  * Expenses
  * Profit
  * Profit Margin
* Operational metrics:

  * Project Success Rate
  * Client Retention Rate
  * Late Payment Ratio
* Rolling trend analysis (3-month averages)
* Dashboard visualization using Jinja templates
* CSV data upload support
* Modular and scalable Flask structure

---

## Technology Stack

Backend:

* Python 3.13
* Flask
* Pandas
* NumPy

Frontend:

* HTML5
* Jinja2 templating
* CSS (custom styling)

Version Control:

* Git
* GitHub

Deployment:

* Compatible with Render and other WSGI-based platforms

---

## Project Structure

```
BusinessHealthEngine/
│
├── app/
│   ├── __init__.py
│   ├── routes.py
│   ├── data_processing.py
│   └── templates/
│       ├── base.html
│       ├── dashboard.html
│       └── index.html
│
├── run.py
├── requirements.txt
└── README.md
```

---

## Installation and Setup

### 1. Clone Repository

```
git clone https://github.com/your-username/Business-Health-Engine.git
cd Business-Health-Engine
```

### 2. Create Virtual Environment

```
python -m venv venv
venv\Scripts\activate
```

Mac/Linux:

```
source venv/bin/activate
```

### 3. Install Dependencies

```
pip install -r requirements.txt
```

### 4. Run Application

```
python run.py
```

Open browser:

```
http://127.0.0.1:5000
```

---

## Data Processing Architecture

The application is divided into two core processing classes:

### DataLoader

* Generates synthetic business data
* Supports CSV upload
* Applies seasonal and growth trends
* Includes fallback logic for resilience

### DataProcessor

* Handles missing values
* Converts date formats
* Calculates derived metrics
* Adds rolling averages for trend detection
* Prepares data for dashboard rendering

This modular separation improves maintainability and extensibility.

---

## Dashboard Capabilities

The dashboard displays:

* Recent performance metrics
* Time-based business trends
* Operational health indicators
* Financial summaries

All date formatting and metric computation are handled in the backend to maintain separation of concerns.

---

## Deployment on Render

1. Push project to GitHub
2. Create new Web Service on Render
3. Connect repository
4. Set build command:

   ```
   pip install -r requirements.txt
   ```
5. Set start command:

   ```
   gunicorn run:app
   ```
6. Add environment variable if required:

   ```
   PYTHON_VERSION=3.13.7
   ```

---

## Future Improvements

* Add authentication system
* Integrate database storage (PostgreSQL)
* Implement chart visualization (Chart.js or Plotly)
* Add export to PDF or Excel
* Introduce AI-driven anomaly detection
* Deploy containerized version using Docker

---

## Author

Tapan Khandelwal
Business Analytics and Software Development Enthusiast

---

