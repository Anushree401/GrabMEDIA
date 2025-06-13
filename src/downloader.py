''' 
Responsible for downloading a single file from a URL

Handles:
 
    Getting filename from URL

    Downloading with progress bar

    Pause/resume support using Range headers

    File writing (append/binary)

Methods:

    __init__(url, filename=None)

    get_filename()

    download()
'''

import urllib.request as ulib
import urllib.parse as urlparse
import tqdm
import os 
from colorama import init, Fore
from utils import format_size
import yt_dlp
import random
import mimetypes
import threading
import sys
import time 

init(autoreset=True)

class Downloader:
    def __init__(self, url, file=None, allowed_types=None):
        self.url = url
        self.file = file if file else self.get_filename()
        self.chunk_size = 1024 * 1024 # 1 MB max chunk size
        self.paused = False
        self.allowed_types = allowed_types

    def get_filename(self):
        parsed_url = urlparse.urlparse(self.url)
        file = os.path.basename(parsed_url.path) if parsed_url.path else 'downloaded_file' 
        return file

    @staticmethod 
    def headers_for_url(url):
        # List of common browser User-Agents
        user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_6_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:125.0) Gecko/20100101 Firefox/125.0",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 13.6; rv:125.0) Gecko/20100101 Firefox/125.0",
        ]

        headers = {
            "User-Agent": random.choice(user_agents),
            "Accept": "image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.9",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive",
            "Sec-Fetch-Dest": "image",
            "Sec-Fetch-Mode": "no-cors",
            "Sec-Fetch-Site": "same-origin",   # You can adjust this for cross-origin if needed
            "Referer": url,  # You can also put the "main page" URL here if known
        }

        return headers
    
    def listen_for_pause(self):
        while True:
            cmd = input().strip().lower()
            if cmd == "p":
                self.paused = True
                print(f"{Fore.CYAN}[PAUSED] Download paused. Press 'r' to resume.")
            elif cmd == "r":
                self.paused = False
                print(f"{Fore.GREEN}[RESUMED] Continuing download...")
            elif cmd == "q":
                print(f"{Fore.RED}[-] Quitting download.")
                sys.exit()

    def download(self):
        response = ulib.urlopen(self.url) 
        self.total_size = int(response.headers.get('Content-Length', 0))
        print(f"{Fore.YELLOW}[+] Total size of file to download: {format_size(self.total_size)}") 
        try:
            print(f"{Fore.YELLOW}[+] Content-Type of URL is : {response.headers['Content-Type']}") 
            content_type = response.headers['Content-Type'].lower()
            file_ext = os.path.splitext(self.file)[1].lower()
            if not file_ext:
                ext = mimetypes.guess_extension(content_type.split(';')[0].strip())
                if ext is None:
                    ext = '.bin'  # fallback extension
                self.file += ext
                print(f"{Fore.GREEN}[+] No extension found in filename, adding extension: {ext}")
            if response.getcode()==200:
                if True: 
                    print(f"{Fore.GREEN}[+] Content-Type is {content_type}, downloading...") 
                    existing_file_size = 0
                    if os.path.exists(self.file):
                        existing_file_size = os.path.getsize(self.file)
                        print(f"{Fore.YELLOW}[+] Resuming download, existing file size: {existing_file_size} bytes")
                    parsed_url = urlparse.urlparse(self.url)
                    referer = f"{parsed_url.scheme}://{parsed_url.netloc}/"
                    header = Downloader.headers_for_url(self.url)  
                    if existing_file_size>0:
                        header["Range"] = f"bytes={existing_file_size}-"
                    req = ulib.Request(self.url, headers=header)
                    response = ulib.urlopen(req)
                    remaining_size = int(response.headers.get('Content-Length', 0)) - existing_file_size
                    mode = "ab" if existing_file_size>0 else "wb"
                    threading.Thread(target=self.listen_for_pause, daemon=True).start()
                    with open(self.file, mode) as f:
                        with tqdm.tqdm(
                            desc=self.file,
                            total=int(response.headers.get('Content-Length', 0)),
                            unit='iB',
                            unit_scale=True,
                            unit_divisor=1024,
                        ) as bar:
                            for chunk in iter(lambda: response.read(self.chunk_size), b''):
                                while self.paused:
                                    time.sleep(0.5)
                                f.write(chunk)
                                bar.update(len(chunk))
                    print(f"{Fore.GREEN}[+] Downloaded video successfully as {self.file}")
                    content_type = response.headers.get('Content-Type', '').lower()
                    file_ext = os.path.splitext(self.file)[1].lower()

                    video_extensions = {'.mp4', '.mov', '.avi', '.mkv', '.webm'}
                    image_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.bmp'}

                    is_video = (content_type.startswith('video/') or 
                                file_ext in video_extensions or
                                'octet-stream' in content_type)  # Some servers use this

                    is_image = (content_type.startswith('image/') or 
                                file_ext in image_extensions)
                    
                    is_audio = content_type.startswith('audio/')

                    is_pdf = content_type == 'application/pdf'

                    allowed = False

                    if not self.allowed_types:
                        allowed = True
                    else:
                        if "video" in self.allowed_types and is_video:
                            allowed = True
                        if "image" in self.allowed_types and is_image:
                            allowed = True
                        if "audio" in self.allowed_types and is_pdf:
                            allowed = True 
                    if not allowed:
                        print(f"{Fore.RED}[-] Skipping download: type '{content_type}' not allowed by filters.")
                        return
                    if not (is_video or is_image):
                        print(f"{Fore.YELLOW}[?] Unknown content type {content_type} - downloading anyway")
                else:
                    print(f"{Fore.RED}[-] Content-Type is not video or image, skipping download.") 
            else:
                print(f"{Fore.RED}[-] Failed to download file, HTTP status code: {response.getcode()}") 
        except Exception as e:
            print(f"{Fore.RED}[-] Error: {e}")

