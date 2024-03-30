# BlogApp

Welcome to the Django BlogApp! This is a simple Django application that allows users to create, read, update, and delete blog posts.

## Prerequisites

Before you begin, make sure you have Docker and Docker Compose installed on your system.

- Docker: [Install Docker](https://docs.docker.com/get-docker/)
- Docker Compose: [Install Docker Compose](https://docs.docker.com/compose/install/)

## Setup Instructions

1. Clone the repository:

    ```bash
    git clone https://github.com/alizahedi7/BlogApp.git
    ```

2. Navigate to the project directory:

    ```bash
    cd BlogApp
    ```

3. Configure Environment Variables

    Create a `.env` file in the root directory of the project and specify the required environment variables. For example:

    ```plaintext
    DEBUG=True
    SECRET_KEY=your_secret_key
    ALLOWED_HOSTS=localhost 127.0.0.1 [::1]
    DB_ENGINE=django.db.backends.postgresql
    DB_NAME=blog_db
    DB_USER=blog_user
    DB_PASSWORD=blog_password
    DB_HOST=db
    DB_PORT=5432
    ```

4. Build the Docker images:

    ```bash
    docker-compose build
    ```

5. Start the Docker containers:

    ```bash
    docker-compose up -d
    ```

The application should now be running. You can access it at [http://localhost:8000/](http://localhost:8000/).

## Generating Fake Data

You can generate fake data for testing purposes using the provided management command. Follow these steps:

1. Access the Docker container running the Django application using the following command:

    ```bash
    docker-compose exec web bash
    ```

2. Once inside the container, run the management command to seed the database with fake data:

    ```bash
    python manage.py seed_db
    ```

This command will generate 10 instances of posts and 10 comments for each post in the database.

## Accessing API Documentation

You can explore the API documentation to understand the endpoints and their functionalities. Follow these steps to access the API documentation:

1. Ensure that the Docker containers are running.
2. Open your web browser and navigate to the following URL:

    [http://0.0.0.0:8000/api/ninja/docs#/](http://0.0.0.0:8000/api/ninja/docs#/)

This URL will take you to the Swagger UI interface, where you can interactively explore and test the available API endpoints.

## Additional Notes

- If you make any changes to the Docker configuration or environment variables, you may need to rebuild the Docker images using `docker-compose build`.

- You can stop the Docker containers by running `docker-compose down`.

- For more detailed logs, you can check the logs of individual containers using `docker-compose logs [container_name]`.

- Integration with GitHub Actions is included in the repository for automated testing and deployment. Make sure to configure your GitHub repository accordingly.