# TraverseX 
Refers to traversing directories with the "X" placeholder in the URL.
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

pip install requests validators

**Limitations**
This tool is designed for educational purposes and should only be used with permission from the owner of the target web application.
It assumes that the web application is vulnerable to path traversal attacks.
Disclaimer
This tool is for educational purposes only. Misuse of this tool may lead to legal consequences. The authors are not responsible for any damage or illegal activities performed with this tool. Use it ethically and responsibly.


## Getting Started
**1. Clone the Repository**  
> git clone https://github.com/kidhacker45/TraverseX  
> cd TraverseX
>
**2. Prepare the Wordlist**  
> Ensure you have a wordlist file named wordlist.txt in the same directory as the script or provide a custom path when prompted.
> 
**3. Run the Tool:**    
> python3 traversex.py

## Usage
When prompted, enter the target URL where you want to perform the brute force attack. Replace the part of the URL you want to test with X (e.g., http://example.com/something?file=X).  

Optionally, specify the path to a custom wordlist. Press Enter to use the default wordlist.txt.  

Enter desired HTTP response codes to filter results (e.g., 200,404). Press Enter to skip filtering.  

After brute forcing, choose whether to save the output. If you opt to save, you can choose to include or exclude the response codes in the saved file  

## Example
1.    $ python3 traversx.py  
2.      Enter the target URL (replace the file with 'X'): http://example.com/something?file=X  
3.      Enter the path to a custom wordlist (press Enter to use the default):   
4.      Enter desired response codes to filter (comma-separated, e.g., 200,404): 200  
5.      Do you want to save the output? (y/n): y  
6.      Do you want to save the output with response codes? (y/n): y  

## Disclaimer
This tool is intended for educational purposes and authorized security testing only. Use it responsibly and ensure you have permission to test the target application

## License
This project is licensed under the MIT License - see the LICENSE file for details.
