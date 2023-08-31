# Use an official Python runtime as a parent image
FROM python:latest

# Set the working directory in the container to /app
WORKDIR /app

ADD ./examples/flyio_deployed_copilot/requirements.txt /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the current directory contents into the container at /app
ADD ./examples/flyio_deployed_copilot /app
ADD . /copilot
WORKDIR /copilot
RUN pip install .
WORKDIR /app

# Make port 8080 available to the world outside this container
EXPOSE 3000

# Run your application when the container launches
CMD ["python", "copilot.py"]