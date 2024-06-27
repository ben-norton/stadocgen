# set base image (host OS)
FROM python:3.12-alpine

# set the working directory in the container
WORKDIR /code

# Create new user with UID
RUN adduser --disabled-password --gecos '' --system --uid 1001 python && chown -R python /code

# copy the dependencies file to the working directory
COPY requirements.txt .

# install dependencies
RUN pip install -r requirements.txt

# copy the content of the local src directory to the working directory
COPY main.py .
COPY app app

# Set user to newly created user
USER 1001

#Expose port 8080 for Flask app
EXPOSE 8080

# command to run on container start
CMD ["waitress-serve", "--port=8080", "app.routes:app"]