from colorama import Fore, Style, init  # For color-coded output

# Initialize colorama
init(autoreset=True)

# Define custom colors
NEON_YELLOW_GREEN = "\033[1;35m"  # Bold purple
RESET = "\033[0m"

def print_logo():
    print(
    f"{NEON_YELLOW_GREEN}" + r"""
 _____                                 __  __
|_   _| __ __ ___   _____ _ __ ___  ___\ \/ /
  | || '__/ _` \ \ / / _ \ '__/ __|/ _ \\  / 
  | || | | (_| |\ V /  __/ |  \__ \  __//  \ 
  |_||_|  \__,_| \_/ \___|_|  |___/\___/_/\_\ by KIDHACKER45
""" + RESET
)
