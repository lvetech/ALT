## The Artificial Light Texture (ALT) technology for vital signs (heartbeats, respiration), sleep, and motor activity monitoring.
### *"A motion capture suite made out of light"*.

The Artificial Light Texture (ALT) technology allows obtaining heart rate and respiration rate information for a person as well as information about other mechanical movements of the person’s body in a non-contact fashion and in real time.

Skin does not have to be exposed to a camera for ALT to work [1, 2, 3, 4]. ALT does not use depth data to obtain the vital signs information [1-4].

ALT can use inexpensive computing and image capture devices such as Raspberry Pi single-board computer [5] and Pi NoIR camera [6] and is compatible with light emitting elements of various consumer electronics devices such as light projectors of standalone or embedded depth sensing systems like Microsoft Kinect ([7]; see below), Intel RealSense cameras [8-10], and Occipital Structure Sensor ([11]; see [Non-contact vital signs monitoring on mobile devices: an iPad + Structure Sensor example](https://www.linkedin.com/pulse/non-contact-vital-signs-monitoring-mobile-devices-ipad-misharin/)). We discuss the ALT tech -based pulse and respiration monitoring using RealSense cameras [here](/code/RealSense/README-RealSense.md).

Three key hardware components of an ALT system are:

![An ALT system](/figures/An-ALT-system.jpg)

A computer, a video camera, and a light source which generates artificial light texture.

The light source element illuminates a set of areas of a person’s body thus imparting an additional (to the natural and/or artificial ambient light) light texture to a part of the person’s body. We call that additional light texture the “artificial light texture” or “ALT”. We call the distinct illumination areas of the added light texture its “elements”. Application of the ALT can increase illumination contrast in the scene observed by a camera. 

Movements of the person’s body which are related to the person’s respiration and/or heartbeats lead to variations in one or more of the illumination distribution, shape distribution, size distribution, location distribution of the elements of the added light texture and/or to variations in the number of those elements.  

These variations are captured by a video camera element in a set of video frames which are processed by a computing element to result in the numeric values representative of the heart rate and/or respiration rate of the person.

**You can think about ALT as putting a person in a motion capture suite made out of light**.

Note that the ALT can cover parts of the objects which are in contact (direct or via other objects) with the person’s body (e.g. a chair, a blanket, a bed, floor, etc.) and movements or variations in the shape of such objects resulting from the movements of the person’s body imparted to them can be picked up in the ALT data too. This is why the ALT systems can detect heartbeats and respiration even when a person is completely hidden under a thick blanket [2]. 

In one implementation of the ALT technology that we will describe here the light source element is the infrared light projector of a Microsoft Kinect for Xbox 360 system, the computing element is a Raspberry Pi single-board computer, and the video camera element is a Pi NoIR camera. Both the Kinect system and the Pi NoIR camera are connected to and controlled by the Raspberry Pi single-board computer.

The infrared light projector of the Microsoft Kinect for Xbox 360 system illuminates a scene observed by the Pi NoIR camera. 

Further, video encoding for the video frames captured by the Pi NoIR camera into H.264 format [12] is performed using the Raspberry Pi single-board computer and functionality provided by the Picamera library [13].

Further, a set of the sum of absolute differences (SAD) values [14] is obtained for (ideally) each of the encoded video frames using the Raspberry Pi single-board computer and functionality provided by the Picamera library.

Further, the sum of the SAD values in the obtained SAD values set (the sSAD value) is calculated using the Raspberry Pi single-board computer for each of the encoded video frames for which the SAD values set was obtained.

Python code which runs on a Raspberry Pi single-board computer having a Pi NoIR camera connected to it and implements the video frames capture and processing steps described above can be found [here](/code/simple-ALT-raw.py).

The calculated sSAD values contain information about the respiration and/or heartbeats and/or other mechanical movements of a person observed by the Pi NoIR camera over the time period covered by the encoded video frames. Numeric values representative of the respiration rate and/or heart rate of the person over that time period can be obtained, for example, by performing Fourier analysis [15] of the sSAD values.

[Note that the added “artificial light texture” plays the role of an amplification medium for small body movements and its application to a person's body can lead to orders of magnitude increase in the ALT-signal (sSAD values) components related to the heart activity and/or respiration of the person compared to the case when there is no “artificial light texture” (e.g. when the ALT-generating light emitter is switched off) and only the “natural light texture” is present during the otherwise equivalent data collection and processing procedure.](/research/amplification.md)

Note that the ‘baseline’ of the sSAD values can be in the range of hundreds of thousands while the heartbeats/respiration/other movements signal can have just several percent amplitude relative to the ‘baseline’ even when the “artificial light texture” is applied to a person's body.

As a practical starting point, the Kinect system can be placed at approximately 5 feet distance from a person with the Pi NoIR camera placed in the vicinity of the Kinect. The distance between the Kinect and the person can affect how pronounced the heartbeat signal will be during the respiration events (inhale/exhale sequence). Generally, the closer Kinect gets to the person the less pronounced the heartbeat signal component in the ALT data becomes during respiration events. An example of the same effect for Intel RealSense cameras can be found [here](/research/dependence-on-distance/RealSense/distance-RealSense.md). Note also that at a large enough distance between the Kinect and the person there will be virtually no discernable pulse or respiration signal in the ALT data. Adjustments of the Kinect and the camera positions can be made, for example, based on observing visualizations of the collected ALT data.

An example of the ALT data captured by the embodiment of the ALT technology described above is shown in the figure below [1]. Real-time data collection was performed at 49 data points per second rate with simultaneous HD video (720p) recording. A person was at 1.5 meters (5 feet) distance from the camera. The camera observed 2/3 of the person's body. Determined rates are:

Respiration rate: 0.24 Hz or 14 respiration cycles per minute.

Heart rate: 1.12 Hz or 67 heartbeats per minute.

![ALT data example](/figures/ALT-data-example.jpg)

Though the ALT system described above can operate in virtually any lighting environment, an optical band pass filter which matches the wavelengths of the Kinect projector can be used with the Pi NoIR camera to reduce effects of fast (relative to the duration of a heartbeat or an inhale/exhale sequence) large-amplitude ambient light intensity variations such as the ones produced by incandescent light bulbs (at e.g. 60 Hz in the U.S.), especially if the incandescent light bulbs are the only source of light for a scene.

Note that implementations of the ALT technology components (hardware, software) other than the one described above are possible. For example, ALT systems can use Intel RealSense cameras which generate both static (R200 [9], D415 [16], D435 [16]) and dynamic (F200 [10]) light patterns [4]. The ALT technology can use light source elements which emit light on different wavelengths either visible or invisible to a human eye, depending on the needs of a particular application.  

We plan to discuss several alternative implementations of the ALT technology separately. We also plan to discuss certain applications of the ALT technology such as the ones previously described [3, 4] and others, and to provide code examples for those applications.

**Update**: We describe heartbeats and respiration monitoring using the ALT systems based on the Intel RealSense cameras [here](/code/RealSense/README-RealSense.md).

**References**:

1. “Non-contact real-time monitoring of heart and respiration rates using Artificial Light Texture" https://www.linkedin.com/pulse/use-artificial-light-texture-non-contact-real-time-heart-misharin

2. “What has happened while we slept?" https://www.linkedin.com/pulse/what-has-happened-while-we-slept-alexander-misharin

3. “When your heart beats” https://www.linkedin.com/pulse/when-your-heart-beats-alexander-misharin

4. “ALT pulse and respiration monitoring using Intel RealSense cameras" https://www.linkedin.com/pulse/alt-pulse-respiration-monitoring-using-intel-cameras-misharin

5. https://www.raspberrypi.org/

6. https://www.raspberrypi.org/products/pi-noir-camera-v2/

7. “Kinect” https://en.wikipedia.org/wiki/Kinect

8. http://www.intel.com/content/www/us/en/architecture-and-technology/realsense-overview.html

9. “Introducing the Intel® RealSenseTM R200 Camera (world facing)” https://software.intel.com/en-us/articles/realsense-r200-camera

10. “Can Your Webcam Do This? - Exploring the Intel® RealSenseTM 3D Camera (F200)” https://software.intel.com/en-us/blogs/2015/01/26/can-your-webcam-do-this 

11. “3D scanning, augmented reality, and more for mobile devices”, https://structure.io 

12. "H.264/MPEG-4 AVC" https://en.wikipedia.org/wiki/H.264/MPEG-4_AVC

13. http://picamera.readthedocs.io

14. "Sum of absolute differences" https://en.wikipedia.org/wiki/Sum_of_absolute_differences

15. “Short-time Fourier transform” https://en.wikipedia.org/wiki/Short-time_Fourier_transform 

16. https://realsense.intel.com/stereo/ 


<a rel="license" href="http://creativecommons.org/licenses/by-nc-sa/4.0/"><img alt="Creative Commons License" style="border-width:0" src="https://i.creativecommons.org/l/by-nc-sa/4.0/88x31.png" /></a><br /><span xmlns:dct="http://purl.org/dc/terms/" property="dct:title">ALT</span> by <a xmlns:cc="http://creativecommons.org/ns#" href="https://www.linkedin.com/in/alexmisharin" property="cc:attributionName" rel="cc:attributionURL">Alexander Misharin, LVE Technologies LLC</a> is licensed under a <a rel="license" href="http://creativecommons.org/licenses/by-nc-sa/4.0/">Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License</a>.
