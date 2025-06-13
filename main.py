''' 
Basic video downloader script using yt-dlp and threading
This script allows users to download videos from provided URLs
yt-dlp is a powerful command-line tool for downloading videos from YouTube and other sites
yt-dlp is used to handle the actual downloading of videos 
threading is used to allow multiple downloads to happen in parallel
this script is a basic implementation and can be extended with more features like error handling, progress bars (implemented), etc.
this script also includes a CLI interface for user interaction (using tqdm for progress bars)
it also uses urlib for handling URLs and file downloads
'''

import yt_dlp
import threading 
from src.cli import CLI 
from src.manager import DownloadManager
from colorama import init, Fore
from src.utils import is_youtube_url 
import sys

init(autoreset=True)  # Initialize colorama for colored output

def main():
    print(f"{Fore.GREEN}=====Welcome to the File Downloader!=====")
    try:
        cli = CLI()  # Initialize the CLI interface
        cli.run()  # Run the CLI to get user input and start downloads
        print(f"{Fore.GREEN}=====File Downloader finished successfully!=====")
    except Exception as e:
        print(f"{Fore.RED}[-] Error: {e}")
        print(f"{Fore.YELLOW}[-] Please check your input and try again.")
    except Exception as e:
        print(f"{Fore.RED}[-] Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()  # Run the main function to start the downloader