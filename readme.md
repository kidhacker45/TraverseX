# TraverseX

A Linux command-line tool for path traversal brute force testing with multi-threading support.

## Features

- **Fast Scanning**: Multi-threaded path testing with adjustable speed
- **Targeted Filtering**: Filter results by HTTP response codes
- **Customizable**: Set custom User-Agent and HTTP headers
- **Organized Output**: Save results to structured output files
- **Visual Feedback**: Progress bar and colorized terminal output

## Installation

### Requirements

- Python 3.7 or higher
- Required Python libraries:
  - requests
  - colorama
  - tqdm
  - argparse (included in Python standard library)
  - concurrent.futures (included in Python standard library)

### Setup

1. Clone the repository:
   ```
   git clone https://github.com/username/traversex.git
   cd traversex
   ```

2. Install required packages:
   ```
   pip install -r requirements.txt
   ```

3. Make the script executable:
   ```
   chmod +x traversex.py
   ```

## Usage

### Basic Usage

```
python3 traversex.py -u <URL> -w <wordlist>
```

### All Options

```
python3 traversex.py -u <URL> -r <response_code> -w <wordlist> -o <output_file> -s <speed>
```

### Arguments

- `-u, --url`: Target URL (Required)
- `-w, --wordlist`: Path to wordlist file (Required)
- `-r, --response-code`: Filter by response code(s) (e.g., 200,403) (Optional)
- `-o, --output`: Output file to save results (Optional, default: output.txt)
- `-s, --speed`: Number of parallel threads (Optional, default: 10)
- -v, --verbose: Show detailed progress for each request
  -t, --timeout: TIMEOUT Request timeout in seconds (default: 10)
- `--user-agent`: Custom User-Agent string (Optional)
- `--headers`: Custom headers in format 'Header1:value1;Header2:value2' (Optional)
- `-h, --help`: Show help menu

### Examples

Basic scan:
```
python3 traversex.py -u http://example.com -w wordlists/common.txt
```

Scan with response code filtering and increased thread count:
```
python3 traversex.py -u http://example.com -w wordlists/paths.txt -r 200,403 -s 20
```

Scan with custom headers:
```
python3 traversex.py -u http://example.com -w wordlists/paths.txt --user-agent "Mozilla/5.0" --headers "X-Forwarded-For:127.0.0.1;Cookie:session=test"
```

## Output

Results will be displayed in the terminal with the following format:
```
[STATUS_CODE] /path (content_length bytes)
```

If an output file is specified with `-o`, results will be saved in the `output/` directory.

## Creating Wordlists

You can create your own wordlists or use common ones available in security tools like SecLists.

Example wordlist format (one path per line):
```
/admin
/login
/backup
/config
/.git
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Disclaimer

This tool is intended for legal security testing with proper authorization only. Unauthorized scanning of systems is illegal and unethical.
