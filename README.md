# thermal_cam

ONLY TESTED ON UBUNTU!

|my system:|
|----------|
|Ubuntu 20.04|
|ROS Foxy|
|kernel: 5.13.0-27-generic|
 
 
 
ROS 2 Lib for thermal cam infisense p2 with open cv and color-mapping

automatically searches all cv.Videocapture inputs and searches for an input with an resolution of 384px x 256px.
Publishes grey image (topic - Image: /thermal_stream) and heatmap (topic - Image: /thermal_colormap) with the cv2.COLORMAP_JET colormap.
