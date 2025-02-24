# Peanut-Butter-Payroll-Backend
a FastAPI application for peanut butter payroll using Postgres and Jenkins for deployment

## Table of Contents
- [Peanut-Butter-Payroll-Backend](#peanut-butter-payroll-backend)
  - [Table of Contents](#table-of-contents)
  - [Installation](#installation)
    - [Local Setup](#local-setup)
    - [Frontend Setup](#frontend-setup)
    - [Docker Setup](#docker-setup)
  - [Using the application](#using-the-application)
  - [Tools and Justifications](#tools-and-justifications)

## Installation

### Local Setup

1. **Create a virtual environment and install dependencies:**

```sh
make venv
make install-packages
```

2. **Make migrations and migrate the database:**

```sh
make makemigrations
make migrate
```

3. **Run the application locally:**

```sh
make run-local
Make migrations and migrate the database:
```

### Docker Setup
Install Docker and Docker Compose if you haven't already.
(Install Docker)[https://docs.docker.com/engine/install/]

1. **Docker Setup**
Build and run Docker containers:

```sh
make up
```

2. **Destroy Docker containers:**

```sh
make down
```

3. **View logs:**

```sh
make logs
```

4. **Make migrations and migrate the database within Docker (if needed):**
(Migrations have been made and application migrates when it starts up.)

```sh
make docker-makemigrations
make docker-migrate
```

## Using the application

1. **Open the application in your browser:**
   For the FastAPI application OpenAPI docs: [http://localhost:8000/docs](http://localhost:8000/docs)

    For the Next.js application: [http://localhost:3000](http://localhost:3000)

    For PGAdmin: [http://localhost:5050](http://localhost:5050) this is used to view and add data to the database manually.

    To create mock data for the database navigation to the FastAPI application OpenAPI docs and use the `POST /items/create_mock_data/generate-mock-data/` endpoint or click on the 'Create Mock Data' button on the Next.js application.

## Tools and Justifications

- **FastAPI**: FastAPI is a modern, fast (high-performance), web framework for building APIs with Python 3.7+ based on standard Python type hints. It is easy to use, fast to develop with, and provides automatic interactive API documentation.
- **OpenAPI**: OpenAPI is a specification for building APIs. Comes standard with FastAPI.
- **PostgreSQL**: PostgreSQL is a powerful, open-source relational database management system that is widely used in production environments.
- **SQLAlchemy**: SQLAlchemy is a popular SQL toolkit and Object-Relational Mapping (ORM) library for Python. I feel like using an ORM will make it easier to interact with the database and write queries especially for other developers who may not be familiar with SQL.
- **asyncpg**: asyncpg is a fast PostgreSQL database client library for Python. It is designed for use with the async/await syntax and provides support for asynchronous I/O operations.
- **React**: React is a popular JavaScript library for building user interfaces.
- **NextJS**: The React website recommends using a framework for building React applications, and Next.js is a popular choice that provides a lot of useful features out of the box.
- **Tailwind CSS**: Tailwind CSS is a utility-first CSS framework that provides a set of pre-built utility classes that can be used to style web applications. It is easy to use and provides a flexible way to style web applications.
- **Docker**: Docker is a popular tool for building, shipping, and running applications in containers. It provides a lightweight and portable way to package applications and their dependencies, which makes it easy to deploy applications in different environments.
- **Redis**: Redis is an in-memory data store that can be used to cache data and speed up applications. It is a popular choice for caching data in web applications and can be used to store the results of sentiment analysis requests.
- **ReactQuery**: ReactQuery is a popular library for managing server state in React applications. It provides a way to fetch and cache data from a server and keep it in sync with the UI.
- **Axios**: Axios is a popular library for making HTTP requests in JavaScript. It provides a simple and flexible way to make requests to a server and handle responses.
- **TypeScript**: TypeScript is a popular superset of JavaScript that provides static typing and other features to help developers write more robust and maintainable code. It is widely used in the React ecosystem and provides a lot of benefits for building web applications.
