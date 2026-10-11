# GenStudio AI — Cloud-Deployed Generative AI Platform

**Generate stunning AI images from text prompts using Stable Diffusion, with a modern full-stack application and cloud-native DevOps infrastructure.**

![Python](https://img.shields.io/badge/Python-3.11+-blue?logo=python)
![React](https://img.shields.io/badge/React-TypeScript-blue?logo=react)
![FastAPI](https://img.shields.io/badge/FastAPI-Backend-009688?logo=fastapi)
![Docker](https://img.shields.io/badge/Docker-Containerization-2496ED?logo=docker)
![Kubernetes](https://img.shields.io/badge/Kubernetes-Orchestration-326CE5?logo=kubernetes)
![Terraform](https://img.shields.io/badge/Terraform-IaC-844FBA?logo=terraform)
![License](https://img.shields.io/badge/License-MIT-green)

## Overview

GenStudio AI is a full-stack text-to-image generation platform that transforms natural-language prompts into AI-generated images using Stable Diffusion.

The project combines generative AI with modern software engineering, cloud infrastructure, CI/CD automation, container orchestration, and observability. It is designed to demonstrate practical skills relevant to Cloud DevOps, MLOps, Generative AI, and Software Engineering roles.

Users can submit prompts, configure generation parameters, track generation jobs, preview generated images, and access their image history through a responsive web interface.

## Key Features

- **AI Image Generation:** Generate images from text prompts using a Stable Diffusion inference backend.
- **Prompt Configuration:** Support positive prompts, negative prompts, seeds, image dimensions, and inference steps where supported by the selected model.
- **Asynchronous Processing:** Execute long-running generation jobs in background workers.
- **Job Tracking:** Monitor pending, running, completed, and failed jobs.
- **Image Gallery:** Preview and download generated images.
- **REST API:** Expose documented endpoints through FastAPI.
- **Containerization:** Package application services using Docker.
- **CI/CD Automation:** Automate linting, testing, builds, and image publishing through GitHub Actions.
- **Infrastructure as Code:** Define cloud infrastructure using Terraform.
- **Kubernetes Deployment:** Deploy services with Kubernetes manifests and Helm charts.
- **Monitoring and Observability:** Track application health, request latency, failures, job duration, and resource utilization through Prometheus and Grafana.
- **Demo Mode:** Support development and UI testing without requiring a GPU, if the demo provider is enabled in the implementation.

## Architecture

```mermaid
flowchart TD
    A[User] --> B[React Frontend]
    B --> C[FastAPI Backend]
    C --> D[Redis Job Queue]
    D --> E[Background Worker]
    E --> F[Stable Diffusion Model]
    C --> G[(PostgreSQL)]
    E --> H[Image Storage]
    C --> I[Prometheus Metrics]
    E --> I
    I --> J[Grafana Dashboard]
    K[GitHub Actions] --> L[Docker Image Registry]
    L --> M[Kubernetes Deployment]
    N[Terraform] --> M
```

The frontend communicates with the backend through REST APIs. The backend validates requests, records job metadata, and schedules image-generation tasks. Background workers execute model inference and store generated images. Infrastructure and delivery automation support repeatable deployment and monitoring.

*The diagram represents the intended architecture. Remove components that are not yet implemented in your repository.*

## Technology Stack

| Component | Technologies |
|---|---|
| Frontend | React, TypeScript, Vite, Tailwind CSS |
| Backend | Python, FastAPI |
| AI Model | Stable Diffusion, TensorFlow/Keras-compatible inference |
| Background Jobs | Redis, Celery or equivalent worker |
| Database | PostgreSQL |
| Image Storage | Local storage for development; Amazon S3 for production |
| Containerization | Docker, Docker Compose |
| CI/CD | GitHub Actions; Jenkins can be added as an alternative |
| Infrastructure as Code | Terraform |
| Cloud | AWS |
| Orchestration | Kubernetes, Amazon EKS, Helm |
| Monitoring | Prometheus, Grafana |
| Testing | Pytest and frontend testing tools |

The exact inference framework and package versions must be selected based on model compatibility and the target hardware.

## Project Structure

```text
genstudio-ai/
├── frontend/                   # React web application
├── backend/
│   ├── api/                    # FastAPI endpoints
│   ├── worker/                 # Background processing
│   └── inference/              # Stable Diffusion integration
├── experiments/
│   ├── stable_diffusion.ipynb
│   └── benchmark.py
├── tests/                      # Automated tests
├── infra/
│   └── terraform/              # Cloud infrastructure
├── deploy/
│   └── helm/                   # Kubernetes Helm charts
├── monitoring/
│   ├── prometheus/
│   └── grafana/
├── .github/
│   └── workflows/              # CI/CD pipelines
├── docker-compose.yml
├── Dockerfile
├── .env.example
├── .gitignore
└── README.md
```

Adjust this tree to match the actual repository structure.

## Getting Started

### Prerequisites

Install the following tools:

- Git
- Python 3.11 or a version supported by your dependencies
- Node.js and npm
- Docker and Docker Compose
- A compatible Stable Diffusion model and sufficient compute resources for real inference

Terraform, AWS CLI, `kubectl`, and Helm are required only when working on cloud infrastructure and Kubernetes deployment.

### 1. Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/genstudio-ai.git
cd genstudio-ai
```

Replace the repository URL with your actual GitHub repository.

### 2. Configure Environment Variables

Create a local environment file from the example:

```bash
cp .env.example .env
```

Configure the variables required by your implementation. For example:

```dotenv
APP_ENV=development
API_HOST=0.0.0.0
API_PORT=8000

DATABASE_URL=postgresql://postgres:postgres@localhost:5432/genstudio
REDIS_URL=redis://localhost:6379/0

INFERENCE_MODE=demo
MODEL_ID=
AWS_REGION=ap-south-1
S3_BUCKET_NAME=
```

These names are illustrative; use the variables defined by your application.

**Security:** Never commit `.env`, AWS credentials, database passwords, API keys, or other secrets to Git. Use secure secret management for deployed environments.

### 3. Run with Docker Compose

If Docker Compose is configured to start all required services:

```bash
docker compose up --build
```

Check the service logs:

```bash
docker compose logs -f
```

Stop the application:

```bash
docker compose down
```

The exact services started depend on your Compose configuration.

### 4. Run the Backend Locally

If you prefer to run the backend outside Docker:

```bash
cd backend
python -m venv .venv
```

Activate the virtual environment.

**Windows PowerShell:**

```powershell
.venv\Scripts\Activate.ps1
```

**Linux/macOS:**

```bash
source .venv/bin/activate
```

Install the backend dependencies using the dependency file provided by the project:

```bash
pip install -r requirements.txt
```

Start the API using the appropriate application module. For example:

```bash
uvicorn api.main:app --reload --host 0.0.0.0 --port 8000
```

The import path may need to be adjusted to match your actual backend structure.

### 5. Run the Frontend Locally

Open a separate terminal:

```bash
cd frontend
npm install
npm run dev
```

Open the local URL printed by Vite, commonly `http://localhost:5173`.

### 6. Access the API Documentation

When FastAPI is running, open:

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`
- Health endpoint: `http://localhost:8000/health`

The documentation and health endpoint URLs depend on your API configuration.

## AI Inference

The project is based on the concepts introduced in the official TensorFlow Stable Diffusion tutorial:

https://www.tensorflow.org/tutorials/generative/generate_images_with_stable_diffusion

The inference workflow generally includes:

1. Accept a text prompt and generation settings.
2. Convert the prompt into text embeddings.
3. Initialize the latent representation.
4. Iteratively denoise the latent representation using the diffusion model.
5. Decode the final latent representation into an image.
6. Store the output and return its location to the application.

### Inference Modes

**Demo mode**

Allows developers to test the interface and job lifecycle without loading a real diffusion model. A demo response must be clearly identified as simulated output and must not be presented as a genuine AI-generated result.

**Real inference mode**

Loads a compatible Stable Diffusion implementation and performs actual model inference. GPU acceleration may be necessary for practical response times, depending on the model and image settings.

The tutorial uses a particular TensorFlow/KerasCV workflow. Validate dependency compatibility before reusing its code in a production service. Keep model inference isolated behind an adapter so the backend can evolve independently of the model implementation.

## API Endpoints

The following is an example API contract. Implemented endpoints and request fields should be documented according to the actual code.

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/health` | Check application health |
| GET | `/ready` | Check readiness and required dependencies |
| POST | `/api/v1/generations` | Submit an image-generation job |
| GET | `/api/v1/generations/{job_id}` | Retrieve job status |
| GET | `/api/v1/generations` | List generation history |
| GET | `/api/v1/generations/{job_id}/image` | Retrieve or download the generated image |

Example request:

```bash
curl -X POST http://localhost:8000/api/v1/generations \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "A futuristic city at sunset, cinematic lighting",
    "negative_prompt": "blurry, low quality",
    "steps": 25,
    "seed": 42
  }'
```

Example response:

```json
{
  "job_id": "example-job-id",
  "status": "queued"
}
```

The response is illustrative. Actual fields and supported parameters depend on the implementation.

## Docker and Containerization

Docker packages the frontend, backend, and worker into reproducible application environments.

The containerization workflow should:

- Use appropriate base images and pinned dependencies.
- Separate services when they have different runtime requirements.
- Avoid running containers as root when feasible.
- Use health checks and appropriate shutdown behavior.
- Keep secrets outside container images.
- Avoid bundling large model weights into application images unless explicitly required.
- Configure resource limits and persistent storage appropriately.

Build
