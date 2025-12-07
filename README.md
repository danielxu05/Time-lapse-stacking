# Time-Lapse Video Stacker

## Description

This Python script converts a sequence of time-lapse images into a video. It stacks the images together to create a smooth transition video, ideal for time-lapse photography. The script supports multiple video formats and codecs, with automatic codec selection for optimal compatibility.

## Features

- Converts a sequence of images into a video
- Supports multiple image formats (JPG, PNG, BMP, TIFF)
- Multiple video codec options for compatibility
- **ffmpeg support** for proper H.264 encoding (recommended for Windows)
- Progress bars for both image loading and video encoding
- Automatic image resizing for mismatched dimensions
- Customizable frame rate
- Simple command-line interface

## Requirements

- Python 3.6+
- OpenCV (`opencv-python`)
- tqdm (for progress bars)
- ffmpeg (optional, but recommended for best codec support)

## Installation

1. Clone this repository to your local machine:

    ```bash
    git clone git@github.com:danielxu05/Time-lapse-stacking.git
    ```

2. Navigate to the directory:

    ```bash
    cd Time-lapse-stacking
    ```

3. Install the required packages:

    ```bash
    pip install opencv-python tqdm
    ```

4. (Optional) Install ffmpeg for better codec support:

    - **Windows**: Download from [ffmpeg.org](https://ffmpeg.org/download.html) or use `choco install ffmpeg` with Chocolatey
    - **macOS**: `brew install ffmpeg`
    - **Linux**: `sudo apt-get install ffmpeg` (Ubuntu/Debian) or `sudo yum install ffmpeg` (CentOS/RHEL)

## Usage

### Basic Usage

```bash
python main.py -i input_folder -o output_video.mp4 -f 25
```

### Recommended Usage (with ffmpeg for H.264)

For best compatibility, especially on Windows, use the `--use-ffmpeg` flag:

```bash
python main.py -i input_folder -o output_video.mp4 -f 25 --use-ffmpeg
```

This creates a proper H.264 MP4 file that works in Windows Media Player and other players.

### AVI Format (Alternative)

If you prefer AVI format with Motion JPEG codec:

```bash
python main.py -i input_folder -o output_video.avi -f 25 --avi
```

## Command-Line Arguments

- `-i`, `--input` (required): Path to the input folder containing time-lapse images
- `-o`, `--output`: Path to the output video file (default: `./video.mp4`)
- `-f`, `--frames`: Frame rate of the output video in frames per second (default: 25)
- `--avi`: Force AVI format output (uses Motion JPEG or XVID codec)
- `--use-ffmpeg`: Use ffmpeg for video encoding (creates H.264 MP4, best compatibility)

## Examples

### Example 1: Create MP4 with ffmpeg (Recommended)

```bash
python main.py -i D:\Pictures\time-lapse\images -o output.mp4 -f 30 --use-ffmpeg
```

### Example 2: Create AVI with Motion JPEG

```bash
python main.py -i ./images -o output.avi -f 24 --avi
```

### Example 3: Basic MP4 (OpenCV codecs)

```bash
python main.py -i ./images -o output.mp4 -f 25
```

## Supported Image Formats

The script automatically detects and processes images with the following extensions:
- `.jpg`, `.jpeg` (JPEG)
- `.png` (PNG)
- `.bmp` (Bitmap)
- `.tiff`, `.tif` (TIFF)

Images are processed in alphabetical order. Make sure your images are named sequentially (e.g., `image001.jpg`, `image002.jpg`, etc.) for proper ordering.

## Codec Information

### With ffmpeg (`--use-ffmpeg`)
- **Codec**: H.264 (libx264)
- **Format**: MP4
- **Compatibility**: Excellent (works in Windows Media Player, VLC, and most players)
- **Quality**: High (CRF 23, medium preset)

### Without ffmpeg (OpenCV)
- **MP4**: Tries H.264/AVC1, falls back to MPEG-4 Part 2
- **AVI**: Uses Motion JPEG (MJPG) or XVID
- **Compatibility**: Varies by codec and player

## Troubleshooting

### Error: `0xc00d36b4` in Windows Media Player

This error indicates a codec compatibility issue. Solutions:

1. **Use ffmpeg** (recommended):
   ```bash
   python main.py -i input_folder -o output.mp4 -f 25 --use-ffmpeg
   ```

2. **Use AVI format**:
   ```bash
   python main.py -i input_folder -o output.avi -f 25 --avi
   ```

3. **Use VLC Media Player** (plays most codecs)

### Error: "Could not open video writer"

This means no compatible codec was found. Try:
- Installing ffmpeg and using `--use-ffmpeg`
- Using `--avi` flag for AVI format
- Checking that OpenCV is properly installed: `pip install --upgrade opencv-python`

### Images with Different Sizes

The script automatically resizes images to match the first image's dimensions. A warning message will be displayed when resizing occurs.

### No Images Found

Make sure:
- The input path is correct
- Images are in the specified directory (not subdirectories)
- Images have supported extensions (see "Supported Image Formats" above)

## License

[Add your license information here]

## Contributing

[Add contribution guidelines here]
