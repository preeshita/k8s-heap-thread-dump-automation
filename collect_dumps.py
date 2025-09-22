#!/usr/bin/env python3
"""
collect_dumps.py
Automates heap and thread dump collection from Kubernetes pods.
"""

import subprocess
import os
from datetime import datetime

# Configuration
NAMESPACE = "default"  # Change if needed
POD_LABEL = "app=my-java-app"  # Label selector for Java pods
OUTPUT_DIR = "dumps"  # Local directory to store dumps

# Ensure output directory exists
os.makedirs(OUTPUT_DIR, exist_ok=True)

def get_pods():
    """Get list of pods matching the label."""
    cmd = ["kubectl", "get", "pods", "-n", NAMESPACE, "-l", POD_LABEL, "-o", "jsonpath={.items[*].metadata.name}"]
    result = subprocess.run(cmd, capture_output=True, text=True)
    pods = result.stdout.strip().split()
    return pods

def collect_heap_thread_dump(pod_name):
    """Collect heap and thread dump from a Java pod."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    heap_file = f"{OUTPUT_DIR}/{pod_name}_heap_{timestamp}.hprof"
    thread_file = f"{OUTPUT_DIR}/{pod_name}_thread_{timestamp}.txt"

    print(f"Collecting dumps from pod: {pod_name}")

    # Heap dump
    heap_cmd = ["kubectl", "exec", pod_name, "-n", NAMESPACE, "--",
                "jmap", "-dump:format=b,file=/tmp/temp.hprof", "1"]
    subprocess.run(heap_cmd, check=True)
    # Copy heap dump locally
    subprocess.run(["kubectl", "cp", f"{NAMESPACE}/{pod_name}:/tmp/temp.hprof", heap_file], check=True)
    # Clean up
    subprocess.run(["kubectl", "exec", pod_name, "-n", NAMESPACE, "--", "rm", "/tmp/temp.hprof"])

    # Thread dump
    thread_cmd = ["kubectl", "exec", pod_name, "-n", NAMESPACE, "--", "jstack", "1"]
    with open(thread_file, "w") as f:
        subprocess.run(thread_cmd, stdout=f, check=True)

    print(f"Dumps collected: {heap_file}, {thread_file}")

def main():
    pods = get_pods()
    if not pods:
        print("No pods found matching the label.")
        return
    for pod in pods:
        collect_heap_thread_dump(pod)

if __name__ == "__main__":
    main()
