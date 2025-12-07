import cv2
import glob
import argparse
import os
import subprocess
import sys
from tqdm import tqdm

def check_ffmpeg():
    """Check if ffmpeg is available"""
    try:
        subprocess.run(['ffmpeg', '-version'], 
                      stdout=subprocess.PIPE, 
                      stderr=subprocess.PIPE, 
                      check=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False

def image2video_ffmpeg(input_dir, output_file, frames):
    """Create video using ffmpeg (better codec support)"""
    # Get all image files
    image_extensions = ['*.jpg', '*.jpeg', '*.png', '*.bmp', '*.tiff', '*.tif']
    image_files = []
    for ext in image_extensions:
        pattern = os.path.join(input_dir, ext)
        image_files.extend(glob.glob(pattern, recursive=False))
        pattern = os.path.join(input_dir, ext.upper())
        image_files.extend(glob.glob(pattern, recursive=False))
    
    if not image_files:
        print(f'Error: No image files found in {input_dir}')
        return False
    
    image_files = sorted(image_files)
    print(f'Found {len(image_files)} image files')
    
    # Create a temporary file list for ffmpeg
    import tempfile
    with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False, encoding='utf-8') as f:
        for img_file in image_files:
            # Use absolute path and escape for ffmpeg
            abs_path = os.path.abspath(img_file).replace('\\', '/')
            f.write(f"file '{abs_path}'\n")
        concat_file = f.name
    
    try:
        # Use ffmpeg to create video with H.264
        cmd = [
            'ffmpeg', '-y',  # Overwrite output
            '-f', 'concat',
            '-safe', '0',
            '-i', concat_file,
            '-c:v', 'libx264',
            '-pix_fmt', 'yuv420p',
            '-r', str(frames),
            '-preset', 'medium',
            '-crf', '23',
            output_file
        ]
        
        print(f'Using ffmpeg to create video with H.264 codec...')
        
        # Run ffmpeg and parse progress from stderr
        import re
        import threading
        
        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        # Create progress bar
        total_frames = len(image_files)
        pbar = tqdm(total=total_frames, desc='Encoding video', unit='frame')
        
        frame_count = 0
        error_output = []
        error_lock = threading.Lock()
        
        def read_stderr():
            """Read stderr in a separate thread"""
            nonlocal frame_count, error_output
            while True:
                line = process.stderr.readline()
                if not line:
                    break
                with error_lock:
                    error_output.append(line)
                    # Parse frame number from ffmpeg output
                    # Format: frame=  123 fps=...
                    frame_match = re.search(r'frame=\s*(\d+)', line)
                    if frame_match:
                        new_frame_count = int(frame_match.group(1))
                        if new_frame_count > frame_count:
                            pbar.update(new_frame_count - frame_count)
                            frame_count = new_frame_count
        
        # Start reading stderr in a separate thread
        stderr_thread = threading.Thread(target=read_stderr)
        stderr_thread.daemon = True
        stderr_thread.start()
        
        # Wait for process to complete
        return_code = process.wait()
        stderr_thread.join()
        pbar.close()
        
        if return_code == 0:
            print('Video created successfully with ffmpeg!')
            return True
        else:
            error_msg = ''.join(error_output)
            print(f'ffmpeg error: {error_msg}')
            return False
    finally:
        # Clean up temp file
        try:
            os.unlink(concat_file)
        except:
            pass

