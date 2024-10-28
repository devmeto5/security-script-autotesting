import time
import requests
import asyncio
from pyppeteer import launch

# Configuration
TARGET = 'https://yoursite.com'  # Target site URL
ZAP_API_KEY = '00000000000000000'  # ZAP API key
ZAP_PROXY = 'http://localhost:8080or8081'  # ZAP proxy server address
ZAP_API_URL = f'{ZAP_PROXY}/JSON'

# Function to send requests to ZAP API
def zap_request(endpoint, params=None):
    if params is None:
        params = {}
    params['apikey'] = ZAP_API_KEY  # Add API key to request parameters
    headers = {'Content-Type': 'application/json'}  # Set content type as JSON
    print(f"Sending request to ZAP API: {endpoint}, parameters: {params}")  # Debug output
    response = requests.get(f'{ZAP_API_URL}/{endpoint}', params=params, headers=headers)
    response.raise_for_status()  # Raise HTTPError if an error occurs
    print(f"Response from ZAP API: {response.text}")  # Debug output
    return response.json()

async def main():
    try:
        # Check if OWASP ZAP is available
        try:
            zap_status = zap_request('core/view/version')
            print("ZAP is available, version:", zap_status)
        except requests.exceptions.HTTPError as err:
            print(f"HTTP error: {err}")
            return
        except Exception as e:
            print(f"Error connecting to ZAP API: {e}")
            return

        # Launch browser using Puppeteer
        print("Launching browser...")  # Debug output
        browser = await launch(headless=False, executablePath=r'C:\Program Files\Google\Chrome\Application\chrome.exe')
        page = await browser.newPage()
        await page.goto(TARGET)
        print("Page opened:", TARGET)  # Debug output

        # Example interaction using Puppeteer
        try:
            # Change selector to match an element on your page
            search_box = await page.waitForSelector('input[type="text"]')  # Example text input field
            await search_box.type('Test')
            await page.keyboard.press('Enter')
            print("Search performed on the page.")  # Debug output
        except Exception as e:
            print(f"Error interacting with page elements: {e}")

        # Wait for some time for actions to complete
        await asyncio.sleep(5)

        # Start spidering before active scanning
        print(f"Starting spider for {TARGET}")
        spider_response = zap_request('spider/action/scan', {'url': TARGET})
        spider_scan_id = spider_response.get('scan')
        while int(zap_request('spider/view/status', {'scanId': spider_scan_id})['status']) < 100:
            print(f"Spidering {TARGET} is {zap_request('spider/view/status', {'scanId': spider_scan_id})['status']}% complete")
            await asyncio.sleep(5)

        # Start passive and active security scanning with ZAP
        print(f"Starting passive and active scanning for {TARGET}")
        zap_request('core/action/accessUrl', {'url': TARGET})
        await asyncio.sleep(2)

        # Passive scanning
        print("Waiting for passive scan to complete...")
        while int(zap_request('pscan/view/recordsToScan')['recordsToScan']) > 0:
            print("Records left to scan:", zap_request('pscan/view/recordsToScan')['recordsToScan'])
            await asyncio.sleep(5)

        # Active scanning
        print("Starting active scan...")
        scan_response = zap_request('ascan/action/scan', {'url': TARGET})
        scan_id = scan_response.get('scan')
        while int(zap_request('ascan/view/status', {'scanId': scan_id})['status']) < 100:
            status = zap_request('ascan/view/status', {'scanId': scan_id})['status']
            print(f"Active scan of {TARGET}: {status}% complete")
            await asyncio.sleep(5)

        print("Scanning complete")

        # Retrieve report of detected vulnerabilities
        alerts = zap_request('core/view/alerts', {'baseurl': TARGET})['alerts']
        for alert in alerts:
            print(f"Vulnerability: {alert['alert']} - Description: {alert['description']}")

        # Close browser
        await browser.close()
    except Exception as e:
        print(f"An error occurred: {e}")

# Run main asyncio process
asyncio.run(main())