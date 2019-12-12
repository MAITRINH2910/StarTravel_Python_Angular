# Use an official Python runtime as a parent image
FROM ubuntu
FROM python:3.6-slim

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app


# Install any needed packages specified in requirements.txt
COPY requirements.txt /app
RUN pip install --trusted-host pypi.python.org -r requirements.txt

# Make port 80 available to the world outside this container
EXPOSE 9999

# Define environment variable
ENV NAME World

# Run run.py when the container launches
CMD ["python", "-u", "run.py"]

