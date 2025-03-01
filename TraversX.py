#!/usr/bin/env python3
"""
TraverseX - Path Traversal Brute-Force Tool
A multithreaded CLI tool for penetration testers to test for path traversal vulnerabilities.
"""

import argparse
import concurrent.futures
import os
import re
import signal
import sys
import time
import subprocess
from urllib.parse import urlparse, urljoin

import requests
from colorama import Fore, Style, init
from tqdm import tqdm

# Initialize colorama
init(autoreset=True)

# Constants
PLACEHOLDER = "X45"
VERSION = "1.2.0"
GITHUB_URL = "https://github.com/kidhacker45/TraverseX"
GITHUB_RAW_URL = "https://raw.githubusercontent.com/kidhacker45/TraverseX/main/TraversX.py"
DEFAULT_TIMEOUT = 10
DEFAULT_THREADS = 10
DEFAULT_USER_AGENT = "TraverseX/1.0 Path Traversal Tool"

# Global variables
successful_hits = 0
total_requests = 0
start_time = None
last_valid_dir = None
error_count = 0
results = []


def print_banner():
    """Print the tool banner"""
    banner = f"""
{Fore.CYAN}████████╗██████╗  █████╗ ██╗   ██╗███████╗██████╗ ███████╗███████╗{Style.RESET_ALL}{Fore.RED}██╗  ██╗{Style.RESET_ALL}
{Fore.CYAN}╚══██╔══╝██╔══██╗██╔══██╗██║   ██║██╔════╝██╔══██╗██╔════╝██╔════╝{Style.RESET_ALL}{Fore.RED}╚██╗██╔╝{Style.RESET_ALL}
{Fore.CYAN}   ██║   ██████╔╝███████║██║   ██║█████╗  ██████╔╝███████╗█████╗  {Style.RESET_ALL}{Fore.RED} ╚███╔╝ {Style.RESET_ALL}
{Fore.CYAN}   ██║   ██╔══██╗██╔══██║╚██╗ ██╔╝██╔══╝  ██╔══██╗╚════██║██╔══╝  {Style.RESET_ALL}{Fore.RED} ██╔██╗ {Style.RESET_ALL}
{Fore.CYAN}   ██║   ██║  ██║██║  ██║ ╚████╔╝ ███████╗██║  ██║███████║███████╗{Style.RESET_ALL}{Fore.RED}██╔╝ ██╗{Style.RESET_ALL}
{Fore.CYAN}   ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═╝  ╚═══╝  ╚══════╝╚═╝  ╚═╝╚══════╝╚══════╝{Style.RESET_ALL}{Fore.RED}╚═╝  ╚═╝{Style.RESET_ALL}
{Fore.CYAN}╔═══════════════════════════════════════════════════════════════╗{Style.RESET_ALL}
{Fore.CYAN}║{Style.RESET_ALL} {Fore.GREEN}Path Traversal Brute Force Tool By KIDHACKER{Style.RESET_ALL}                             {Fore.CYAN}║{Style.RESET_ALL}
{Fore.CYAN}║{Style.RESET_ALL} Replaces X45 placeholder with words from a wordlist           {Fore.CYAN}║{Style.RESET_ALL}
{Fore.CYAN}╚═══════════════════════════════════════════════════════════════╝{Style.RESET_ALL}
"""
    print(banner)



def check_for_updates():
    """Check for updates from GitHub repository."""
    print(f"{Fore.CYAN}[*] Checking for updates...")
    
    try:
        response = requests.get(GITHUB_RAW_URL, timeout=10)
        
        if response.status_code != 200:
            print(f"{Fore.RED}[!] Failed to check for updates. Status code: {response.status_code}")
            return False
        
        remote_content = response.text
        
        # Extract version from remote content
        remote_version_match = re.search(r'VERSION\s*=\s*["\']([0-9.]+)["\']', remote_content)
        if remote_version_match:
            remote_version = remote_version_match.group(1)
            
            if remote_version != VERSION:
                print(f"{Fore.GREEN}[+] Update available: v{VERSION} → v{remote_version}")
                return True
            else:
                print(f"{Fore.GREEN}[+] Already running the latest version (v{VERSION})")
                return False
        else:
            print(f"{Fore.RED}[!] Couldn't determine remote version")
            return False
    
    except Exception as e:
        print(f"{Fore.RED}[!] Error checking for updates: {e}")
        return False


