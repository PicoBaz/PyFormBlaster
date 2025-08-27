import json
import requests
import random
import time
import csv
from datetime import datetime
from bs4 import BeautifulSoup

with open('config.json', 'r') as f:
    config = json.load(f)

form_url = config['formUrl']
form_fields = config['formFields']
payload_config = config['payloadConfig']
characters = config['characters']

results = []

def generate_random_input(length):
    all_chars = characters['lowercase'] + characters['uppercase'] + characters['numbers'] + characters['special']
    return ''.join(random.choice(all_chars) for _ in range(length))

def generate_malicious_payloads(field):
    payloads = [
        "<script>alert('xss')</script>",
        "' OR '1'='1",
        "1; DROP TABLE users;",
        "<img src=x onerror=alert(1)>",
        "admin' --",
        "{{7*7}}",
        "%00",
        ""><script>alert(1)</script>",
        "' UNION SELECT NULL, NULL, NULL --"
    ]
    return payloads if field in payload_config.get('maliciousFields', []) else []

def get_form_fields():
    try:
        response = requests.get(form_url)
        soup = BeautifulSoup(response.text, 'html.parser')
        form = soup.find('form')
        fields = {}
        for input_tag in form.find_all('input'):
            name = input_tag.get('name')
            if name:
                fields[name] = input_tag.get('value', '')
        return fields
    except:
        return {}

def try_form_submission(fields, retry_count=0):
    try:
        payload = {k: v for k, v in fields.items()}
        response = requests.post(form_url, data=payload, headers={'Content-Type': 'application/x-www-form-urlencoded'}, allow_redirects=False)
        
        content_length = len(response.text)
        is_error = response.status_code >= 400 or 'error' in response.text.lower()
        
        results.append({
            'fields': json.dumps(fields),
            'status': 'error' if is_error else 'success',
            'responseCode': response.status_code,
            'contentLength': content_length,
            'timestamp': datetime.utcnow().isoformat()
        })

        return {'success': not is_error, 'response': response}
    except Exception as e:
        if retry_count < payload_config['maxRetries']:
            time.sleep(2)
            return try_form_submission(fields, retry_count + 1)
        results.append({
            'fields': json.dumps(fields),
            'status': 'error',
            'responseCode': getattr(e.response, 'status_code', 'N/A'),
            'contentLength': 0,
            'timestamp': datetime.utcnow().isoformat(),
            'error': str(e)
        })
        return {'success': False, 'response': None}

def delay(ms):
    time.sleep(ms / 1000)

def save_results():
    with open('form_fuzzer_results.csv', 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['fields', 'status', 'responseCode', 'contentLength', 'timestamp', 'error'])
        writer.writeheader()
        writer.writerows(results)

def form_fuzzer():
    form_fields_template = get_form_fields() if payload_config['autoDetectFields'] else form_fields
    if not form_fields_template:
        return

    for _ in range(payload_config['maxAttempts']):
        fields = form_fields_template.copy()
        for field in fields:
            if field in payload_config.get('fuzzFields', []):
                if random.random() < payload_config['maliciousPayloadChance']:
                    payloads = generate_malicious_payloads(field)
                    fields[field] = random.choice(payloads) if payloads else generate_random_input(payload_config['randomInputLength'])
                else:
                    fields[field] = generate_random_input(payload_config['randomInputLength'])
        
        try_form_submission(fields)
        delay(payload_config['delayMs'])

    save_results()

try:
    form_fuzzer()
except Exception as e:
    save_results()