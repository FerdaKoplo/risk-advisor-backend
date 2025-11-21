# Risk Advisor Backend — README

This README explains how to set up and run the **risk-advisor-backend** locally. It includes instructions for database migrations, running the backend, testing endpoints, and setting up Ollama with Llama 3.2 locally.

---

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Clone Repository & Create Virtual Environment](#clone-repository--create-virtual-environment)
3. [Environment Variables](#environment-variables)
4. [Install Dependencies](#install-dependencies)
5. [Database Setup with Flask-Migrate](#database-setup-with-flask-migrate)
6. [Seeding Initial Data](#seeding-initial-data)
7. [Running the Application](#running-the-application)
8. [Testing Endpoints](#testing-endpoints)
9. [Ollama Local Setup & Llama 3.2](#ollama-local-setup--llama-32)
10. [Machine Learning and Rule-Based Fallback](#machine-learning-and-rule-based-fallback)
11. [Troubleshooting](#troubleshooting)
12. [References](#references)

---

## Prerequisites

* Python 3.10 or higher
* Git
* Ollama CLI installed
* Sufficient disk space and memory for running Llama 3.2 locally

---

## Clone Repository & Create Virtual Environment

```bash
git clone https://github.com/FerdaKoplo/risk-advisor-backend.git
cd risk-advisor-backend

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # macOS / Linux

# Windows PowerShell
# .\.venv\Scripts\Activate.ps1
```

---

## Environment Variables

Copy the example environment file and update values as needed:

```bash
cp .env.example .env
```

Update the `.env` file with appropriate values (example values shown):

```
FLASK_APP=run.py
FLASK_ENV=development
DATABASE_URL=sqlite:///instance/app.db
SECRET_KEY=your_secret_key_here
OLLAMA_URL=http://127.0.0.1:11434
```

---

## Install Dependencies

```bash
pip install --upgrade pip setuptools wheel
pip install -r requirement.txt
```

---

## Database Setup with Flask-Migrate

Set environment variables and activate your virtual environment:

```bash
export FLASK_APP=run.py
export FLASK_ENV=development
source .venv/bin/activate
```

For Windows PowerShell:

```powershell
$env:FLASK_APP="run.py"
$env:FLASK_ENV="development"
.\.venv\Scripts\Activate.ps1
```

Apply database migrations:

```bash
flask db upgrade
```

If you need to create migrations for model changes:

```bash
flask db migrate -m "migration message"
flask db upgrade
```

---

## Seeding Initial Data

Populate tables such as `RiskFactorDefinition` and `RiskMatrixRule`:

```bash
python seed.py
```

---

## Running the Application

Run the Flask application (development):

```bash
flask run --host=0.0.0.0 --port=5000
# or
python run.py
```

The backend will be accessible at `http://127.0.0.1:5000`.

---

## Testing Endpoints

### `calculate` endpoint

```bash
curl -X POST http://127.0.0.1:5000/api/risk/calculate \
  -H "Content-Type: application/json" \
  -d '{
    "employee_id": "E123",
    "location_area": "Warehouse 1",
    "prob_input": "medium",
    "sev_input": "high",
    "comp_input": "low"
  }'
```

### `safety-advice` endpoint

```bash
curl -X POST http://127.0.0.1:5000/api/ai/safety-advice \
 -H "Content-Type: application/json" \
 -d '{
   "employee_id": "E123",
   "location_area": "Warehouse 1",
   "prob_input": "medium",
   "sev_input": "high",
   "comp_input": "low"
 }'
```

---

## Ollama Local Setup & Llama 3.2

### Install Ollama

* **macOS**: download the installer from Ollama website.
* **Linux**: install via:

```bash
curl -fsSL https://ollama.com/install.sh | sh
```

* **Windows**: download and run the installer from the Ollama website.

### Pull and Run Llama 3.2

```bash
# Pull the model
ollama pull llama3.2

# Run interactively (optional)
ollama run llama3.2

# Start the Ollama server to expose a local HTTP endpoint
ollama serve
```

Default server URL: `http://127.0.0.1:11434`.

Confirm the model is available:

```bash
ollama list
ollama show llama3.2
```

> **Note:** Running Llama 3.2 locally requires significant disk space and memory. Make sure your machine meets the requirements.

---

## Machine Learning and Rule-Based Fallback

* `RiskService` trains a `RandomForestClassifier` from labeled `RiskAssessment` data stored in the database.
* If the ML model is unavailable, the service calculates risk using `RiskMatrixRule` based on the calculated score.
* The ML model is saved to `risk_model.pkl` and automatically loaded when predictions are required.

---

## Troubleshooting

* **No migrations detected**: Ensure models are imported in the `FLASK_APP` entry point so Flask-Migrate can detect them.
* **Ollama HTTP errors**: Confirm `ollama serve` is running and accessible at the URL specified in your `.env` file.
* **Model download issues**: Ensure you have sufficient disk space for Llama 3.2.

---

## References

* Ollama CLI Documentation
* Llama 3.2 Model
* Flask-Migrate Documentation

---

*If you want this saved as a `README.md` file in the repo or want edits (more examples, badges, or CI instructions), tell me what to change and I’ll update it.*
