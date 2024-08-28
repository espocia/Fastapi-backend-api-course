# Use the official Python image from the Docker Hub
FROM python:3.9

# Set the working directory in the container
WORKDIR /code

# Copy the requirements file to the working directory
COPY ./requirements.txt /code/requirements.txt

# Create a virtual environment inside the Docker container
# and install the dependencies there
RUN python -m venv /code/venv

# Activate the virtual environment and install the required packages
RUN /bin/bash -c "source /code/venv/bin/activate && pip install --no-cache-dir --upgrade -r /code/requirements.txt"

# Copy the FastAPI app code to the working directory
COPY ./app /code/app

# Set environment variable to ensure the virtual environment is used
ENV PATH="/code/venv/bin:$PATH"

# Run the FastAPI application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8001", "--workers", "4"]

