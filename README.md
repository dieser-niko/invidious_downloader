# POC Invidious Downloader

This is a proof-of-concept to download videos from YouTube. Focus here is audio-only, so no video download.

The script saves the success rate of each instance, so it might be faster on the second run.

I just threw this script together, so please don't try to learn how to program from this.

## Usage
Install requirements:
```bash
# virtual environment for Linux
python3 -m venv .venv
source .venv/bin/activate

# virtual environment for Windows
python -m venv .venv
.venv\Scripts\activate

pip install -r requirements.txt
```

And then execute. Video ID can only submitted like this.
```bash
python main.py dQw4w9WgXcQ
```

There are some args, just use `python main.py -h` to check it out.

## FFMPEG

Install ffmpeg. On Windows just throw in the executable in the same directory. On Linux.. Find out yourself.

Then you can pass the output file like this:
```bash
python main.py dQw4w9WgXcQ --ffmpeg output.mp3
```
