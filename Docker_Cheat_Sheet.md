# Docker Cheat Sheet

## 1. Core mental model

- **Image** = blueprint/template for a container.
- **Container** = a running instance of an image.
- **Dockerfile** = instructions for building an image.
- **Volume** = persistent storage outside the container lifecycle.
- **Port mapping** = connects a host port to a container port.
- **Docker Compose** = defines and runs multiple services together.
- **Registry** = place where images are stored/downloaded, such as Docker Hub.

Typical project:

    docker-compose.yml
          |
          +-- backend container
          |
          +-- database container

## 2. Check Docker installation

    docker --version
    docker compose version

Check whether Docker is running:

    sudo systemctl status docker

Start Docker:

    sudo systemctl start docker

Enable Docker at boot:

    sudo systemctl enable docker

## 3. Basic Docker commands

List running containers:

    docker ps

List all containers, including stopped ones:

    docker ps -a

List local images:

    docker images

Download an image:

    docker pull postgres:15-alpine

Run a container:

    docker run IMAGE

Run in the background:

    docker run -d IMAGE

Give a container a name:

    docker run --name my-container IMAGE

Stop a container:

    docker stop CONTAINER

Start an existing stopped container:

    docker start CONTAINER

Restart a container:

    docker restart CONTAINER

Remove a stopped container:

    docker rm CONTAINER

Remove an image:

    docker rmi IMAGE

## 4. Ports

Map host port 8000 to container port 8000:

    docker run -p 8000:8000 IMAGE

Meaning:

    your-computer:8000 -> container:8000

Example:

    http://localhost:8000

List ports currently used by containers:

    docker ps

If you get:

    address already in use

another process is already using that host port.

Find what is using a port:

    sudo ss -ltnp | grep :5432

## 5. Docker logs and debugging

View container logs:

    docker logs CONTAINER

Follow logs live:

    docker logs -f CONTAINER

Show the last 100 lines:

    docker logs --tail 100 CONTAINER

Open a shell inside a running container:

    docker exec -it CONTAINER sh

For images that contain bash:

    docker exec -it CONTAINER bash

Run a command inside a container:

    docker exec CONTAINER COMMAND

Example:

    docker exec taskflow_db pg_isready -U taskflow -d taskflow_db

Inspect a container:

    docker inspect CONTAINER

Check container resource usage:

    docker stats

## 6. Dockerfile essentials

A Dockerfile describes how an image should be built.

Example:

    FROM python:3.12-slim

    WORKDIR /app

    COPY requirements.txt .

    RUN pip install --no-cache-dir -r requirements.txt

    COPY . .

    CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

Important instructions:

### FROM

Selects the base image.

    FROM python:3.12-slim

### WORKDIR

Sets the working directory inside the image/container.

    WORKDIR /app

### COPY

Copies files from your project into the image.

    COPY requirements.txt .

    COPY . .

### RUN

Runs a command while building the image.

    RUN pip install -r requirements.txt

### CMD

Default command when the container starts.

    CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

### EXPOSE

Documents which port the application uses.

    EXPOSE 8000

It does NOT publish the port by itself. Port publishing is normally done with `-p` or Compose.

## 7. Build an image

Build from the Dockerfile in the current directory:

    docker build -t my-app .

`-t` gives the image a name/tag.

List images:

    docker images

Run it:

    docker run -p 8000:8000 my-app

## 8. Rebuild after Dockerfile changes

    docker build -t my-app .

Or with Compose:

    docker compose build

Build and start:

    docker compose up --build

## 9. Docker Compose essentials

Start services:

    docker compose up

Start in background:

    docker compose up -d

Build and start:

    docker compose up --build

Stop services:

    docker compose stop

Stop and remove containers/networks created by Compose:

    docker compose down

Show Compose containers:

    docker compose ps

Show Compose logs:

    docker compose logs

Follow logs:

    docker compose logs -f

Logs for one service:

    docker compose logs backend

Restart a service:

    docker compose restart backend

Build a specific service:

    docker compose build backend

Run a one-off command:

    docker compose run --rm backend COMMAND

Example:

    docker compose run --rm backend alembic init alembic

Execute a command in an already-running service:

    docker compose exec backend COMMAND

Open a shell:

    docker compose exec backend sh

## 10. Compose service names and networking

If Compose has:

    services:
      db:
      backend:

The backend can normally reach the database using:

    db

not:

    localhost

Example:

    DATABASE_URL=postgresql+asyncpg://taskflow:password@db:5432/taskflow_db

Inside a container:

    localhost

means the current container itself.

The Compose service name:

    db

means the database container/service.

## 11. Environment variables

Pass an environment variable:

    docker run -e APP_ENV=development IMAGE

In Compose:

    environment:
      APP_ENV: development

Or:

    environment:
      - APP_ENV=development

A `.env` file can store configuration:

    DATABASE_URL=postgresql+asyncpg://...

Then Compose can read variables from it.

Important:

- Do not commit secrets such as real passwords or API keys.
- Add `.env` to `.gitignore` when appropriate.
- Prefer environment variables or a proper secret-management system for sensitive configuration.

## 12. Volumes

List volumes:

    docker volume ls

Inspect a volume:

    docker volume inspect VOLUME

Remove a volume:

    docker volume rm VOLUME

Compose example:

    volumes:
      postgres_data:

    services:
      db:
        volumes:
          - postgres_data:/var/lib/postgresql/data

