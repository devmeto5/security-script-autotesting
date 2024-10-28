# Security Test Script

This project is a Python script that performs security testing on a target website using OWASP ZAP and Puppeteer. The script automatically runs both passive and active scans to identify vulnerabilities.

## Features
- Launches a browser using Puppeteer for interaction.
- Uses OWASP ZAP to perform passive and active vulnerability scans.
- Retrieves and displays a list of discovered vulnerabilities.

## Prerequisites
- Python 3.x: [Download here](https://www.python.org/downloads/)
- Node.js and npm: [Download here](https://nodejs.org/)
- Google Chrome
- OWASP ZAP: [Download here](https://www.zaproxy.org/download/)

## Installation
1. Install Python, Node.js, npm, Google Chrome, and OWASP ZAP.
2. Install required Python packages:
   ```bash
   pip install requests pyppeteer
