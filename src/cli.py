''' 
CLI class (optional but nice)

    Handles user input/output in CLI

    Parses command line args (optional: use argparse)

    Prints instructions, progress, errors, summaries

    Methods:

        get_urls_from_user()

        run()
'''

import argparse
from colorama import init, Fore
from manager import DownloadManager
from utils import is_youtube_url, format_size, validate_url 

init(autoreset=True)  # Initialize colorama for colored output

class CLI:
    def __init__(self):
        self.parser = argparse.ArgumentParser(description="Video Downloader CLI")
        self.parser.add_argument('urls', nargs='+', help='List of video URLs to download')
        self.parser.add_argument('--output', '-o', default='downloads', help='Output directory for downloaded files')
        self.parser.add_argument('--threads', '-t', type=int, default=4, help='Number of parallel download threads')
        self.parser.add_argument(
            '--types',
            nargs='+',
            choices=['audio', 'pdf', 'image', 'video'],
            help='Allowed file types to download (e.g., audio pdf)'
        )
        self.parser.add_argument(
            '--audio-only',
            action='store_true',
            help='Download only audio for YouTube videos'
        )
        self.allowed_types = self.args.types
        self.yt_audio_only = self.args.audio_only
        self.args = self.parser.parse_args() # Parse command line arguments
        self.urls = self.args.urls # List of URLs to download 
        self.output_dir = self.args.output # Output directory for downloaded files
        self.threads = self.args.threads # Number of parallel download threads, thread means number of parallel downloads
        self.validate_args() # Validate command line arguments
    def validate_args(self):
        if not self.urls:
            raise ValueError("At least one URL must be provided")
        if not isinstance(self.threads, int) or self.threads <= 0:
            raise ValueError("Number of threads must be a positive integer")
        if not isinstance(self.output_dir, str) or not self.output_dir.strip():
            raise ValueError("Output directory must be a non-empty string")     
    def get_urls_from_user(self):
        print(f"{Fore.YELLOW}Enter video URLs (one per line, empty line to finish):")
        urls = []
        while True:
            url = input()
            if not url.strip():
                break
            urls.append(url.strip())
        return urls    
    def validate_url(self, url):
        try:
            validate_url(url)
            if not is_youtube_url(url):
                raise ValueError(f"{Fore.RED}Invalid URL: {url} is not a YouTube URL")
            return True
        except ValueError as e:
            print(f"{Fore.RED}Error: {e}")
            return False
    def run(self):
        print(f"{Fore.GREEN}Starting video download with the following settings:")
        print(f"{Fore.YELLOW}Output Directory: {self.output_dir}")
        print(f"{Fore.YELLOW}Number of Threads: {self.threads}")
        print(f"{Fore.YELLOW}URLs to Download: {', '.join(self.urls)}")
        for url in self.urls:
            if is_youtube_url(url):
                print(f"{Fore.CYAN}  [YouTube] {url}")
            else:
                print(f"{Fore.CYAN}  [Direct] {url}")
        # Here you would typically call the download manager to start downloading
        # For example:
        manager = DownloadManager(
            self.urls,
            output_dir=self.output_dir,
            threads=self.threads,
            allowed = self.allowed_types,
            yt_audio_only = self.yt_audio_only 
        )
        manager.start_all()