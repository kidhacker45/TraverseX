![image alt](https://github.com/kidhacker45/stuffs/blob/dc25d922bc10fc4c2bae9b2c6a8dc38c9717cac3/VirtualBox_KALI%20LINUX_02_03_2025_14_02_43.png)
# Path Traversal Brute Force Tool

A Python-based tool for performing path traversal brute force attacks by replacing a placeholder in a target URL with words from a wordlist.

## 🔍 Overview

This tool is designed for security researchers and penetration testers to efficiently discover hidden or vulnerable paths in web applications by systematically testing numerous path variations. It works by replacing the "X45" placeholder in a provided URL with entries from a wordlist.

## ✨ Features

- **Placeholder Replacement**: Replaces "X45" in any part of a URL with wordlist entries
- **Concurrent Processing**: Multi-threaded testing for faster scanning
- **Customizable Status Codes**: Filter responses based on specific HTTP status codes
- **Progress Tracking**: Real-time progress bar shows scan status
- **Colorized Output**: Different colors for different HTTP status codes
- **Output Management**: Save successful matches to a file for further analysis
- **Flexible Configuration**: Adjust threads, timeout, and user-agent settings

## 🛠️ Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/path-traversal-tool.git
cd path-traversal-tool

# Install dependencies
pip install -r requirements.txt


### Dependencies

- requests
- colorama
- tqdm

## 📋 Usage

```bash
python path_traversal.py -u "http://example.com/X45/" -w wordlist.txt
```

### Command-line Arguments

| Argument | Description | Default |
|----------|-------------|---------|
| `-u, --url` | Target URL with X45 placeholder | Required |
| `-w, --wordlist` | Path to wordlist file | Required |
| `-c, --codes` | Comma-separated HTTP status codes to display | 200,301,302,307,401,403 |
| `-t, --threads` | Number of concurrent threads | 10 |
| `-o, --output` | Output file to save successful results | None |
| `-v, --verbose` | Show all requests, including failures | False |
| `--timeout` | Request timeout in seconds | 5.0 |
| `--user-agent` | User-Agent header to use | Mozilla/5.0... |

## 🚀 Use Cases

### 1. Finding Hidden Directories

```bash
python path_traversal.py -u "http://example.com/X45/" -w directory-list.txt
```

### 2. Testing Admin Panels

```bash
python path_traversal.py -u "http://example.com/X45/admin" -w prefixes.txt -c 200,403
```

### 3. Parameter Testing

```bash
python path_traversal.py -u "http://example.com/page.php?path=X45" -w traversal-payloads.txt
```

### 4. Discovering API Endpoints

```bash
python path_traversal.py -u "http://example.com/api/X45" -w api-endpoints.txt
```

### 5. Finding Backup Files

```bash
python path_traversal.py -u "http://example.com/X45.bak" -w common-files.txt
```

## 🔐 Security Considerations

This tool is intended for legitimate security testing with proper authorization. Unauthorized testing against systems you don't own or have permission to test is illegal and unethical. Always:

- Obtain proper authorization before testing
- Respect rate limits and avoid DoS conditions
- Follow responsible disclosure procedures for any findings

## 📝 Example Output

```
╔═══════════════════════════════════════════════════════════════╗
║ Path Traversal Brute Force Tool                               ║
║ Replaces X45 placeholder with words from a wordlist           ║
╚═══════════════════════════════════════════════════════════════╝

[*] Target URL: http://example.com/X45/
[*] Wordlist: common-dirs.txt
[*] Threads: 10
[*] Filter codes: 200, 301, 302, 307, 401, 403
[*] Total words: 4523
[*] Output file: results.txt
Testing: 100%|███████████████████████| 4523/4523 [00:32<00:00, 141.34word/s]
[200] http://example.com/admin/ (5621 bytes)
[403] http://example.com/config/ (1233 bytes)
[301] http://example.com/api/ (0 bytes)

[*] Brute force completed in 32.45 seconds
[*] Found 15 matching paths
[*] Results saved to: results.txt
```

## 🔄 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## ⚠️ Disclaimer

This tool is provided for educational and professional security testing purposes only. The authors are not responsible for any misuse or damage caused by this program.
