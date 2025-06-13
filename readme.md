# Video Downloader CLI Tool

A command-line tool for downloading videos from YouTube and other platforms, with support for parallel downloads and format conversion.

![Demo](demo.gif) *(Replace with actual screenshot/gif)*

## Features

- 🎥 **YouTube support** - Downloads videos and playlists
- ⚡ **Multi-threaded** - Parallel downloads with configurable threads
- 🔊 **Audio preservation** - Ensures audio tracks are properly merged
- 🛡️ **DRM handling** - Warns about protected content
- 📁 **Custom output** - Save to any directory

## Installation

### Prerequisites
- Python 3.8+
- FFmpeg (for format conversion)

```bash
# Clone repository
git clone https://github.com/yourusername/video-downloader.git
cd video-downloader

# Install dependencies
pip install -r requirements.txt

## Usage

python3 main.py [URL] [OPTIONS] 

### Download a single video:
python main.py "https://www.youtube.com/watch?v=dQw4w9WgXcQ" --output "~/Videos" 

### Download with 4 parallel threads:
python main.py "https://youtu.be/example1" "https://youtu.be/example2" -t 4

## Options
Flag	        Description	                             Default
-o,             --output	Output directory	        ./downloads
-t,             --threads	Parallel download threads	 2

## Known Issues

    ⚠️ DRM-protected videos: Some YouTube content may not be downloadable due to DRM restrictions

    📺 TV client formats: Certain formats may be skipped (see yt-dlp#12563)

    🌐 Web client formats: Some formats may be missing (see yt-dlp#12482)

## Troubleshooting

No audio in downloads?

    Verify FFmpeg is installed correctly

    Try different format combinations:
    python

    # In downloader.py
    'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best'

DRM warnings?
Try adding --ignore-errors to skip problematic videos.