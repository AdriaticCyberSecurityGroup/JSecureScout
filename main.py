# Libraries
import requests
from bs4 import BeautifulSoup
import argparse
import re
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import time
import html
import googlesearch

# Google search function
def google_search(query, num_results):
    session = requests.Session()
    retry = Retry(connect=3, backoff_factor=0.5)
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    
    url = "https://www.google.com/search"
    params = {
        "q": query,
        "num": num_results
    }
    
    try:
        response = session.get(url, params=params)
        response.raise_for_status()  # Raise an exception for HTTP errors
        return response.content
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 429:
            print(f"Too many requests, retrying after {e.response.headers.get('Retry-After', 60)} seconds")
            time.sleep(int(e.response.headers.get('Retry-After', 60)))
            return google_search(query, num_results)
        else:
            print(f"Error searching Google: {e}")
            return None
    except Exception as e:
        print(f"Error searching Google: {e}")
        return None

def extract_js_files_and_comments(url):
        session = requests.Session()
        retry = Retry(connect=3, backoff_factor=0.5)
        adapter = HTTPAdapter(max_retries=retry)
        session.mount('http://', adapter)
        session.mount('https://', adapter)
        
        try:
            response = session.get(url)
            response.raise_for_status()  # Raise an exception for HTTP errors
            soup = BeautifulSoup(response.content, 'html.parser')
    
            # Extracting JavaScript files
            js_files = soup.find_all('script', src=True)
            js_files = [js_file['src'] for js_file in js_files]
    
            # Extracting JavaScript code from <script> tags
            js_code = []
            for script in soup.find_all('script'):
                if script.text.strip():
                    js_code.append(script.text.strip())
    
            # Extracting HTML comments
            html_comments = []
            for element in soup.find_all(string=lambda t: isinstance(t, str) and re.match(r'<!--.*?-->', t)):
                html_comments.append(element.strip())
    
            return js_files, js_code, html_comments
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 429:
                print(f"Too many requests, retrying after {e.response.headers.get('Retry-After', 60)} seconds")
                time.sleep(int(e.response.headers.get('Retry-After', 60)))
                return extract_js_files_and_comments(url)
            else:
                print(f"Error extracting data from {url}: {e}")
                return [], [], []
        except Exception as e:
            print(f"Error extracting data from {url}: {e}")
            return [], [], []

# Report generation
def generate_html_report(results, output_file):
    html_report = """
    <html>
    <head>
        <title>Report</title>
        <style>
            body {
                font-family: Arial, sans-serif;
            }
            h2 {
                margin-top: 0;
            }
            .result {
                margin-bottom: 20px;
                padding: 10px;
                border: 1px solid #ccc;
                border-radius: 5px;
                box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
            }
            .result h2 {
                margin-bottom: 10px;
            }
            .result ul {
                list-style: none;
                padding: 0;
                margin: 0;
            }
            .result li {
                margin-bottom: 10px;
            }
        </style>
    </head>
    <body>
    <a href="https://acs-group.info/"><img src="ACSG.png" alt="For those who value security."></a>
    <h3>To look for certain patterns use CTRL+F</h3>
    <h1>Report</h1>
    """
    for result in results:
        url = result
        js_files, js_code, html_comments = extract_js_files_and_comments(url)
        html_report += """
        <div class="result">
            <h2>URL: {}</h2>
            <h3>JavaScript Files:</h3>
            <ul>
        """.format(url)
        for js_file in js_files:
            html_report += "<li>- {}</li>".format(html.escape(js_file))  # HTML-escape JavaScript file URLs
        html_report += """
            </ul>
            <h3>JavaScript Code:</h3>
            <pre>
        """
        for code in js_code:
            html_report += "{}\n".format(html.escape(code))  # HTML-escape JavaScript code
        html_report += """
            </pre>
            <h3>HTML Comments:</h3>
            <ul>
        """
        for comment in html_comments:
            html_report += "<li>- {}</li>".format(html.escape(comment))  # HTML-escape HTML comments
        html_report += """
            </ul>
        </div>
        """
    html_report += """
    </body>
    </html>
    """
    with open(output_file, "w") as f:
        f.write(html_report)

def main():
    # Arguments
    parser = argparse.ArgumentParser(description="Penetration testing tool developed by Adriatic CyberSecurity Group.")
    parser.add_argument("-d", "--domain", help="Domain to search", required=True)
    parser.add_argument("-n", "--num_results", help="Number of search results to retrieve", type=int, default=10)
    parser.add_argument("-o", "--output_file", help="Output file for results", default="results.html")
    
    args = parser.parse_args()
    
    query = f"site:{args.domain} filetype:js | inurl:js | intext:javascript"
    results = googlesearch.search(query)
    urls = []
    
    for i, result in enumerate(results):
        if i >= args.num_results:
            break
        urls.append(result)
    
    generate_html_report(urls, args.output_file)

if __name__ == "__main__":
    main()
