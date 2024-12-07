FROM --platform=$TARGETPLATFORM python:3.9-slim
WORKDIR /usr/src/app
COPY requirements.txt ./
COPY credentials.json ./
ENV GOOGLE_APPLICATION_CREDENTIALS="credentials.json"
RUN pip3 install --no-cache-dir -r requirements.txt
COPY flask_app ./
EXPOSE 8080
ENTRYPOINT ["python", "app.py"]