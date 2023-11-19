FROM python:3.9

WORKDIR /app

# Copy the .env file into the /app directory
COPY ./.env /app/.env

# Copy the requirements.txt file and install dependencies
COPY ./requirements.txt ./requirements.txt
RUN pip install --no-cache-dir --upgrade -r ./requirements.txt

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONBUFFERED 1

# Add the project root directory to the PYTHONPATH
ENV PYTHONPATH /app:/app/app:${PYTHONPATH}

# Copy the app code into the container
COPY ./app ./app

# Copy Alembic files
COPY ./alembic.ini /app/alembic.ini
COPY ./app/alembic /app/alembic

# Command to run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
