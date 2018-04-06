#include "opencv2/imgproc/imgproc.hpp"
#include "opencv2/highgui/highgui.hpp"
#include <iostream>
 
 // Author Rishab Shah

using namespace cv;
 
int main( int argc, char** argv )
{
   Mat src, gray, dst;

  // Load an image
  src = imread( argv[1], 1 );
 
  // Convert the image to Gray
  cvtColor( src, gray, CV_RGB2GRAY );
 
  namedWindow("Input Image", CV_WINDOW_AUTOSIZE );
  imshow("Input Image", src);

  /* 0: Binary,      1: Binary Inverted,      2: Threshold Truncated,      3: Threshold to Zero,      4: Threshold to Zero Inverted    */
  int threshold_type = 2;    // slider 1 [0, 4]
  int threshold_value = 128;  // slider 2 [0 255]

    threshold(gray, dst, threshold_value, 255, threshold_type );
    imshow("Thresholded Image", dst );
    
         int current_threshold = 128;
        int max_threshold = 255;
	
	//Binary Threshold
	Mat thresholded;
	threshold(gray, thresholded, current_threshold, max_threshold, THRESH_BINARY);
	imshow("Binary threshold",thresholded);	

	// Band thresholding
	Mat binary_image1,binary_image2,band_thresholded_image;
	int threshold1 = 27, threshold2 = 125;
	threshold(gray, binary_image1, threshold1, max_threshold, THRESH_BINARY);
	threshold(gray, binary_image2, threshold2, max_threshold, THRESH_BINARY_INV);
	bitwise_and( binary_image1, binary_image2, band_thresholded_image );
        imshow("Band Thresholding", band_thresholded_image);

	// Semi thresholding
	Mat semi_thresholded_image;
	threshold(gray, semi_thresholded_image, current_threshold, max_threshold, THRESH_BINARY_INV | THRESH_OTSU);
	bitwise_and( gray, semi_thresholded_image, semi_thresholded_image );
        imshow("Semi Thresholding", semi_thresholded_image);

	// Adaptive thresholding
	Mat adaptive_thresh;
	adaptiveThreshold(gray, adaptive_thresh, 255.0, ADAPTIVE_THRESH_GAUSSIAN_C, THRESH_BINARY, 101, 10 );
	imshow("Adaptive Thresholding", adaptive_thresh);

  waitKey( 0 );
}