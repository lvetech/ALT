# Instructions for the [Frame Capture Script for D400-Series Intel RealSense Cameras](RealSense/D400_frame_capture.py)

This Python script is designed to capture infrared (IR) frames from Intel RealSense D400 series cameras. It displays the infrared frames in real-time using OpenCV, saves the captured IR frames to disk, and logs metadata related to each frame, such as frame numbers and timestamps. The script is tailored for use with the Intel RealSense D400 series cameras, which are powerful depth-sensing devices widely used in various applications, including robotics, 3D scanning, and computer vision. You can learn more about the Intel RealSense D400 series on [Intel's website](https://www.intelrealsense.com/).

## Features

- **Real-time Frame Capture:** Captures infrared frames at a specified frame rate (e.g., 60 FPS) using Intel RealSense D400 series cameras.
- **Frame Display:** Displays the captured infrared frames at a specified display rate (e.g., 1 FPS) in real-time using OpenCV.
- **Frame Storage:** Saves each captured infrared frame to the disk in binary format.
- **Metadata Logging:** Creates a metadata file that logs frame numbers and timestamps for later analysis.

## How It Works

1. **Initialization:**
   - The script initializes the Intel RealSense camera and configures it to capture infrared and depth streams.
   - The camera's laser power is set to maximum, and auto exposure is enabled.

2. **Capture Process:**
   - The `capture_frames` function captures infrared frames from the camera, converts them into a NumPy array, and saves them to a shared memory array that can be accessed by other processes.
   - Each frame is saved to the disk in a binary `.dat` file.
   - A metadata file logs the frame number and timestamp, along with time deltas from the first frame and the previous frame.

3. **Display Process:**
   - The `display_frames` function runs concurrently with the capture process, fetching the latest frame from the shared memory array and displaying it using OpenCV.
   - The display process can be terminated by pressing the "q" key.

4. **Termination:**
   - The capture and display processes automatically terminate after capturing a predefined number of frames or when the user presses the "q" key.

## Important Considerations

- **Frame Loss and Computational Resources:**
  The percentage of frames that are not captured heavily depends on the computational resources of the computer running the script and the resources available to the script during execution. Insufficient resources can lead to dropped frames, especially when running at high frame rates. 

- **Performance Enhancement:**
  Implementing the functionality of this script in C/C++ is recommended for applications requiring high reliability and minimal frame loss. A C/C++ implementation should significantly reduce the number of lost frames due to more efficient resource management and lower computational overhead.

## Metadata File Structure

The script generates a metadata file named `frames_meta_YYYYMMDD_HHMMSS.txt`, where `YYYYMMDD_HHMMSS` represents the timestamp when the script was executed. The metadata file contains the following information:

- **Frame Number:** The frame number obtained from the metadata of the captured frame.
- **Timestamp:** The timestamp of the captured frame, obtained from the metadata of the captured frame, in milliseconds since the camera started.
- **Delta First:** The time difference in seconds between the current frame and the first captured frame.
- **Delta Previous:** The time difference in seconds between the current frame and the previous frame. If the frame is the first frame, this value is `NaN`.

Example metadata file format:
```
Frame_Number Timestamp Delta_First Delta_Previous
1            123456.789 0.000       NaN
2            123456.923 0.134       0.134
...
```

## Frame Storage

Captured infrared frames are stored as binary files in a folder named `Frames_YYYYMMDD_HHMMSS`, where `YYYYMMDD_HHMMSS` corresponds to the timestamp of when the script started. Each frame is saved in a file named `000000001.dat`, `000000002.dat`, etc., where the number corresponds to the frame number, zero-padded to nine digits.

The frames are stored as raw binary data in `.dat` files, where each file contains the pixel values of a single infrared frame. The files can be read back into a NumPy array for further processing or analysis.

## Usage

To run the script, simply execute it in an environment where the required dependencies (`pyrealsense2`, `opencv-python`, `numpy`, etc.) are installed. The script will automatically start capturing and displaying frames, saving them to disk, and logging the metadata.

## Requirements

- Python 3.6+
- Intel RealSense SDK (`pyrealsense2`)
- OpenCV (`opencv-python`)
- NumPy
- Multiprocessing

## Further Analysis

For detailed analysis of the captured frames, such as determining the percentage of lost frames and calculating the effective FPS, you can use a complementary script available [here](./) (placeholder link). This second script reads the metadata file created by the frame capture process and provides detailed statistics on frame continuity and performance. This analysis can help you understand the impact of computational resource limitations on frame capture reliability.
