# YouTube Video Transcription Tool

A Python script that downloads audio from YouTube videos and transcribes them to text using OpenAI's Whisper model. The tool is specifically configured for Polish language transcription but can be adapted for other languages.

## Features

- Download audio from YouTube videos using `yt-dlp`
- Transcribe audio to text using OpenAI Whisper
- Automatic cleanup of temporary audio files
- Unique transcript file naming with video ID and timestamp
- Polish language transcription by default
- File size validation and error handling

## Prerequisites

- Python 3.7 or higher
- `yt-dlp` (for YouTube audio downloading)
- `ffmpeg` (required by yt-dlp for audio processing)

### Installing System Dependencies

**macOS (using Homebrew):**

```bash
brew install ffmpeg
brew install yt-dlp
```

**Ubuntu/Debian:**

```bash
sudo apt update
sudo apt install ffmpeg
sudo apt install yt-dlp
```

**Windows:**

- Download ffmpeg from [https://ffmpeg.org/download.html](https://ffmpeg.org/download.html)
- Download yt-dlp from [https://github.com/yt-dlp/yt-dlp](https://github.com/yt-dlp/yt-dlp)
- Add both to your system PATH

## Installation

1. Clone or download this repository
2. Set up the virtual environment and install Python dependencies:

```bash
# Make the setup script executable
chmod +x setup_venv.sh

# Run the setup script
./setup_venv.sh
```

Or manually:

```bash
# Create virtual environment
python3 -m venv .venv

# Activate virtual environment
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

## Usage

1. Activate the virtual environment:

```bash
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

2. Run the script:

```bash
python whisper_transcribe_pl.py
```

3. Enter the YouTube URL when prompted

4. The script will:
   - Download the audio from the YouTube video
   - Transcribe it using Whisper
   - Save the transcript as a text file with format: `transkript_{video_id}_{timestamp}.txt`

## Configuration

### Language Settings

The script is configured for Polish (`pl`) by default. To change the language, modify the `lang` parameter in the `transcribe` function call:

```python
transcribe(audio_path, video_id=video_id, lang="en")  # For English
```

### Whisper Model

The script uses the "large" Whisper model by default for best accuracy. You can change this to a smaller model for faster processing:

- `tiny`: Fastest, least accurate
- `base`: Fast, basic accuracy
- `small`: Balanced speed/accuracy
- `medium`: Good accuracy, slower
- `large`: Best accuracy, slowest

Change the model in the `transcribe` function call:

```python
transcribe(audio_path, model_name="medium", video_id=video_id)
```

## Output

- Transcript files are saved in the current directory with the format: `transkript_{video_id}_{timestamp}.txt`
- Temporary audio files are stored in `temp_audio/` directory and cleaned up automatically
- Console output provides progress updates and status information

## Troubleshooting

### Common Issues

1. **"yt-dlp not found"**: Make sure yt-dlp is installed and available in your system PATH
2. **"ffmpeg not found"**: Install ffmpeg as described in the prerequisites
3. **Small audio file warning**: The downloaded audio file is very small, which might indicate a download failure
4. **Permission errors**: Make sure you have write permissions in the current directory

### Dependencies Not Installing

If you encounter issues with installing the Python dependencies, try:

```bash
pip install --upgrade pip
pip install --no-cache-dir -r requirements.txt
```

## License

This project is provided as-is for educational and personal use. Please respect YouTube's terms of service when using this tool.

## Contributing

Feel free to submit issues or pull requests to improve this tool.
