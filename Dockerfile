FROM python:3.10
WORKDIR /app
COPY requirements.txt .
EXPOSE 5000

RUN pip install --upgrade pip && pip install -r requirements.txt
COPY . .
# Define environment variable
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0

# Run app.py when the container launches
CMD ["flask", "run"]