def image2video(input_dir, output_file, frames):
    img_array = []
    size = None
    
    # Common image extensions
    image_extensions = ['*.jpg', '*.jpeg', '*.png', '*.bmp', '*.tiff', '*.tif']
    
    # Get all image files from the directory
    image_files = []
    for ext in image_extensions:
        pattern = os.path.join(input_dir, ext)
        image_files.extend(glob.glob(pattern, recursive=False))
        # Also try uppercase extensions
        pattern = os.path.join(input_dir, ext.upper())
        image_files.extend(glob.glob(pattern, recursive=False))
    
    if not image_files:
        print(f'Error: No image files found in {input_dir}')
        return
    
    # Sort files naturally
    image_files = sorted(image_files)
    print(f'Found {len(image_files)} image files')
    
    print('loading files...')
    for filename in tqdm(image_files):
        img = cv2.imread(filename)
        if img is None:
            print(f'Warning: Could not read {filename}, skipping...')
            continue
        height, width, layers = img.shape
        if size is None:
            size = (width, height)
        elif size != (width, height):
            print(f'Warning: Image {filename} has different size ({width}x{height}), resizing to match...')
            img = cv2.resize(img, size)
        img_array.append(img)
    
    if not img_array:
        print('Error: No valid images were loaded')
        return
    
    print(f'loaded {len(img_array)} files')
    
    # Determine codec based on file extension
    file_ext = os.path.splitext(output_file)[1].lower()
    
    if file_ext == '.mp4':
        # For MP4, try codecs in order of compatibility
        codecs_to_try = [
            ('avc1', 'H.264/AVC1 (best for MP4)'),
            ('H264', 'H.264'),
            ('mp4v', 'MPEG-4 Part 2'),
        ]
    else:
        # For AVI or other formats, use MJPG first (most compatible)
        codecs_to_try = [
            ('MJPG', 'Motion JPEG (most compatible)'),
            ('XVID', 'XVID'),
            ('DIVX', 'DivX'),
        ]
    
    out = None
    used_codec = None
    for codec, description in codecs_to_try:
        try:
            fourcc = cv2.VideoWriter_fourcc(*codec)
            out = cv2.VideoWriter(output_file, fourcc, frames, size)
            if out.isOpened():
                used_codec = description
                print(f'Using codec: {description}')
                break
            else:
                if out:
                    out.release()
                out = None
        except Exception as e:
            if out:
                out.release()
            out = None
            continue
    
    if out is None or not out.isOpened():
        # Last resort: try writing as AVI with XVID
        if file_ext == '.mp4':
            print('Warning: Could not create MP4 with available codecs.')
            print('Trying AVI format with XVID codec instead...')
            avi_output = os.path.splitext(output_file)[0] + '.avi'
            fourcc = cv2.VideoWriter_fourcc(*'XVID')
            out = cv2.VideoWriter(avi_output, fourcc, frames, size)
            if out.isOpened():
                print(f'Created AVI file instead: {avi_output}')
                output_file = avi_output
            else:
                print(f'Error: Could not open video writer')
                print('Tried multiple codecs. You may need to install additional codecs.')
                return
        else:
            print(f'Error: Could not open video writer for {output_file}')
            return
     
    print(f'writing to {output_file}....')
    for i in tqdm(range(len(img_array))):
        out.write(img_array[i])
    out.release()
    print('exported.')


def main(args):
    # Access the argument values
    if not args.input:
        print('Error: Input directory is required. Use -i or --input to specify the directory.')
        return
    
    input_dir = args.input
    if not os.path.isdir(input_dir):
        print(f'Error: Input path "{input_dir}" is not a valid directory')
        return
    
    if args.output:
        output = args.output
    else:
        output = './video.mp4'
    
    # Force AVI format if requested
    if args.avi:
        output = os.path.splitext(output)[0] + '.avi'
    
    if args.frames:
        frames = int(args.frames)
    else:
        frames = 25
    
    # Use ffmpeg if requested and available
    if args.use_ffmpeg:
        if check_ffmpeg():
            success = image2video_ffmpeg(input_dir, output_file=output, frames=frames)
            if not success:
                print('Falling back to OpenCV...')
                image2video(input_dir, output_file=output, frames=frames)
        else:
            print('ffmpeg not found. Install ffmpeg for better codec support.')
            print('Falling back to OpenCV...')
            image2video(input_dir, output_file=output, frames=frames)
    else:
        image2video(input_dir, output_file=output, frames=frames)
    
if __name__ == "__main__":
    # Create a parser
    parser = argparse.ArgumentParser(description="stack images to video")

    # Add arguments
    parser.add_argument('-i', '--input', required=True, help='input directory containing images')
    parser.add_argument('-o', '--output', help='output video file (default: ./video.mp4)')
    parser.add_argument('-f', '--frames', type=int, help='frames per second (default: 25)')
    parser.add_argument('--avi', action='store_true', help='force AVI format (better Windows compatibility)')
    parser.add_argument('--use-ffmpeg', action='store_true', help='use ffmpeg for encoding (requires ffmpeg installed, best for H.264 MP4)')
    
    # Parse the arguments
    args = parser.parse_args()

    # Call the main function with parsed arguments
    main(args)



