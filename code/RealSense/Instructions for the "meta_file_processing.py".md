# Instructions for the [Frame Metadata Analysis Script](meta_file_processing.py)

This Python script analyzes a metadata file generated by the [D400_frame_capture.py](D400_frame_capture.py) script. The metadata file contains information about each captured frame, including its frame number and timestamp. The script identifies any gaps in the sequence of frame numbers (indicating dropped frames), calculates the effective frame rate (FPS), and provides a detailed report on frame continuity and performance.

## Features

- **Frame Continuity Analysis:** Identifies gaps between consecutive frame numbers, which indicate dropped or lost frames.
- **Frame Loss Reporting:** Counts and reports the number of frames lost during the capture process.
- **Effective FPS Calculation:** Calculates the effective frames per second based on the total time span of the capture and the number of frames successfully recorded.
- **Detailed Output:** Prints the frame differences and their occurrence percentages, providing insights into the capture process's reliability.

## How It Works

1. **Input:** The script reads a metadata file (e.g., `frames_meta_YYYYMMDD_HHMMSS.txt`), where each line contains:
   - Frame Number
   - Timestamp (in milliseconds since the start of the capture)
   - Delta First (time difference from the first frame in seconds)
   - Delta Previous (time difference from the previous frame in seconds)

2. **Analysis:**
   - The script processes the metadata line by line, calculating the difference between consecutive frame numbers.
   - It tracks the number of frames lost if there are gaps in the sequence of frame numbers.
   - If any frames are lost, the script prints out the relevant lines from the metadata file, along with an explanation of the fields.

3. **Output:**
   - The script outputs a summary of frame differences and their frequencies, allowing you to assess how often frames were captured continuously or with gaps.
   - It calculates and prints the effective FPS, which reflects the actual frame rate achieved during the capture.
   - The total number of frames collected and the number of frames lost are also reported.

## Script Outputs

1. **Frame Difference Summary:**
   - The script prints a table showing the difference between consecutive frame numbers and the percentage of instances each difference occurred.
   - Example output:
     ```
     Difference between frame numbers | Percentage of instances
     ----------------------------------+-----------------------
     1                                | 98.5                 
     2                                | 1.5                  
     ```

2. **Effective FPS:**
   - The script calculates and prints the effective FPS based on the time span between the first and last frame captured.
   - Example output:
     ```
     Effective FPS: 59.8
     ```

3. **Total Frames and Frames Lost:**
   - The script reports the total number of frames successfully collected and the number of frames lost during the capture process.
   - Example output:
     ```
     Total number of frames collected: 3600
     Number of frames lost: 54
     ```

4. **Lost Frame Details (if applicable):**
   - If any frames are lost, the script prints the lines from the metadata file corresponding to the last successfully captured frame before the loss and the first frame after the loss.
   - It also provides an explanation of what each field in these lines represents:
     ```
     Fields in the following lines represent: Frame Number, Timestamp, Delta First, Delta Previous
     124 123456.789 2.074 0.017
     126 123456.822 2.107 0.033
     ```

## Usage

1. **Input:** The script expects a metadata file (`frames_meta_YYYYMMDD_HHMMSS.txt`) as input, which should be located in the same directory as the script.
   
2. **Execution:** Run the script in an environment with Python 3.6+ and the NumPy library installed. The script will automatically process the metadata file and produce the outputs described above.

## Requirements

- Python 3.6+
- NumPy

This script is useful for diagnosing issues in frame capture processes, such as dropped frames or inconsistent frame rates, providing valuable feedback on the reliability and performance of your capture setup.
