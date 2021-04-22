#include <string>
#include <vector>
#include "opencv2/opencv.hpp"
using namespace cv;
#include <cstdio>
#include <thread>
#include <sys/stat.h>
#include <chrono>
using namespace std;

union pipe
{
    uint8_t image[1440] [1920] [3];
    uint8_t data [1440 * 1920 * 3];
} raw;


int main(){
    // Reads in the raw data
    //OPEN FILE PIPE1
    IPC_FIFO_NAME = "pipe1"
    fifo = fopen( IPC_FIFO_NAME , O_RDONLY );
    out << "hello from cpp";
    fread(&raw.image, 1, sizeof(raw.data), fifo);
    Mat image;
    // Rebuild raw data to cv::Mat
    image = Mat(1440, 1920, CV_8UC3, *raw.image);
    imshow("Janela Cpp", image);
    cv::waitKey(0);
    cout << "bye from cpp";
    fclose(fifo);
    return 0;
}