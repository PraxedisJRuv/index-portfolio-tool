#include <Eigen/Dense>
using namespace Eigen;
VectorXd project_simplex(VectorXd v)
{
    int n = v.size();

    VectorXd u = v;
    sort(u.data(), u.data()+n, greater<double>());

    double cssv=0;
    int rho=0;

    for(int i=0;i<n;i++){
        cssv += u(i);
        double t = (cssv-1)/(i+1);

        if(u(i)-t>0)
            rho=i;
    }

    double theta = (u.head(rho+1).sum()-1)/(rho+1);

    VectorXd w = (v.array()-theta).max(0);

    return w;
}

VectorXd optimize_pg(MatrixXd Sigma, VectorXd wb)
{
    int n = wb.size();

    VectorXd w = wb;

    double alpha = 0.01;

    for(int k=0;k<1000;k++){

        VectorXd grad = 2*Sigma*(w-wb);

        w = w - alpha*grad;

        w = project_simplex(w);
    }

    return w;
}