def update_script():
    """Update the script from GitHub repository."""
    print(f"{Fore.CYAN}[*] Updating TraverseX...")
    
    try:
        response = requests.get(GITHUB_RAW_URL, timeout=10)
        
        if response.status_code != 200:
            print(f"{Fore.RED}[!] Failed to download update. Status code: {response.status_code}")
            return False
        
        # Get current script path
        current_script = os.path.abspath(sys.argv[0])
        
        # Create backup
        backup_file = f"{current_script}.bak"
        try:
            with open(current_script, 'r') as original:
                with open(backup_file, 'w') as backup:
                    backup.write(original.read())
            print(f"{Fore.GREEN}[+] Created backup: {backup_file}")
        except Exception as e:
            print(f"{Fore.RED}[!] Failed to create backup: {e}")
            return False
        
        # Write new content
        try:
            with open(current_script, 'w') as script_file:
                script_file.write(response.text)
            print(f"{Fore.GREEN}[+] Updated successfully to the latest version")
            print(f"{Fore.YELLOW}[*] Please restart the script to use the new version")
            return True
        except Exception as e:
            print(f"{Fore.RED}[!] Failed to write update: {e}")
            
            # Restore from backup
            try:
                with open(backup_file, 'r') as backup:
                    with open(current_script, 'w') as original:
                        original.write(backup.read())
                print(f"{Fore.YELLOW}[*] Restored from backup")
            except Exception as restore_error:
                print(f"{Fore.RED}[!] Failed to restore from backup: {restore_error}")
                print(f"{Fore.RED}[!] Your backup is available at: {backup_file}")
            
            return False
    
    except Exception as e:
        print(f"{Fore.RED}[!] Error updating: {e}")
        return False


def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="TraverseX - Path Traversal Brute-Force Tool")
    parser.add_argument("-u", "--url", required=True, help=f"Target URL (use {PLACEHOLDER} as placeholder)")
    parser.add_argument("-w", "--wordlist", required=True, help="Path to wordlist file")
    parser.add_argument("-r", "--response-codes", default="200,403", 
                       help="Comma-separated HTTP response codes to filter (default: 200,403)")
    parser.add_argument("-o", "--output", help="Output file for results")
    parser.add_argument("-s", "--threads", type=int, default=DEFAULT_THREADS,
                       help=f"Number of threads (default: {DEFAULT_THREADS})")
    parser.add_argument("-v", "--verbose", action="store_true", 
                       help="Show detailed progress for each request")
    parser.add_argument("-t", "--timeout", type=int, default=DEFAULT_TIMEOUT,
                       help=f"Request timeout in seconds (default: {DEFAULT_TIMEOUT})")
    parser.add_argument("-up", "--update", action="store_true",
                       help="Check for updates and update the script")
    parser.add_argument("--user-agent", default=DEFAULT_USER_AGENT,
                       help="Custom User-Agent")
    parser.add_argument("--headers", help="Custom headers in format 'Header1:Value1;Header2:Value2'")
    
    args = parser.parse_args()
    
    # Handle update request first
    if args.update:
        if check_for_updates():
            if update_script():
                sys.exit(0)
    
    # Validate URL contains the placeholder
    if PLACEHOLDER not in args.url:
        parser.error(f"URL must contain the placeholder '{PLACEHOLDER}'")
    
    # Validate wordlist exists
    if not os.path.isfile(args.wordlist):
        parser.error(f"Wordlist file not found: {args.wordlist}")
    
    return args


