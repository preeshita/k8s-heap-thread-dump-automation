# k8s-heap-thread-dump-automation
Python script to automate heap and thread dump collection from Kubernetes pods for monitoring and debugging purposes, with optional cloud storage upload.


## Overview
This project automates the collection of heap and thread dumps from Java applications running in Kubernetes pods. It is useful for monitoring, debugging, and performance analysis of Java-based microservices.

## Features
- Collects **heap dumps (.hprof)** from Java pods.
- Collects **thread dumps (.txt)** from Java pods.
- Supports multiple pods using **label selectors**.
- Stores dumps in a local directory (`dumps`).
- Easy to extend for cloud storage upload (GCP/AWS S3).

## Prerequisites
- Python 3.8+
- `kubectl` installed and configured to access your cluster
- Java application running in Kubernetes pods with access to `jmap` and `jstack` tools

## Configuration
Edit the top of `collect_dumps.py`:

```python
NAMESPACE = "default"           # Kubernetes namespace
POD_LABEL = "app=my-java-app"   # Label selector for your pods
OUTPUT_DIR = "dumps"            # Local folder to store dumps

# Usage

## Clone the repo:

git clone https://github.com/<your-username>/k8s-heap-thread-dump-automation.git
cd k8s-heap-thread-dump-automation

##Run the script:

python3 collect_dumps.py

##Check the dumps/ folder for collected heap and thread dumps.
