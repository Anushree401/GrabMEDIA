# GrabMEDIA

A powerful command-line tool for downloading videos, audio, PDFs, and images from YouTube and direct URLs. Built with `yt-dlp`, `urllib`, and Python threading, it supports multi-threaded downloads, file-type filtering, and YouTube audio-only mode.

---

## 🚀 Features

- 🎬 **YouTube support** – Download videos or audio-only
- 🌐 **Direct URL support** – PDFs, images, MP3s, MP4s
- 🔁 **Pause/Resume** – Works with Range headers
- ⚙️ **Multi-threaded** – Parallel downloads with configurable threads
- 📁 **Custom output** – Choose your download directory
- 🎧 **Audio-only mode** – Extract audio from YouTube videos
- 🔍 **File-type filters** – Only download PDFs, images, audio, etc.
- 📊 **Progress bar** – Powered by `tqdm`

---

## 📦 Installation

### Prerequisites:
- Python 3.8+
- FFmpeg (for YouTube audio/video merging)

### Setup:
```bash
git clone https://github.com/yourusername/video-downloader.git
cd video-downloader
pip install -r requirements.txt
```

## 🧑‍💻 Usage
```bash
python main.py [URL1] [URL2] ... [OPTIONS]
```

### 🧪 Examples

#### ✅ Download a YouTube video:
```bash
python main.py "https://www.youtube.com/watch?v=dQw4w9WgXcQ" --output "E:/Downloads"
```

#### 🎵 Download YouTube audio-only:
```bash
python main.py "https://www.youtube.com/watch?v=dQw4w9WgXcQ" --audio-only --types audio
```

#### 🧵 Download 3 URLs with 3 threads:
```bash
python main.py "URL1" "URL2" "URL3" --threads 3
```

#### 🎯 Filter only audio + PDF:
```bash
python main.py "URL1" "URL2" --types audio pdf
```

#### 📍 Direct MP4:
```bash
python main.py "https://download.samplelib.com/mp4/sample-5s.mp4" --types video --output "E:/Downloads"
```

## 🛠️ Options
|Flag	        | Description                                    | Default            |
|-------------|------------------------------------------------|--------------------|
|-o,          | --output	Output directory	                  | ./downloads        |
|-t,          | --threads	Number of parallel download threads	| 2                  |
|--types      | Allowed file types: audio, pdf, image, video	| None (all allowed) |
|--audio-only | Only download audio (YouTube only)	            | False              |

## 📸 Sample Output

### 🎥 Video File (MP4)
![Video Demo](tests/video)

### 📸 Image File (JPEG)
![Image Demo](tests/image)

### 📄 PDF Document
![PDF Demo](tests/pdf)

### 🎧 Audio File (MP3)
![Audio Demo](tests/audio)

### 📹 YouTube Video (Audio-Only)
![YouTube Audio Demo](tests/yt_audio)

## 🧩 Supported File Types

    🎞️ .mp4, .webm, .avi (video)

    🎵 .mp3, .wav, .aac (audio)

    🖼️ .jpg, .png, .webp (image)

    📄 .pdf, .docx, .txt (document)

## ⚠️ Known Issues

    ❌ DRM-protected videos: Cannot be downloaded

    📺 TV/client formats: May be skipped (yt-dlp#12563)

    🌐 Missing formats: If not available via web client (yt-dlp#12482)


## 🧯 Troubleshooting

### No audio in output file?
Ensure FFmpeg is installed:
```bash
ffmpeg -version
```
Check the format settings in YouTubeDownloader (in downloader.py):
```bash
'format': 'bestaudio+bestvideo/best'
```

## 📚 Dependencies

    yt-dlp – Download engine

    FFmpeg – Video/audio processing

    tqdm – Progress bars

    colorama – Terminal color output

## 📄 License
[LICENSE](LICENSE)