def parse_custom_headers(headers_str):
    """Parse custom headers from string."""
    if not headers_str:
        return {}
    
    headers = {}
    try:
        for header_pair in headers_str.split(';'):
            if ':' in header_pair:
                name, value = header_pair.split(':', 1)
                headers[name.strip()] = value.strip()
    except Exception as e:
        print(f"{Fore.RED}[!] Error parsing custom headers: {e}")
        print(f"{Fore.RED}[!] Expected format: 'Header1:Value1;Header2:Value2'")
        sys.exit(1)
    
    return headers


def load_wordlist(wordlist_path):
    """Load words from the wordlist file."""
    try:
        with open(wordlist_path, 'r', errors='ignore') as f:
            return [line.strip() for line in f if line.strip()]
    except Exception as e:
        print(f"{Fore.RED}[!] Error loading wordlist: {e}")
        sys.exit(1)


def get_color_for_status(status_code):
    """Return the appropriate color for a status code."""
    if status_code >= 200 and status_code < 300:
        return Fore.GREEN
    elif status_code >= 300 and status_code < 400:
        return Fore.BLUE
    elif status_code == 403:
        return Fore.YELLOW
    elif status_code >= 400 and status_code < 500:
        return Fore.RED
    elif status_code >= 500:
        return Fore.MAGENTA
    else:
        return Fore.WHITE


def save_result(output_file, url, status_code, content_length):
    """Save successful result to the output file."""
    if not output_file:
        return
    
    try:
        with open(output_file, 'a') as f:
            f.write(f"[{status_code}] {url} (Size: {content_length})\n")
    except Exception as e:
        print(f"{Fore.RED}[!] Error writing to output file: {e}")


def make_request(word, url, filter_codes, headers, timeout, output_file, verbose):
    """Make a HTTP request and process the response."""
    global successful_hits, error_count, results
    
    target_url = url.replace(PLACEHOLDER, word)
    
    try:
        response = requests.get(target_url, headers=headers, timeout=timeout, allow_redirects=True)
        status_code = response.status_code
        content_length = len(response.content)
        
        result = {
            'url': target_url,
            'status_code': status_code,
            'content_length': content_length,
            'word': word
        }
        
        if str(status_code) in filter_codes or '*' in filter_codes:
            result['success'] = True
            successful_hits += 1
            
            if output_file:
                save_result(output_file, target_url, status_code, content_length)
            
            # If verbose mode is on, print the result immediately
            if verbose:
                color = get_color_for_status(status_code)
                print(f"{color}[+] Found: {target_url} (Status: {status_code}, Size: {content_length})")
                
            # Store successful results to display later if not in verbose mode
            results.append(result)
        elif verbose:
            print(f"{Fore.WHITE}[-] {target_url} (Status: {status_code}, Size: {content_length})")
        
        return result
    except requests.exceptions.Timeout:
        error_count += 1
        if verbose:
            print(f"{Fore.RED}[!] Timeout: {target_url}")
        return {'url': target_url, 'error': 'Timeout', 'word': word}
    except requests.exceptions.ConnectionError:
        error_count += 1
        if verbose:
            print(f"{Fore.RED}[!] Connection Error: {target_url}")
        return {'url': target_url, 'error': 'Connection Error', 'word': word}
    except Exception as e:
        error_count += 1
        if verbose:
            print(f"{Fore.RED}[!] Error: {target_url} - {str(e)}")
        return {'url': target_url, 'error': str(e), 'word': word}


def signal_handler(sig, frame):
    """Handle Ctrl+C gracefully."""
    print(f"\n{Fore.YELLOW}[!] Scan interrupted by user.")
    print_summary()
    display_results()
    sys.exit(0)