class YouTubeDownloader(Downloader):
    def __init__(self, url, output_dir='downloads', audio_only=False):
        super().__init__(url)
        self.output_dir = output_dir
        self.audio_only = audio_only
    def download(self):
        class ProgressLogger:
            def __init__(self):
                self.pbar = None
            def hook(self, d):
                if d['status'] == 'downloading':
                    total = d.get('total_bytes')
                    downloaded = d.get('downloaded_bytes')

                    if total is not None and downloaded is not None:
                        if self.pbar is None:
                            self.pbar = tqdm.tqdm(
                                desc="Downloading",
                                unit='B',
                                unit_scale=True,
                                unit_divisor=1024,
                                total=total
                            )
                        self.pbar.n = downloaded
                        self.pbar.refresh()
        progress = ProgressLogger()
        ydl_opts = {
            'outtmpl': os.path.join(self.output_dir, '%(title)s.%(ext)s'),
            'format': 'bestaudio+bestvideo/best',
            'merge_output_format': 'mp4',
            'progress_hooks': [progress.hook],
            'quiet': True,  # We handle output ourselves
            'continue': True,
            'nopart': False, # Enable partial downloads
            #'ffmpeg_location': r'E:\Psnal\hecking\projects\tools\video downloader\ffmpeg-7.1.1-essentials_build\ffmpeg-7.1.1-essentials_build\bin\ffmpeg.exe',
            'postprocessors': [{
                    'key': 'FFmpegVideoConvertor',
                    'preferedformat': 'mp4'
                }],
        }
        if self.audio_only:
            ydl_opts.update({
                'format': 'bestaudio/best',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec':'mp3',
                    'preferredquality':'192',  
                }],
            })
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([self.url])
                print(f"{Fore.GREEN}[+] Downloaded YouTube video successfully to {self.output_dir}")
                return 
        except Exception as e:
            print(f"{Fore.RED}[-] YouTube download failed: {e}")