The important idea:

    container removed
          |
          v
    volume can remain
          |
          v
    database data survives

WARNING:

    docker compose down -v

can remove Compose-managed volumes.

For databases, be careful with `-v`.

## 13. Bind mounts

A bind mount maps a local directory into a container.

Example:

    volumes:
      - ./backend:/app

Meaning:

    local ./backend -> container /app

This is useful during development because code changes on your computer can appear inside the container.

## 14. Container lifecycle

Typical lifecycle:

    Dockerfile
        |
        v
      build
        |
        v
      image
        |
        v
       run
        |
        v
    container
        |
        +--> stop
        |
        +--> start
        |
        +--> remove

A stopped container is not automatically deleted.

## 15. Docker Compose lifecycle

Typical development workflow:

    docker compose up -d

Check:

    docker compose ps

Read logs:

    docker compose logs -f

Stop:

    docker compose down

If code/build configuration changed:

    docker compose up --build -d

## 16. PostgreSQL with Docker

Example Compose service:

    services:
      db:
        image: postgres:15-alpine
        environment:
          POSTGRES_USER: taskflow
          POSTGRES_PASSWORD: taskflow_secret
          POSTGRES_DB: taskflow_db
        volumes:
          - postgres_data:/var/lib/postgresql/data
        ports:
          - "5432:5432"

Inside the Compose network, the backend connects to:

    db:5432

From your host machine, if port 5432 is published:

    localhost:5432

These are different connection contexts.

## 17. Healthchecks

A healthcheck tests whether a service is actually ready.

Example:

    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U taskflow -d taskflow_db"]
      interval: 5s
      timeout: 5s
      retries: 5

Compose can wait for a healthy dependency:

    depends_on:
      db:
        condition: service_healthy

## 18. Useful inspection commands

Container details:

    docker inspect CONTAINER

Image history:

    docker history IMAGE

Docker system information:

    docker info

Disk usage:

    docker system df

List Docker networks:

    docker network ls

Inspect a network:

    docker network inspect NETWORK

## 19. Cleanup

Remove stopped containers:

    docker container prune

Remove unused images:

    docker image prune

Remove unused volumes:

    docker volume prune

Remove unused networks:

    docker network prune

General cleanup:

    docker system prune

More aggressive cleanup:

    docker system prune -a

WARNING:

Prune commands delete unused Docker resources. Always understand what is being removed before using them, especially volumes containing database data.

## 20. Common problems

### "Permission denied"

Your user may not have Docker permissions, or a generated file may be owned by root.

Check ownership:

    ls -l FILE

For a project file owned by root, you can change ownership:

    sudo chown -R $USER:$USER PROJECT_DIRECTORY

Be careful with recursive ownership changes on system directories.

### "address already in use"

A host port is already occupied.

Check:

    sudo ss -ltnp | grep :5432

Then either stop the process using that port or choose another host port.

### Container exits immediately

Check:

    docker logs CONTAINER

### Container is unhealthy

Check:

    docker ps

Then:

    docker inspect --format='{{json .State.Health}}' CONTAINER

And:

    docker logs CONTAINER

### Backend cannot connect to database

Check:

1. Is the database container running?
2. Is it healthy?
3. Is the database URL correct?
4. Are you using the Compose service name instead of localhost?

For example:

    @db:5432

rather than:

    @localhost:5432

when the backend is inside Compose.

### Changes are not appearing

If using a bind mount, check that the mount is correct.

If the change affects the image/Dockerfile:

    docker compose up --build

## 21. Docker vs local development

You do NOT have to use Docker for every project.

Local development:

    Python venv
      |
      +-- FastAPI
      +-- dependencies
      +-- local PostgreSQL

Docker development:

    Docker
      |
      +-- backend container
      +-- PostgreSQL container

Docker is especially useful when a project has multiple services or needs a reproducible environment.

## 22. Commands worth memorizing first

Do not try to memorize everything.

Start with:

    docker --version
    docker ps
    docker ps -a
    docker images
    docker logs CONTAINER
    docker exec -it CONTAINER sh
    docker build -t IMAGE .
    docker run -p HOST:CONTAINER IMAGE

For Compose:

    docker compose up -d
    docker compose up --build
    docker compose ps
    docker compose logs -f
    docker compose exec SERVICE sh
    docker compose run --rm SERVICE COMMAND
    docker compose down

## 23. TaskFlow-specific workflow

Start TaskFlow:

    docker compose up -d

Check services:

    docker compose ps

Watch backend logs:

    docker compose logs -f backend

Watch database logs:

    docker compose logs -f db

Run Alembic:

    docker compose run --rm backend alembic COMMAND

Enter the backend container:

    docker compose exec backend sh

Stop TaskFlow:

    docker compose down

If the Dockerfile or dependencies changed:

    docker compose up --build -d

## 24. The most important mental model

Remember these relationships:

    Dockerfile
        ↓ build
      Image
        ↓ run
    Container

And:

    docker-compose.yml
        ↓
    multiple services
        ↓
    backend + database + other services

And:

    volume
        ↓
    persistent data

And:

    port mapping
        ↓
    host <-> container communication

And:

    service name
        ↓
    container-to-container communication

For your current project, you do not need to master every Docker feature. Learn these concepts while building TaskFlow, then use this cheat sheet as a reference when you encounter something unfamiliar.
