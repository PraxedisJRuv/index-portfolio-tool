#include <pybind11/pybind11.h>
#include <pybind11/numpy.h>

#include <Eigen/Dense>
#include <algorithm>

namespace py = pybind11;
using namespace Eigen;
using namespace std;

VectorXd project_simplex(VectorXd v)
{
    int n = v.size();

    VectorXd u = v;
    sort(u.data(), u.data()+n, greater<double>());

    double cssv = 0;
    int rho = 0;

    for(int i=0;i<n;i++){
        cssv += u(i);
        double t = (cssv-1)/(i+1);

        if(u(i)-t > 0)
            rho = i;
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


py::array_t<double> optimize_portfolio(
        py::array_t<double> Sigma_np,
        py::array_t<double> wb_np)
{
    auto Sigma_buf = Sigma_np.request();
    auto wb_buf = wb_np.request();

    int n = wb_buf.shape[0];

    double* Sigma_ptr = (double*) Sigma_buf.ptr;
    double* wb_ptr = (double*) wb_buf.ptr;

    Map<MatrixXd> Sigma(Sigma_ptr, n, n);
    Map<VectorXd> wb(wb_ptr, n);

    VectorXd w = optimize_pg(Sigma, wb);

    py::array_t<double> result(n);
    auto r = result.mutable_unchecked<1>();

    for(int i=0;i<n;i++)
        r(i) = w(i);

    return result;
}

PYBIND11_MODULE(markowitz_cpp, m)
{
    m.def("optimize_portfolio", &optimize_portfolio);
}