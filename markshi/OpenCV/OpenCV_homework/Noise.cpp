#include "opencv2/core/core.hpp"
#include "opencv2/highgui/highgui.hpp"
#include "opencv2/imgproc/imgproc.hpp"
#include "iostream"
 
 // Author Rishab Shah

using namespace cv;
using namespace std;

void Add_salt_pepper_Noise(Mat &srcArr, float pa, float pb );
void Add_gaussian_Noise(Mat &srcArr,double mean,double sigma);
 
int main(int argc, char** argv )
{
    Mat image;
    image = imread(argv[1], 0);
    namedWindow( "Original image", CV_WINDOW_AUTOSIZE );
    imshow( "Original image", image);

    Mat noise_img = image.clone(); 
    float mean = 0;			
    float sigma = 50;		//Not the variance
    Add_gaussian_Noise(noise_img, mean, sigma);
    imshow( "Gaussian Noise", noise_img);

    Mat noise_dst = noise_img.clone();
    blur(noise_dst,noise_dst,Size(3,3));
    imshow( "Box filter", noise_dst);

    Mat noise_dst1 = noise_img.clone();
    GaussianBlur(noise_dst1, noise_dst1, Size(3,3),1.5);
    imshow( "Gaussian filter", noise_dst1);
    
    Mat noise_dst2 = noise_img.clone();
    medianBlur(noise_dst2,noise_dst2,3);
    imshow( "Median filter", noise_dst2);
    
    Mat noise_img2 = image.clone(); 
    float pa=0.01;			//Controls the amount of black spots in the noise
    float pb=0.01;			//Controls the amount of white spots in the noise
    Add_salt_pepper_Noise(noise_img2, pa, pb); 
    imshow( "Salt and Pepper Noise", noise_img2);

    Mat noise_dst3 = noise_img2.clone();
    blur(noise_dst3,noise_dst3,Size(3,3));
    imshow( "Box filter", noise_dst3);

    Mat noise_dst4 = noise_img2.clone();
    GaussianBlur(noise_dst4,noise_dst4,Size(3,3),1.5);
    imshow( "Gaussian filter", noise_dst4);
    
    Mat noise_dst5 = noise_img2.clone();
    medianBlur(noise_dst5,noise_dst5,3);
    imshow( "Median filter", noise_dst5);
    return 0;
}

void Add_salt_pepper_Noise(Mat &srcArr, float pa, float pb )

{    RNG rng; // rand number generate
    int amount1=srcArr.rows*srcArr.cols*pa; //Need to run through all channels
    int amount2=srcArr.rows*srcArr.cols*pb;
    for(int counter=0; counter<amount1; ++counter)
    {
     srcArr.at<uchar>(rng.uniform( 0,srcArr.rows), rng.uniform(0, srcArr.cols)) =0;

    }
     for (int counter=0; counter<amount2; ++counter)
     {
     srcArr.at<uchar>(rng.uniform(0,srcArr.rows), rng.uniform(0,srcArr.cols)) = 255;
     }
}


void Add_gaussian_Noise(Mat &srcArr,double mean,double sigma)
{
    Mat NoiseArr = srcArr.clone();
    RNG rng;
    rng.fill(NoiseArr, RNG::NORMAL, mean,sigma);  
    add(srcArr, NoiseArr, srcArr);   
}