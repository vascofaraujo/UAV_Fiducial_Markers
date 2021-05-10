#include <iostream>
#include <unistd.h>
#include <fcntl.h>
#include <vector>
#include <sys/stat.h> 

using namespace std;

int main(){

int pipefile;



//std::string s = "loooool";

//std::vector<char> bytes(s.begin(), s.end());
//bytes.push_back('\n');
//bytes.push_back('\0');
//char *c = &bytes[0];

std::cout << "Opening c++ program " << std::endl;

float distancia = 10.249;

std::string dist_str = to_string(distancia);
std::vector<char> dist_bytes(dist_str.begin(), dist_str.end());
dist_bytes.push_back('\n');
//dist_bytes.push_back('\0');
char *ptr = &dist_bytes[0];




if ((pipefile = open("myfifo", O_WRONLY)) < 0) {
  perror("open");
  exit(-1);
}

std::cout << "c++ opened the pipe" << std::endl;


size_t written; //= write(pipefile, c, sizeof(char)*7);


written = write(pipefile, ptr, sizeof(dist_bytes));


for (int i = 0; i < 10; i++)
{
	//i--;
	distancia++;
	std::cout << "distancia in loop c++ =" << distancia << endl;
	std::string dist_str = to_string(distancia);
	std::vector<char> dist_bytes(dist_str.begin(), dist_str.end());
	dist_bytes.push_back('\n');
	dist_bytes.push_back('\0');
	char *ptr = &dist_bytes[0];
	std::cout << sizeof(dist_bytes) << endl;
	write(pipefile, ptr, sizeof(dist_bytes));
}

//written = write(pipefile, c2, sizeof(float));

// fechar a entrada do fifo
if (close(pipefile) < 0) {
  perror("close");
  exit(-1);
}
return 0;

}