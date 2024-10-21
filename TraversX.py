import requests
import os
import re
import validators  # Ensure this is installed: pip install validators
from logofile import print_logo  # Import your logo function

# Specify the path to the default wordlist file (included in the same directory)
DEFAULT_WORDLIST_FILE = "wordlist.txt"  # Ensure this file is included in your project
OUTPUT_FOLDER = "output"  # Default output folder

# Function to read the wordlist from the specified file
def load_wordlist(file_path):
    try:
        with open(file_path, 'r') as file:
            return [line.strip() for line in file]
    except Exception as e:
        print(f"[-] Error reading wordlist from {file_path}: {e}")
        return []

# Function to create a valid filename from the base URL
def url_to_filename(url):
    # Remove protocol (http, https) and non-alphanumeric characters
    filename = re.sub(r'http[s]?://', '', url)
    filename = re.sub(r'[^\w\-]', '_', filename)
    return filename

# Function to validate URL
def validate_url(url):
    if validators.url(url):
        return True
    return False

# Function to perform path traversal brute force
def brute_force_path_traversal(base_url, wordlist, response_codes):
    results = []  # List to store results
    for path in wordlist:
        # Replace 'X' in the URL with the traversal path
        url = base_url.replace('X', path)
        print(f"Trying: {url}")  # Show the URL being attempted

        try:
            response = requests.get(url, timeout=5)
            # Print the response code for debugging
            print(f"[DEBUG] Response Code: {response.status_code}, URL: {url}")  # Debug line
            
            # Add the URL and its response code to results
            results.append((url, response.status_code))
        
        except requests.exceptions.RequestException as e:
            print(f"[-] Request failed for URL: {url}, Error: {e}")  # Print error if request fails

    return results  # Return the list of results

# Main function to execute the brute force
def main():
    print_logo()  # Call the logo function to display the logo at the start

    # Validate the input URL from user
    while True:
        base_url = input("Enter the target URL (replace the file with 'X'): ").strip()
        if validate_url(base_url):
            break
        else:
            print("[-] Invalid URL. Please enter a valid URL (e.g., http://example.com/something?file=X).")

    # Input for custom wordlist
    custom_wordlist_path = input("Enter the path to a custom wordlist (press Enter to use the default): ").strip()

    # Load the wordlist: use custom if provided, otherwise use default
    if custom_wordlist_path and os.path.isfile(custom_wordlist_path):
        wordlist = load_wordlist(custom_wordlist_path)
        if not wordlist:
            print("[-] No valid paths in custom wordlist. Exiting.")
            return
    else:
        print("[*] Using default wordlist.")
        wordlist = load_wordlist(DEFAULT_WORDLIST_FILE)
        if not wordlist:
            print("[-] No valid paths in default wordlist. Exiting.")
            return

    # Input for response code filter
    response_code_input = input("Enter desired response codes to filter (comma-separated, e.g., 200,404): ").strip()
    response_codes = response_code_input.split(',') if response_code_input else []

    # Start brute forcing with the provided URL and wordlist
    results = brute_force_path_traversal(base_url, wordlist, response_codes)

    # Filter results based on desired response codes
    if response_codes:
        matches = [f"[INFO] URL: {url}, Response Code: {code}" for url, code in results if str(code) in response_codes]
    else:
        matches = [f"[INFO] URL: {url}, Response Code: {code}" for url, code in results]

    # Check if matches are found
    if matches:
        print("\nResults:")
        for match in matches:
            print(match)

        # Ask user if they want to save the output
        save_output = input("Do you want to save the output? (y/n): ").strip().lower()
        if save_output == 'y':
            include_response_code = input("Do you want to save the output with response codes? (y/n): ").strip().lower()

            # Ensure output folder exists
            if not os.path.exists(OUTPUT_FOLDER):
                os.makedirs(OUTPUT_FOLDER)

            output_file = os.path.join(OUTPUT_FOLDER, url_to_filename(base_url) + ".txt")  # Save file in output folder

            try:
                with open(output_file, 'w') as file:
                    for match in matches:
                        if include_response_code == 'y':
                            file.write(match + '\n')
                        else:
                            # Save without response code (just the URL)
                            url = match.split(",")[0].split(": ")[1]  # Extract the URL
                            file.write(url + '\n')
                print(f"[+] Output saved to {output_file}")
            except Exception as e:
                print(f"[-] Error saving output: {e}")
        else:
            print("Output not saved.")
    else:
        print("No matches found.")

if __name__ == "__main__":
    main()
 
