# PyFormBlaster

A powerful, modular web form fuzzing tool built for ethical security audits in Python. PyFormBlaster enables developers and security enthusiasts to test web forms with random and malicious inputs, uncovering potential vulnerabilities like XSS, SQL Injection, or unexpected behaviors.

⚠️ **Ethical Use Only**: This tool is for testing your own systems or with explicit permission. Misuse can lead to legal consequences. Always prioritize security best practices.

## Features
- **Modular Config**: All settings (URL, form fields, fuzzing rules) in a single `config.json` file for quick tweaks.
- **Auto Form Detection**: Automatically extracts form fields using BeautifulSoup.
- **Smart Input Generation**: Combines random strings with malicious payloads for comprehensive testing.
- **Error Resilience**: Automatic retries on transient errors, with configurable delays to avoid locks.
- **CSV Reporting**: Detailed logs of attempts, including response codes and content length.
- **Python Powered**: Lightweight, runs anywhere with Python 3.6+.

## Installation
1. Clone the repo:
   ```
   git clone https://github.com/PicoBaz/PyFormBlaster.git
   cd PyFormBlaster
   ```
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Edit `config.json` to match your setup (e.g., form URL, fields).

## Usage
Run the script:
```
python form_fuzzer.py
```
- Output: Progress in console, results in `form_fuzzer_results.csv`.
- Example config tweak: Increase `maxAttempts` for deeper tests, but monitor for rate limits.

## Configuration
Edit `config.json`:
- `formUrl`: Target form submission endpoint.
- `formFields`: Default form fields (used if `autoDetectFields` is false).
- `payloadConfig`: Tune attempts, delays, retries, input length, and malicious payload usage.
- `characters`: Char sets for random inputs.

## Extending PyFormBlaster
- Add custom malicious payloads in `form_fuzzer.py`.
- Integrate with external payload lists (e.g., OWASP lists in TXT files).
- For advanced setups, fork and add parallel processing via `concurrent.futures`.

## Disclaimer
PyFormBlaster is an educational tool. Use responsibly—test only what you own. The author assumes no liability for misuse.



Star the repo if it helps your audits! 🌟 Contributions welcome.
