# PhotoCloud
cs1660 photo cloud

## Project Title: Image Processing Service
Group Members:
- Seongmin Oh 
- Maliki Mwangi
- Rachel Jan
- Lukas Finn
- Stephen Gwon

## Overview:
This is the final project for CS1660. The objective is to leverage Google Cloud Platform (GCP) services to build a cloud-based application that incorporates at least three different cloud services (i.e. Cloud Storage, Compute Engine, Cloud Run, BigQuery, etc). These services do not need to be limited to the ones covered in the course, and the project can be developed using any programming language or framework.

## Project Description:
Our project will be an image processing service, where a user will access a web application that allows users to upload images. We will provide multiple processing options for images, such as color filters, and will give users the opportunity to download the changed photo. This project will involve front-end and back-end web development and the utilization of GCP services such as cloud storage, cloud functions, and app engine.

## Rubric:
The project will be graded based on the following criteria:
- Usage of at least 3 GCP Services: (30 pts) The project should incorporate at least three different GCP services.
- Deployment Automation: (5 pts) The deployment process should be automated (that is, it should not require manual intervention). Presentation: (5 pts) The team will demo the project to the class, explaining the problem it aims to solve, the architecture, and the technologies used.

## Project Structure:
1. UI/Frontend: responsive web app where users can upload an image from their device and choose a processing option, then have the processed image be displayed and ready for download
- Made in HTML, CSS, and JavaScript
2. Backend Services: Cloud functions that handle upload processing(saving to cloud storage), image processing task(applying selected processing options)
- Cloud Storage (to store uploaded/processed images) - Cloud Run/App Engine: to host the web application
3. Image Processing Logic: backend logic to manipulate the image and store it back to Cloud Storage
