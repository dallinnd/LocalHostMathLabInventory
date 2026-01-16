# Use a lightweight Python image
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Install Flask
RUN pip install flask

# Copy all your files into the container
COPY . .

# Expose the port
EXPOSE 8000

# Run the server unbuffered (so you see logs instantly)
CMD ["python", "-u", "server.py"]
