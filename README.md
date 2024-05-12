# Time-Lapse Video Stacker


## Description

This Python script converts a sequence of time-lapse images into a video. It stacks the images together to create a smooth transition video, ideal for time-lapse photography.

## Features

- Converts a sequence of images into a video.
- Smooth transition between images.
- Customizable parameters (frame rate).
- Simple to use.

## Installation

1. Clone this repository to your local machine:

    ```bash
    git clone git@github.com:danielxu05/Time-lapse-stacking.git
    ```

2. Navigate to the directory:

    ```bash
    cd your-repository
    ```

3. Install the required packages:

    ```bash
    pip install opencv-python
    ```

## Usage

1. Place your time-lapse images in a folder (e.g., `input_images`).
2. Run the Python script:

    ```bash
    python main.py -i input_images -o output_video.mp4 -f 25
    ```

    Replace `input_images` with the path to your input folder and `output_video.mp4` with the desired name for your output video file.

## Parameters

- `-i`, `--input`: Path to the input folder containing time-lapse images.
- `-o`, `--output`: Path to the output video file.
- `-f`, `--frame_rate`: Frame rate of the output video (default: 25).
