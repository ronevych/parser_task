# Social Parser System 🚀

A robust ETL system built with Django, Celery, and Docker. It parses Users, Posts, and Comments from external APIs (JSONPlaceholder, DummyJSON), stores them in a normalized PostgreSQL database, and provides a REST API to view the data.

## 🛠 Tech Stack

* **Core:** Python 3.12, Django 6.0
* **API:** Django REST Framework (DRF), Drf-Spectacular (Swagger)
* **Async & ETL:** Celery, Redis, Celery Beat
* **Database:** PostgreSQL
* **Infrastructure:** Docker, Docker Compose
* **QA:** Pytest, Flake8, Black, Isort, Requests-Mock

## ✨ Features

* **Microservices Architecture:** Fully dockerized environment.
* **Smart ETL Strategy:**
    * **Strict Consistency:** Posts are fetched only for existing users.
    * **Efficient Parsing:** Comments are fetched only for existing posts (saving bandwidth).
    * **Atomic Transactions:** Ensures data integrity.
* **Automated Scheduling:** Periodic tasks run automatically via Celery Beat.
* **REST API:** Fully documented endpoints with filtering, searching, and pagination.

## 🚀 How to Run

1.  **Clone the repository:**
    ```bash
    git clone <your-repo-url>
    cd parser_system
    ```

2.  **Create `.env` file:**
    ```bash
    cp .env.example .env
    # Or just use the defaults in docker-compose for local dev
    ```

3.  **Build and Run with Docker:**
    ```bash
    docker-compose up -d --build
    ```

4.  **Access the Application:**
    * **Swagger UI (API Docs):** [http://127.0.0.1:8000/api/schema/swagger-ui/](http://127.0.0.1:8000/api/schema/swagger-ui/)
    * **Admin Panel:** [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)

## 🧪 Running Tests & Quality Checks

Run all tests inside the docker container:

```bash
# Run Unit & Integration Tests
docker-compose exec web pytest

# Check Code Style (Black & Isort)
docker-compose exec web black . --check
docker-compose exec web isort . --check-only

# Run Linter (Flake8)
docker-compose exec web flake8