//Esta es la mejor opción para algo exacto-rápido. EL problema es que es C++
//Y c++ no está tan bien integrado con pandas o otras herramientas necesarias
#include <iostream>
#include <vector>
#include <Eigen/Dense>
#include "osqp.h"

using namespace Eigen;
using namespace std;

VectorXd optimizar_portafolio(
        MatrixXd Sigma,
        VectorXd wb,
        VectorXd w0,
        double tau_max)
{

    int n = wb.size();
    int vars = 2*n;

    VectorXd q(vars);
    q.setZero();

    q.head(n) = -2 * Sigma * wb;

    MatrixXd P = MatrixXd::Zero(vars,vars);
    P.block(0,0,n,n) = 2 * Sigma;

    int m = 2*n + 2;

    MatrixXd A = MatrixXd::Zero(m, vars);
    VectorXd l(m);
    VectorXd u(m);

    int row=0;

    A.block(row,0,1,n) = VectorXd::Ones(n).transpose();
    l(row)=1;
    u(row)=1;
    row++;

    for(int i=0;i<n;i++){
        A(row,i)=1;
        l(row)=0;
        u(row)=OSQP_INFTY;
        row++;
    }

    for(int i=0;i<n;i++){
        A(row,i)=1;
        A(row,n+i)=-1;
        l(row)= -OSQP_INFTY;
        u(row)= w0(i);
        row++;
    }

    for(int i=0;i<n;i++){
        A(row,i)=-1;
        A(row,n+i)=-1;
        l(row)= -OSQP_INFTY;
        u(row)= -w0(i);
        row++;
    }

    A.block(row,n,1,n)=VectorXd::Ones(n).transpose();
    l(row)=-OSQP_INFTY;
    u(row)=tau_max;

    VectorXd w_opt = wb;

    return w_opt;
}

int main(){

    int n = 4;

    MatrixXd Sigma(n,n);
    Sigma <<
    0.1,0.02,0.01,0.03,
    0.02,0.2,0.04,0.01,
    0.01,0.04,0.15,0.02,
    0.03,0.01,0.02,0.1;

    VectorXd wb(n);
    wb << 0.25,0.25,0.25,0.25;

    VectorXd w0 = wb;

    double tau = 0.1;

    VectorXd w = optimizar_portafolio(Sigma,wb,w0,tau);

    cout<<"Pesos optimos:"<<endl;
    cout<<w<<endl;

}