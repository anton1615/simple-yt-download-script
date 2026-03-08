# Simple YouTube Download Script

A collection of Python scripts for downloading YouTube videos, live streams, and chat archives.

## Security Notice

> This repository may be used alongside API keys, browser cookies, logs, and exported chat or analytics data that can contain sensitive information.
> Do not publish or sync working directories, cookie files, environment files, or generated output blindly.
> Review any archive, CSV, JSON, or log artifacts before sharing them with others.

## Features

- **Live Stream Archiving**: Download live streams with chat archives in parallel
- **VOD Downloading**: Batch download videos with chat history
- **Chat Export**: Export live chat to TXT, CSV, and JSON formats (including Super Chats)
- **Super Chat Analytics**: Analyze and aggregate Super Chat data with currency conversion
- **Twitcasting Support**: Record Twitcasting live streams
- **Channel Batch Processing**: Download all videos from a channel's upload playlist

## Scripts Overview

| Script | Description |
|--------|-------------|
| `archive.py` | Archive live streams with metadata and chat (no cookies) |
| `archive_cookies.py` | Archive live streams with cookie authentication |
| `vod_video_downloader.py` | Download single VOD with format selection |
| `vod_batch_downloader.py` | Batch download VODs from URL list |
| `vod_chat_downloader.py` | Download chat archives for a single video |
| `channel_chat_downloader.py` | Batch download chat from channel's recent videos |
| `import_all_sc.py` | Aggregate Super Chat data with currency conversion |
| `tc_record.py` | Record Twitcasting live streams |

## Requirements

### External Dependencies

- **yt-dlp**: Video/audio downloader - [https://github.com/yt-dlp/yt-dlp](https://github.com/yt-dlp/yt-dlp)
- **ytarchive**: Live stream archiver - [https://github.com/Kethsar/ytarchive](https://github.com/Kethsar/ytarchive)
- **chat_downloader**: Chat archive tool - [https://github.com/xenova/chat-downloader](https://github.com/xenova/chat-downloader)
- **ffmpeg**: Media conversion (for Twitcasting) - [https://ffmpeg.org/](https://ffmpeg.org/)

### Python Dependencies

```bash
pip install -r requirements.txt
```

### Environment Setup

1. Copy `.env.example` to `.env`:
   ```bash
   cp .env.example .env
   ```

2. Get a YouTube Data API v3 key from [Google Cloud Console](https://console.cloud.google.com/apis/credentials)

3. Set your API key in `.env`:
   ```
   YOUTUBE_API_KEY=your_api_key_here
   ```

4. (Optional) Export cookies from your browser for accessing members-only content:
   - Use browser extensions like "Get cookies.txt LOCALLY"
   - Save as `cookies.txt` or `youtube.com_cookies.txt`

## Usage

### Archive a Live Stream

```bash
python archive.py
# Input YouTube live stream URL when prompted
```

This will:
1. Create a folder named `{date} {title}`
2. Download video via yt-dlp and ytarchive (parallel)
3. Export chat to TXT, CSV, and JSON formats

### Batch Download VODs

1. Create `download.txt` with video URLs (one per line)
2. Run:
   ```bash
   python vod_batch_downloader.py
   ```

### Download Chat Only

```bash
python vod_chat_downloader.py
# Input YouTube video URL when prompted
```

### Channel Chat Batch Download

```bash
python channel_chat_downloader.py
# Input channel ID and delay between downloads
```

### Super Chat Analytics

```bash
python import_all_sc.py
# Processes all JSON files in current directory
# Outputs: sc_total.csv, sc_daily.csv, sc_user.csv
```

### Twitcasting Recording

```bash
python tc_record.py
# Input Twitcasting URL when prompted
```

## Output Format

### File Naming Convention
```
{YYYYMMDD}[{video_id}].{ext}
```

### Chat Export Formats
- **TXT**: Plain text chat log
- **CSV**: Structured chat data
- **JSON**: Full chat data including Super Chats

### Super Chat Analysis Output
- `sc_total.csv`: Total Super Chats by currency
- `sc_daily.csv`: Daily Super Chat totals
- `sc_user.csv`: Per-user Super Chat statistics

## Technical Specifications

### API Usage
- YouTube Data API v3 for video metadata
- WebSocket for Twitcasting streams

### Threading
- Parallel downloads using Python `threading` module
- Separate threads for video and chat downloads

### Currency Conversion
- Real-time exchange rates from [exchangerate-api.com](https://api.exchangerate-api.com)

## Security Notes

- **Never commit** `cookies.txt` or `youtube.com_cookies.txt` - they contain session tokens
- **Never commit** your API key - use environment variables
- The `.gitignore` file excludes sensitive files by default

## License

This project is for personal use. Please respect YouTube's Terms of Service and content creators' rights.

## Disclaimer

This tool is provided as-is for archiving purposes. Users are responsible for complying with YouTube's Terms of Service and applicable laws regarding content downloading.
