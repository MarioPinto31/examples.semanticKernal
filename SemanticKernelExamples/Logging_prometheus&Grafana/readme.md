# OBSERVABILITY_SETUP.md: Flask Agent Observability Stack

This document provides a guide to setting up an observability stack for our multi-agent Flask application using **Prometheus** for metrics, **Grafana** for visualization, and **OpenTelemetry (OTel) Tracing** for deep agent debugging.

## 🚀 1. Prerequisites and Deployment

### Prerequisites

* **Python 3.10+** (for the Flask API and Semantic Kernel).
* **Docker** and **Docker Compose** (to run the monitoring services easily).
* **Required Python Packages:**
    ```bash
    pip install flask prometheus-client prometheus-flask-exporter semantic-kernel
    # For Tracing:
    pip install opentelemetry-api opentelemetry-sdk opentelemetry-exporter-otlp-proto-http
    ```

### Deployment (Getting Started)

1.  Ensure all the files below (`api.py`, `prometheus.yml`, `docker-compose.yml`) are in the same directory.
2.  Run the following command to build the Flask app and start all services (App, Prometheus, Grafana) in the background:

    ```bash
    docker compose up --build -d
    ```

3.  Wait a minute for all containers to initialize.
4.  Verify all services are running: `docker compose ps`

---

## 💻 2. Application Scripts & Configuration

### 2.1. `app/api.py` (Flask API Backend)

This script demonstrates integrating custom metrics into the Flask application, specifically tracking agent invocations and execution time.

```python
# app/api.py - Simplified Flask + Prometheus Example

from flask import Flask, request, jsonify
from prometheus_flask_exporter import PrometheusMetrics
from prometheus_client import Counter, Histogram
import time
# NOTE: Replace with your actual Semantic Kernel imports

app = Flask(__name__)
# Initialize Prometheus Metrics on the Flask app
# This automatically exposes /metrics endpoint with default HTTP metrics
metrics = PrometheusMetrics(app, group_by='endpoint')

# 1. Custom Counter for agent invocation
AGENT_INVOCATION_COUNTER = Counter(
    'agent_invocation_total', 
    'Total number of times a specific agent has been invoked',
    ['agent_name'] # Label to differentiate agents
)

# 2. Custom Histogram for agent execution time
AGENT_EXECUTION_TIME = Histogram(
    'agent_execution_seconds', 
    'Agent processing time (seconds)',
    ['agent_name'] 
)

@app.route('/health')
def health_check():
    """Simple endpoint for liveness/readiness checks."""
    return 'OK', 200

@app.route('/api/agent/run/<agent_name>', methods=['POST'])
# Decorate the endpoint to track duration automatically by Flask Exporter
@metrics.time_this('api_agent_run_duration') 
def run_agent(agent_name):
    """Example agent execution endpoint."""
    start_time = time.time()
    
    try:
        data = request.json
        user_input = data.get('input', 'default task')
        
        # --- Semantic Kernel Logic (Placeholder) ---
        # Run your Semantic Kernel agent here: result = agent.run(user_input) 
        time.sleep(0.5) # Simulate agent work
        result = f"Agent {agent_name} processed: '{user_input}'"
        # --- End Semantic Kernel Logic ---
        
        # Increment the custom counter
        AGENT_INVOCATION_COUNTER.labels(agent_name=agent_name).inc()

        # Observe the custom histogram with the actual execution time
        AGENT_EXECUTION_TIME.labels(agent_name=agent_name).observe(time.time() - start_time)
        
        return jsonify({"result": result})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)