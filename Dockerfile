FROM --platform=$TARGETPLATFORM python:3.9-slim
WORKDIR /usr/src/app
ARG GOOGLE_APPLICATION_CREDENTIALS_CONTENT
RUN echo "$GOOGLE_APPLICATION_CREDENTIALS_CONTENT" > credentials.json
ENV GOOGLE_APPLICATION_CREDENTIALS="credentials.json"
COPY requirements.txt ./
RUN pip3 install --no-cache-dir -r requirements.txt
COPY flask_app ./
EXPOSE 8080
ENTRYPOINT ["python", "app.py"]
