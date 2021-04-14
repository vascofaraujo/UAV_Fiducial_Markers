#include <iostream>
#include <fstream>
#include <string>
#include <vector>
#include "opencv2/opencv.hpp"
using namespace cv;
#include <cstdio>
#include <thread>

#include <sys/stat.h>
#include <chrono>
using namespace std;
/*
int main() {

    //Open image file to read from
    char imgPath[] = "./AR6.jpeg";
    ifstream fileImg(imgPath, ios::binary);
    fileImg.seekg(0, std::ios::end);
    int bufferLength = fileImg.tellg();
    fileImg.seekg(0, std::ios::beg);

    if (fileImg.fail())
    {
        cout << "Failed to read image" << endl;
        cin.get();
        return -1;
    }

    //Read image data into char array
    char *buffer = new char[bufferLength];
    fileImg.read(buffer, bufferLength);

    //Decode data into Mat 
    cv::Mat matImg;
    matImg = cv::imdecode(cv::Mat(1, bufferLength, CV_8UC1, buffer), cv::IMREAD_UNCHANGED);

    //Create Window and display it
    if (!(matImg.empty()))
    {
        imshow("Image from Char Array", matImg);
    }
    cv::waitKey(0);

    delete[] buffer;

    return 0;
}
*/
int main(int argc, char *argv[]) {
    cout << "Heloooooooooooooooo";
    const char *fifo_name = "fifo";
    std::ifstream f;
    for(;;) { // Wait till the named pipe is available.
        f.open(fifo_name, std::ios_base::in);
        if(f.is_open())
            break;
        std::this_thread::sleep_for(std::chrono::seconds(3));
    }
    /*ifstream f(fifo_name);*/
    string line;
    getline(f, line);
    auto data_size = stoi(line);

    char *buf = new char[data_size];
    f.read(buf, data_size);
    Mat matimg;
    //cout << Mat(data);
    matimg = imdecode(Mat(1, data_size, CV_8UC1, buf), IMREAD_UNCHANGED);
    cout << buf;

     if (!(matimg.empty()))
    {
        imshow("display", matimg);
    }
    waitKey(0);
    delete[] buf;

    return 0;
}
