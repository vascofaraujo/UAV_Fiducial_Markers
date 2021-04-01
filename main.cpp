#include "opencv2\opencv.hpp"
using namespace cv;

#include <time.h>
#include <ctime>
#include <opencv2/aruco.hpp>



cv::Mat compute_marker(cv::Mat img) 
{
	cv::Mat threshImage; 
	std::vector<std::vector<cv::Point> > contours;
	double cnt_len;
	cv::aruco::DetectorParameters* params = cv::aruco::DetectorParameters::create();
	adaptiveThreshold(img, threshImage, 255, ADAPTIVE_THRESH_GAUSSIAN_C, THRESH_BINARY, 5, 3);

	findContours(threshImage, contours, RETR_LIST, CHAIN_APPROX_NONE);
	Mat drawing = Mat::zeros(img.size(), CV_8UC3);

	
	//for (size_t i = 0; i < contours.size(); i++)
	//{
		//std::cout << contours[i] << "print \n";
		//std::cout << "print \n";
		
	//}


	for (unsigned int i = 0; i < contours.size(); i++) {
		std::vector< Point > approxCurve;
		cnt_len = arcLength(contours[i], true);
		
		//if (approxCurve.size() != 4 || !isContourConvex(approxCurve)) continue;
		//std::cout << "ENCONTREI CONVEX E 4 LADOS \n";
		//std::cout << "SIZE:" << contours[i].size() << "\n";
		//if (approxCurve.size() == 4 && isContourConvex(approxCurve)) {
			
			//std::cout << "SIZE2:" << cnt_len << "\n";
			//std::cout << contourArea(contours[i]) << "\n";
			//std::cout << "COL:" << img.cols << "ROWS" << img.rows << "\n";
			if (contourArea(contours[i]) > 80 && contourArea(contours[i]) < 0.2 * img.cols * img.rows) {
				//approxPolyDP(contours[i], approxCurve, double(cnt_len * params->polygonalApproxAccuracyRate), true);
				//std::cout << "SIZE2:" << params->polygonalApproxAccuracyRate << "\n";
				approxPolyDP(contours[i], approxCurve, double(contours[i].size()) * 0.03, true);
				if (approxCurve.size() == 4 && isContourConvex(approxCurve)) {
					drawContours(drawing, contours, (int)i, (255, 255, 255), 2, LINE_8);
				}
				std::cout << approxCurve << "ENCONTREI \n";

			}
		}
		//}

	cv::imshow("Drawing", drawing);
	waitKey(0);




		
	

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
