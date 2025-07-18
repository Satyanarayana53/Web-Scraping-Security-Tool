import requests
from bs4 import BeautifulSoup
import re

def analyze_security(html):
    soup = BeautifulSoup(html, 'html.parser')
    issues = []

    # Inline scripts check
    inline_scripts = soup.find_all('script', src=False)
    if inline_scripts:
        issues.append(f"Found {len(inline_scripts)} inline script(s)")

    # Forms with missing or suspicious action
    forms = soup.find_all('form')
    for form in forms:
        action = form.get('action')
        if not action or action.strip() == "" or re.match(r"javascript:", action, re.I):
            issues.append("Form with missing or suspicious action attribute")

    # External resources loaded over HTTP
    for tag in soup.find_all(['script', 'link', 'img']):
        url = tag.get('src') or tag.get('href')
        if url and url.startswith('http://'):
            issues.append(f"External resource loaded over HTTP: {url}")

    return issues

def scrape_website(url):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        html = response.text
        issues = analyze_security(html)
        snippet = html[:1000]  # store first 1000 chars for reference

        return {
            "url": url,
            "issues": issues,
            "html_snippet": snippet
        }
    except Exception as e:
        return {
            "url": url,
            "error": str(e)
        }
