# Nebula Assignment 
Fork or Take a pull of this repo .




## Assignment Tasks (Python & Go)

Python Assignments:

1. Write a Python script using Boto3 to list all EC2 instances in a region and highlight those with unencrypted EBS volumes.


# EC2 Reader

A Python script that lists all EC2 instances in a region and highlights any **unencrypted EBS volumes**.

---

## Requirements
- Python 3.7+  
- Boto3 (`pip install boto3`)  
- AWS credentials (via `aws configure`, env vars, or IAM role)  

---

## Usage
Clone the repo and run:


```bash
python ec2_encryption_checker.py

```
![Description of image](images/screenshot.png)


