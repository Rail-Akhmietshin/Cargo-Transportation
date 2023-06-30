

## Deployment with Docker

After cloning the repository, grant write permissions for the root and its incoming files and folders:

* chmod -R 755 (your path to the root folder)

Starting the project build:

* docker-compose up -d --build

After successfully running the project in Docker, application will be available at:

* http://localhost:8000

* All routes are available on http://localhost:8000/docs or http://localhost:8000/redoc paths with Swagger or ReDoc.
