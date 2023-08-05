# VideoJoiner

[![PyPI version](https://badge.fury.io/py/videojoiner.svg)](https://badge.fury.io/py/videojoiner)

Videojoiner is now a Gooey program used to join video files together.
Documentation to come.

The ffmpeg binaries are stored in `%APPDATA%/videojoiner/ffmpeg` and will only be downloaded if missing or the '-d/--force-download' flag is passed.

The output filename can be specified, or it will autogenerate a video file formatted `merged_video_YYMMDD_HHMMSS.EXT` where the extension is copied from the first file in the input list.

## Install

```
pip install videojoiner
```
