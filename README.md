# LAneDetection
 Detecting road lanes using openCV and Segementation

In the first python file, I'm trying to detect the lanes using open cv library by converting it to white and black detecting the edges with the lane area colored white.
Then I'm trying to get the region of interest by anding the result of the edge detection with a specific polygon colored white so I can get the desired region and rest of the image is black.
After that using the HoughLine function of opencv I'm trying to draw the lines (lanes) of the region I got ,averaving each side, Then draw the averaged line of the original image. 

After applying these steps on the input video, I took the frames generated and manually edited some of them to use them as training data to my next DeepLearning model.
In this model I used Unet architecture which is a sequence of downsampled layers followed by upsampled ones to preserve the lost features.
I trained the model on some of the input frames and kept the remaining for testing.
