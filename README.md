<h1 align="center">JSecureScout</h1>
<h3 align="center">Automate crawling, dorking and enumeration of HTML comments and Javascript files through CLI with tool written in Python, developed by <a href="https://acs-group.info">ACSG</a> Team!</h3>
<h2>About</h2>
<b>JSecureScout</b> is a premium-quality tool designed for Penetration Testers, Bug Bounty Hunters or any CyberSecurity Enthusiasts to automate certain security checks on web applications with a visual report.<br>
Available functions are:
* Using Google Dorks to gather web pages that are using JavaScript files or JavaScript tags
* Gathering all the JavaScript files links
* Gathering all the code between JavaScript tags
* Gathering all HTML Comments<br>

Coming soon:
* Dorking sensitive links (making them primary) and extracting JavaScript and HTML Comments from them
* Gathering larger amount of JavaScript files
* Implementing more mechanisms of brute forcing and crawling
* Automatically analyzing gathered code

## Libraries
```
requests
bs4 (BeautifulSoup)
argparse
re
request.adaoters (HTTPAdapter)
urllib3.util.retry (Retry)
time
html
googlesearch
```
## Usage
### Help command
Using `python3 main.py -h` or `python3 main.py --help` will give you output which will in details explain usage.
### All usages
| Flag    | Type   | Default | Description                                 |
|---------|--------|---------|---------------------------------------------|
| -d      | string | /       | Domain to test (example.com)                |
| -n      | integer| /       | Number of links displayed from google dorks |
| -o      | file   | /       | Output file (Will be in HTML format)        |

## Example usages
`python3 main.py -d acs-group.info -n 5 -o report.html`<br>
This sets:
* Target domain: acs-group.info
* Number of dork links: 5
* Output file: report.html

### Tip
When tool generates report, you can use CTRL+F to search for certain patterns manually (Such as `api`,`key`,`password` and more).

## Feedback/Bugs
In case of encountering any problems, bugs or just having idea on what to implement in this project, feel free to contact developer (Luka Miletic) at [lm@acsg.me](mailto:lm@acsg.me)<br<

# Your security is our top priority.
[<img src="./ACSG.png" />](https://acs-group.info/)


