# TraverseX
# Path Traversal Brute Force Tool

## Overview
This Python-based tool is designed to perform path traversal brute force attacks against web applications. It allows users to specify a target URL and a wordlist to replace a placeholder in the URL, attempting various path values to find vulnerable endpoints.

## Features
- Customizable wordlist: Use a default wordlist or specify your own.
- Response code filtering: Focus on specific HTTP response codes during brute forcing.
- Output management: Save results to a file with options for including or excluding response codes.
- URL validation: Ensures that the provided target URL is valid before execution.

## Prerequisites
- Python 3.x
- Required libraries: `requests`, `validators`

You can install the required libraries using pip:

```bash
pip install requests validators

Limitations
This tool is designed for educational purposes and should only be used with permission from the owner of the target web application.
It assumes that the web application is vulnerable to path traversal attacks.
Disclaimer
This tool is for educational purposes only. Misuse of this tool may lead to legal consequences. The authors are not responsible for any damage or illegal activities performed with this tool. Use it ethically and responsibly.
