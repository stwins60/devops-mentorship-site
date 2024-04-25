FROM python:3.11

ARG SENDGRID_API_KEY
ENV SENDGRID_API_KEY=$SENDGRID_API_KEY

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt --no-cache-dir

COPY . .

EXPOSE 5000

CMD ["python", "server.py"]
