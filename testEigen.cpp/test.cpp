#include <Eigen/Dense>
#include <iostream>

using namespace Eigen;

int main(){
    MatrixXd A = MatrixXd::Random(3,3);
    std::cout << A << std::endl;
}