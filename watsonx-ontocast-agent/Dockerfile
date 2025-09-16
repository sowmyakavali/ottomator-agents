FROM ottomator/base-python:latest

# Build argument for port with default value
ARG PORT=8001
ENV PORT=${PORT}

WORKDIR /app

# Copy the application code
COPY . .

# Install additional dependencies for watsonx
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port from build argument
EXPOSE ${PORT}

# Command to run the application
CMD ["sh", "-c", "uvicorn watsonx_ontocast_agent:app --host 0.0.0.0 --port ${PORT}"]