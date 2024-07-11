#include <iostream>
#include <string>
#include <vector>
#include <algorithm>
#include <fstream>
#include <sstream>
#include <iomanip>
#include <random>
using namespace std;

// set the seed for the random number generator

void execFiglet(int i, int j) {
    //int style = 0;
    string style = "";
    
    style = "-f banner";
    // style = "-f slant";
    style = "-f standard";
    
    string command = "figlet " + style + " " + to_string(i) + "*" + to_string(j) + " > " + to_string(i) + "*" + to_string(j) + "_standard" + ".txt";
    system(command.c_str());
}
int main() {
    int times = 100;
    for(int i=0; i<times; i++) {
        for(int j=0; j<times; j++) {
            execFiglet(i, j);
        }
    }

}