#include "opencv2\opencv.hpp"
using namespace cv;

#include <time.h>
#include <ctime>
#include <opencv2/aruco.hpp>



cv::Mat compute_marker(cv::Mat img) 
{
	cv::Mat threshImage;
	std::vector< std::vector< Point > > contours;
	cv::aruco::DetectorParameters* params = cv::aruco::DetectorParameters::create();
	adaptiveThreshold(img, threshImage, 255, ADAPTIVE_THRESH_GAUSSIAN_C, THRESH_BINARY, 5, 3);

	findContours(threshImage, contours, RETR_LIST, CHAIN_APPROX_NONE);

	for (unsigned int i = 0; i < contours.size(); i++) {
		std::vector< Point > approxCurve;
		approxPolyDP(contours[i], approxCurve, double(contours[i].size()) * params->polygonalApproxAccuracyRate, true);
		if (approxCurve.size() != 4 || !isContourConvex(approxCurve)) continue;

		if (contourArea(cv::Mat(contours[i])) > 80 and contourArea(cv::Mat(contours[i])) < 0.2 * img.cols * img.rows) {
			std::cout << "ENCONTREI \n";

		}

		}




		
	

	return threshImage;

}









void main()
{
	//VideoCapture cap(0);
	VideoCapture cap("D:/Desktop/Python/UAV_markers_test/New_Images/C_fast_short.MOV");
	cv::Mat img, img_original;
	cv::Size sz = img.size();
	int imageWidth = sz.width;
	int imageHeight = sz.height;
	int dim, width, height, scale_percent = 150;
	width = int(imageWidth * scale_percent / 100);
	height = int(imageHeight * scale_percent / 100);
	bool bSuccess;

	while (cap.read(img))
	{
		img_original = img;
		cvtColor(img, img, CV_BGR2GRAY);
		
		cv::resize(img, img, cv::Size(img.cols * 1.5, img.rows * 1.5), 0, 0, CV_INTER_LINEAR);
		
		img = compute_marker(img);

		cv::imshow("Window", img);

		if (waitKey(1) == 27)
		{
			std::cout << "Esc key is pressed by user. Stopping the video\n";
			break;
		}

	}

}
