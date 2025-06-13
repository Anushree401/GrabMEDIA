'''
DownloadManager class 

    Manages multiple downloads (like playlist support)

    Uses threading for parallel downloads

    Maintains list of URLs to download

    Starts download threads and waits for them to finish
 
    Methods:

        __init__(urls)

        start_all()
'''
from downloader import Downloader, YouTubeDownloader 
import threading
import os
from colorama import init, Fore
from utils import is_youtube_url
from concurrent.futures import ThreadPoolExecutor, as_completed 
from utils import get_file_type_from_url 

init(autoreset=True)

class DownloadManager: 
    def __init__(self, urls, output_dir='downloads', threads=4, allowed_types=None, yt_audio_only=False):
        self.urls = urls
        self.output_dir = output_dir
        self.threads = threads
        self.allowed_types = allowed_types 
        self.yt_audio_only = yt_audio_only
        self.downloads = []
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
    def start_all(self):
        print(f"{Fore.GREEN}[+] Starting download manager with {len(self.urls)} URLs")
        with ThreadPoolExecutor(max_workers=self.threads) as executor:
            futures = []
            for url in self.urls:
                if is_youtube_url(url):
                    downloader = YouTubeDownloader(url, self.output_dir, audio_only=self.yt_audio_only)
                else:
                    file_type = get_file_type_from_url(url)
                    if self.allowed_types and file_type not in self.allowed_types:
                        print(f"{Fore.YELLOW}[!] Skipping {url} (type '{file_type}' not allowed)")
                        continue 
                    filename = Downloader(url).get_filename()
                    filepath = os.path.join(self.output_dir, filename)
                    downloader = Downloader(url, file=filepath)
                futures.append(executor.submit(downloader.download))
            for future in as_completed(futures):
                try:
                    future.result()  # This will raise any exceptions that occurred
                except Exception as e:
                    print(f"{Fore.RED}[-] Download failed: {e}")
