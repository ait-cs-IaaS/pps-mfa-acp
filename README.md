# Physical Protection System (PPS) Multi-Factor Authentication (MFA) Access Control Panel (ACP)

## Description and Purpose

This is a Flask server designed to forward MFA inputs to the Central Access Control System (CACS)

The server has receives the following JSON data (shown as python code):
```python
data = {
        "employee_id":<integer>,
        "pin":<integer>,
        "image":<base64_encoded_image>
    }
```
The request is then forwarded to the CACS. 

## Installation Instructions 

**Python Version:** `3.8.10`

**APT Extras:** `None`

**PIP Packages:**
```bash
pip install requirements.txt
```

## Directory Structure

`log` - folder containing log files

## Starting the Server

```bash
python3 acp.py
```
