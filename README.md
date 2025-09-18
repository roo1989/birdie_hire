# Backend Engineer Technical Interview Case Study

## Objective

The goal of this case study is to evaluate the candidate's ability to design, implement, and test a robust backend system using the specified tech stack. The focus is on practical skills, system design, code quality, and the effective use of asynchronous processing and real-time communication.

## Problem Statement: The "Event Horizon" Service

Design and implement a microservice named "Event Horizon" that processes large log files. The service will accept file uploads, process them asynchronously, and provide real-time status updates to the user.

A user will upload a `.jsonl` file (a newline-delimited JSON file) containing log events. The service should:

1.  Store the uploaded file.
2.  Queue a background task to parse and analyze the file.
3.  Persist the parsed data into a database.
4.  Notify the user of the processing status in real time.

## Core Requirements

The candidate must implement a working solution that satisfies the following:

### 1. REST API with FastAPI & Pydantic

- **POST `/api/v1/files/upload`**: Accepts a file upload (`.jsonl`).
  - Validates the file format and size.
  - Stores the file in MinIO (S3). (NOTE: MinIO works with any s3 compatible SDK, like `boto`)
  - Creates a record in the Postgres database with the file metadata (name, size, status: 'queued').
  - Sends a message to RabbitMQ to queue a processing task.
  - Returns a `202 Accepted` response with a unique `job_id`.

- **GET `/api/v1/jobs/{job_id}`**: Returns the current status of a processing job (e.g., 'queued', 'processing', 'completed', 'failed').

### 2. Asynchronous Task Processing with Dramatiq & RabbitMQ

- Create a Dramatiq (or Celery) worker that consumes messages from the RabbitMQ queue.
- The worker should:
  - Fetch the file from MinIO using the file path provided in the message.
  - Read the `.jsonl` file line by line.
  - Add a random delay of 0-1 second between each line.
  - Parse each line as a JSON object and validate its structure using a Pydantic model (e.g., `LogEntry`).
  - Ingest the valid log entries into the Postgres database.
  - Update the job status in the database (e.g., 'processing', 'completed', 'failed').

### 3. Data Persistence with Postgres & SQLAlchemy

- Use SQLAlchemy to define the data models for `Job` and `LogEntry`.
- `Job` model should include fields like `job_id`, `file_name`, `status`, `created_at`, and `completed_at`.
- `LogEntry` model should reflect the data within the `.jsonl` file.

### 4. Real-time Communication with WebSockets

- Implement a WebSocket endpoint at `/ws/jobs/{job_id}`.
- When a client connects to this endpoint, the backend should send real-time updates on the processing status of the specified `job_id`.
- The backend worker should trigger these updates at key stages (e.g., 'started processing', '10% complete', '50% complete', 'completed').
- [ALTERNATIVELY]: If you have problems implementing the websocket, implement a simple get request to get the status

## Bonus/Stretch Goals (Not mandatory, but highly valued)

- **Error Handling**: Implement robust error handling for common failure scenarios (e.g., file not found in MinIO, invalid JSON format, database connection failure).
- **Testing**: Write appropriate tests for the FastAPI endpoints and the Dramatiq worker function using a framework like `pytest`.
- **Containerization**: Provide a `Dockerfile` for the FastAPI service and the Dramatiq worker, and implement in the docker compose file.
- **GraphQL**: Implement a simple GraphQL query to fetch the status of a job.
- **Documentation**: Provide clear documentation for the API endpoints using a tool like OpenAPI/Swagger UI (which FastAPI provides out-of-the-box).
- **DB Migration:** Demonstrate a basic understanding of database migrations using **Alembic** by providing a migration script to create the initial tables.
- **Basic Auth:** Write down thoughts about an authorization approach that would be appropriate for such an app

## Evaluation Criteria

The candidate will be evaluated on the following aspects:

- **Python Proficiency**: Clean, readable, and idiomatic Python code following PEP 8.
- **FastAPI & Pydantic**: Correct use of decorators, request/response models, and dependency injection.
- **System Design**: The logical separation of concerns between the API, the database, and the background worker. The ability to articulate and justify design choices.
- **Database Interaction**: Proper use of SQLAlchemy for ORM and Alembic for migrations.
- **Asynchronous Processing**: Correct implementation of a message queue with Dramatiq and RabbitMQ.
- **Problem-Solving**: The approach to solving the problem, including handling edge cases and errors.
- **Communication (At Interview)**: The ability to clearly explain the code, its architecture, and the trade-offs made during development.
- **Bonus Points**: Completion of any of the stretch goals, demonstrating a deeper understanding of the full software development lifecycle (e.g., testing, deployment, CI/CD).

The case is designed to be quite extensive, and we do _not_ expect you to finish the entire case, so use you time wisely. If you have any thoughts or ideas that you would like to share, please add them in the `NOTES.md` file. You might have a good idea for eg. a testing approach, but not enough time to actually implement it.

## Getting Started

We have provided a Docker Compose file `docker-compose.yml` containing the services you will need (MinIO, RabbitMQ and Postgress). To start the services, run:
`docker compose up -d`

We use `uv` as our prefered packagemanager. We would prefer you to do the same, but if you are unfamiliar, you can use good old `pip`.

To get started `fork` this repo, and start working. When the time is up, please send a public link to the repo to the communication details provided to you.
