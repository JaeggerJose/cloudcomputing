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

void execFigletslant(int i, int j) {
    //int style = 0;
    string style = "";
    
    style = "-f slant";
    string command = "figlet " + style + " " + to_string(i) + "x" + to_string(j) + " > " + to_string(i) + "*" + to_string(j) + "_slant.txt";
    system(command.c_str());
}

void execFigletslantbanner(int i, int j) {
    //int style = 0;
    string style = "";
    
    style = "-f banner";
    string command = "figlet " + style + " " + to_string(i) + "x" + to_string(j) + " > " + to_string(i) + "*" + to_string(j) + "_banner.txt";
    system(command.c_str());
}   

void execFigletstandard(int i, int j) {
    //int style = 0;
    string style = "";
    
    style = "-f standard";
    string command = "figlet " + style + " " + to_string(i) + "x" + to_string(j) + " > " + to_string(i) + "*" + to_string(j) + "_standard.txt";
    system(command.c_str());
}
void execFigletsmall(int i, int j) {
    string style = "";
    
    style = "-f small";
    string command = "figlet " + style + " " + to_string(i) + "x" + to_string(j) + " > " + to_string(i) + "*" + to_string(j) + "_small.txt";
    system(command.c_str());
}
int main() {
    int times = 100;
    for(int i=0; i<times; i++) {
        for(int j=0; j<times; j++) {
            execFigletslant(i, j);
            execFigletslantbanner(i, j);
            execFigletstandard(i, j);
            execFigletsmall(i, j);
        }
    }

}