def print_summary():
    """Print a summary of the scan results."""
    global successful_hits, total_requests, start_time, error_count
    
    duration = time.time() - start_time
    print("\n" + "=" * 60)
    print(f"{Fore.CYAN}[*] Scan Summary:")
    print(f"{Fore.CYAN}[*] Total Requests: {total_requests}")
    print(f"{Fore.GREEN}[*] Successful Hits: {successful_hits}")
    print(f"{Fore.RED}[*] Errors: {error_count}")
    print(f"{Fore.YELLOW}[*] Duration: {duration:.2f} seconds")
    print(f"{Fore.YELLOW}[*] Average Speed: {total_requests / duration:.2f} requests/second")
    print("=" * 60)


def display_results():
    """Display all successful results at the end of the scan."""
    global results
    
    if results:
        print(f"\n{Fore.CYAN}[*] Successful Results:")
        for result in results:
            if 'success' in result and result['success']:
                color = get_color_for_status(result['status_code'])
                print(f"{color}[+] Found: {result['url']} (Status: {result['status_code']}, Size: {result['content_length']})")
    
    print(f"\n{Fore.GREEN}[*] Thanks for using TraverseX!")
    print(f"{Fore.GREEN}[*] GitHub: {GITHUB_URL}")


def main():
    """Main function to run the tool."""
    global successful_hits, total_requests, start_time, last_valid_dir, results
    
    print_banner()
    args = parse_arguments()
    
    # Setup signal handler for Ctrl+C
    signal.signal(signal.SIGINT, signal_handler)
    
    # Parse response codes to filter
    filter_codes = args.response_codes.split(',')
    
    # Load wordlist
    wordlist = load_wordlist(args.wordlist)
    total_words = len(wordlist)
    print(f"{Fore.CYAN}[*] Loaded {total_words} words from wordlist")
    
    # Setup headers
    headers = {
        'User-Agent': args.user_agent
    }
    
    if args.headers:
        custom_headers = parse_custom_headers(args.headers)
        headers.update(custom_headers)
    
    # Initialize output file if specified
    if args.output:
        try:
            with open(args.output, 'w') as f:
                f.write(f"# TraverseX Scan Results\n")
                f.write(f"# Target: {args.url}\n")
                f.write(f"# Date: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"# Filter Codes: {args.response_codes}\n\n")
        except Exception as e:
            print(f"{Fore.RED}[!] Error creating output file: {e}")
            sys.exit(1)
    
    # Display scan information
    print(f"{Fore.CYAN}[*] Target URL: {args.url}")
    print(f"{Fore.CYAN}[*] Filter codes: {args.response_codes}")
    print(f"{Fore.CYAN}[*] Threads: {args.threads}")
    print(f"{Fore.CYAN}[*] Timeout: {args.timeout} seconds")
    print(f"{Fore.CYAN}[*] Verbose mode: {'Enabled' if args.verbose else 'Disabled'}")
    print(f"{Fore.CYAN}[*] Starting scan...")
    
    # Initialize counter, timer and results list
    start_time = time.time()
    total_requests = 0
    results = []
    
    # Create thread pool executor
    with concurrent.futures.ThreadPoolExecutor(max_workers=args.threads) as executor:
        # Submit all tasks
        futures = {
            executor.submit(
                make_request, 
                word, 
                args.url, 
                filter_codes, 
                headers, 
                args.timeout, 
                args.output, 
                args.verbose
            ): word for word in wordlist
        }
        
        # Process results as they complete with progress bar
        with tqdm(total=total_words, desc="Scanning", unit="req", bar_format="{l_bar}{bar:30}{r_bar}") as pbar:
            for future in concurrent.futures.as_completed(futures):
                word = futures[future]
                try:
                    result = future.result()
                    total_requests += 1
                    pbar.update(1)
                except Exception as e:
                    if args.verbose:
                        print(f"{Fore.RED}[!] Error processing word '{word}': {e}")
    
    # Print summary and results
    print_summary()
    
    # If not in verbose mode, display all successful results at the end
    if not args.verbose:
        display_results()
    else:
        print(f"\n{Fore.GREEN}[*] Thanks for using TraverseX!")
        print(f"{Fore.GREEN}[*] GitHub: {GITHUB_URL}")


if __name__ == "__main__":
    main()

