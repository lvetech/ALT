import os
import cv2
import time
import numpy as np
import pyrealsense2 as rs
from multiprocessing import Process, Array, Value
from datetime import datetime

# Configuration variables for the infrared and depth streams
infrared_stream_index = 1
infrared_width = 848
infrared_height = 480
infrared_format = rs.format.y8
infrared_fps = 60

depth_width = 848
depth_height = 480
depth_format = rs.format.z16
depth_fps = 60

# Duration to capture frames and calculate the number of frames to collect
capture_duration = 60  # seconds
frames_to_collect = capture_duration * infrared_fps

def capture_frames(shared_frame, shared_frame_number, stop_signal):
    """
    Capture infrared and depth frames using the Intel RealSense camera, save them to disk,
    and share the latest infrared frame with another process.

    Args:
        shared_frame (Array): Shared memory array to hold the latest infrared frame.
        shared_frame_number (Value): Shared memory value to hold the current frame number.
        stop_signal (Value): Shared memory value used as a flag to stop the capture process.
    """
    prev_frame_time = time.time()
    display_frame_rate = 1  # Frames per second to display
    number_of_frames = 0

    # Initialize the Intel RealSense camera
    pipeline = rs.pipeline()
    config = rs.config()

    # Configure the camera settings
    config.enable_stream(rs.stream.infrared, infrared_stream_index, infrared_width, infrared_height, infrared_format, infrared_fps)
    config.enable_stream(rs.stream.depth, depth_width, depth_height, depth_format, depth_fps)

    # Start the camera
    profile = pipeline.start(config)

    # Set the laser power to maximum for better depth accuracy
    device = profile.get_device()
    depth_sensor = device.first_depth_sensor()
    depth_sensor.set_option(rs.option.laser_power, depth_sensor.get_option_range(rs.option.laser_power).max)

    # Enable auto exposure for depth sensor
    depth_sensor.set_option(rs.option.enable_auto_exposure, 1)

    # Create a folder to save frames with a timestamped name
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    frames_dir = os.path.abspath(f"Frames_{ts}")
    os.makedirs(frames_dir, exist_ok=True)

    # Create a metadata file to log frame numbers and timestamps
    with open(f"frames_meta_{ts}.txt", "w") as meta_file:
        first_timestamp = None
        prev_timestamp = None

        try:
            while not stop_signal.value:
                # Wait for the next set of frames
                frames = pipeline.wait_for_frames()
                ir_frame = frames.get_infrared_frame(infrared_stream_index)

                # Get frame number and timestamp
                frame_number = ir_frame.get_frame_number()
                timestamp = ir_frame.get_timestamp()

                # Calculate time deltas and write metadata
                if first_timestamp is None:
                    first_timestamp = timestamp
                delta_first = (timestamp - first_timestamp) / 1000  # milliseconds to seconds
                if prev_timestamp is not None:
                    delta_prev = (timestamp - prev_timestamp) / 1000  # milliseconds to seconds
                    meta_file.write(f"{frame_number} {timestamp} {delta_first} {delta_prev}\n")
                else:
                    meta_file.write(f"{frame_number} {timestamp} {delta_first} NaN\n")

                prev_timestamp = timestamp

                # Convert the IR frame to a NumPy array
                ir_image = np.asanyarray(ir_frame.get_data(), dtype=np.uint8)

                # Share the current frame with the display process
                current_time = time.time()
                if current_time - prev_frame_time >= 1 / display_frame_rate:
                    with shared_frame.get_lock():
                        np.copyto(np.frombuffer(shared_frame.get_obj(), dtype=np.uint8).reshape(infrared_height, infrared_width), ir_image)
                    with shared_frame_number.get_lock():
                        shared_frame_number.value = frame_number
                    prev_frame_time = current_time

                # Save the IR frame to disk
                frame_file_path = os.path.join(frames_dir, f"{frame_number:09d}.dat")
                with open(frame_file_path, "wb") as frame_file:
                    frame_file.write(ir_image.tobytes())

                number_of_frames += 1
                if number_of_frames == frames_to_collect:
                    stop_signal.value = True
                    continue

                # Check for stop signal after each frame
                if stop_signal.value:
                    break

        finally:
            # Stop the camera
            pipeline.stop()

def display_frames(shared_frame, shared_frame_number, stop_signal):
    """
    Display infrared frames in real-time using OpenCV.

    Args:
        shared_frame (Array): Shared memory array containing the latest infrared frame.
        shared_frame_number (Value): Shared memory value holding the current frame number.
        stop_signal (Value): Shared memory value used as a flag to stop the display process.
    """
    cv2.namedWindow("IR Frame", cv2.WINDOW_AUTOSIZE)
    last_displayed_frame_number = -1

    while not stop_signal.value:
        with shared_frame_number.get_lock():
            current_frame_number = shared_frame_number.value
        if current_frame_number != last_displayed_frame_number:
            with shared_frame.get_lock():
                ir_image = np.frombuffer(shared_frame.get_obj(), dtype=np.uint8).reshape(infrared_height, infrared_width).copy()
            last_displayed_frame_number = current_frame_number

            # Display the frame using OpenCV
            cv2.imshow("IR Frame", ir_image)

        key = cv2.waitKey(1)
        if key & 0xFF == ord("q"):
            stop_signal.value = True
            cv2.destroyAllWindows()


if __name__ == "__main__":
    # Shared memory for communication between processes
    shared_frame = Array('B', infrared_height * infrared_width)
    shared_frame_number = Value('i', -1)
    stop_signal = Value('i', 0)

    # Start the capture and display processes
    capture_process = Process(target=capture_frames, args=(shared_frame, shared_frame_number, stop_signal))
    display_process = Process(target=display_frames, args=(shared_frame, shared_frame_number, stop_signal))

    capture_process.start()
    display_process.start()

    # Wait for both processes to complete
    capture_process.join()
    display_process.join()
