## Amplification function of the additional light texture. 

Application of the [additional light texture](/README.md) can greatly increase illumination contrast in the scene observed by a video camera, 
especially in low ambient light environment such as the one typically present during nighttime. 
As we demonstrate below, the additional light texture can play the role of an amplification medium 
for small body movements and its application to a person's body can lead to orders of magnitude increase in the ALT data components 
related to the heart activity and/or respiration of the person compared to the case when there is no additional light texture present 
(e.g. when the ALT-generating light element is switched off) during the otherwise equivalent data collection and data processing procedures. 

![amplification function of the ALT](/figures/research/amplification-A-C.png)

To demonstrate the amplification function of the additional light texture, [ALT data collection](/code/simple-ALT-raw.py) was performed during daytime 
using the ALT system in which the light source element is the infrared light emitter of a Microsoft Kinect for Xbox 360 system, 
the computing element is a Raspberry Pi single-board computer, and the video camera element is a Pi NoIR camera connected to the Raspberry Pi single-board computer. 
Data in Figures A-C above were collected with the Pi NoIR camera running at 90 frames per second rate. 
The video frame size was set to 640x480 pixels. A person was at approximately 1.3 meters (4.3 feet) distance from the Pi NoIR camera. 
The camera observed about 1/2 of the person's body. 

Figures A and B show frequency spectra which were obtained via fast Fourier transformation of two different [sSAD values data sets](/code/simple-ALT-raw.py). 
The sSAD values data sets used to obtain spectra shown in Figures A and B had the same length and corresponded to one minute data collection time. 
These data sets were collected under the same ambient lighting conditions in the room (the ones excluding the additional illumination created by a light source element of an ALT system). 
The light emitter of the Microsoft Kinect for Xbox 360 unit was active (switched ON) during collection of the sSAD data set corresponding to Figure A, 
and the light emitter was inactive (switched OFF) during collection of the sSAD data set corresponding to Figure B. 
Note that the vertical scales of the plots in Figures A and B are the same. 

Figure C shows the same data as Figure B, yet the maximum value of the vertical axis in Figure C 
is one hundred times smaller compared to the maximum values of the vertical axes of the plots in Figures A and B 
(2.0E+11 for the plot in Figure C vs. 2.0E+13 for the plots in Figures A and B). 
Therefore, the frequency components Fr and Fh corresponding to respiration and heartbeats of a person, respectively, in the spectrum shown in Figure A are at least one hundred times larger 
compared to the frequency components in the same regions of the frequency spectra shown in Figures B and C. 
Horizontal axis numbers of the plots in Figures A, B, and C correspond to the frequency bin numbers of the FFT. 

Therefore, the data shown in Figures A, B, and C demonstrate that application of the additional light texture leads (under the conditions described above) 
to at least two orders of magnitude amplification of the frequency components corresponding to a person’s respiration and pulse in the frequency spectra 
compared to the case when there is no additional light texture present. 

Note also that both the respiration rate and the heart rate were determined from the same sSAD data. 


<a rel="license" href="http://creativecommons.org/licenses/by-nc-sa/4.0/"><img alt="Creative Commons License" style="border-width:0" src="https://i.creativecommons.org/l/by-nc-sa/4.0/88x31.png" /></a><br /><span xmlns:dct="http://purl.org/dc/terms/" property="dct:title">ALT</span> by <a xmlns:cc="http://creativecommons.org/ns#" href="https://www.linkedin.com/in/alexmisharin" property="cc:attributionName" rel="cc:attributionURL">Alexander Misharin, LVE Technologies LLC</a> is licensed under a <a rel="license" href="http://creativecommons.org/licenses/by-nc-sa/4.0/">Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License</a>. The full text of the CC BY-NC-SA 4.0 license can be found at [https://creativecommons.org/licenses/by-nc-sa/4.0/legalcode](https://creativecommons.org/licenses/by-nc-sa/4.0/legalcode). Contact [LVE Technologies LLC](https://lvetechnologies.com/) if you would like to obtain a commercial license: info(at)lvetechnologies.com 
