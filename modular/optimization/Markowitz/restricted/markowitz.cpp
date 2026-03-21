#include <pybind11/pybind11.h>
#include <pybind11/numpy.h>
#include <Eigen/Dense>
#include <algorithm>

namespace py = pybind11;
using namespace Eigen;
using namespace std;

// Proyección al simplex
VectorXd project_simplex(VectorXd v)
{
    int n = v.size();
    VectorXd u = v;
    sort(u.data(), u.data() + n, greater<double>());

    double cssv = 0;
    int rho = 0;

    for(int i = 0; i < n; i++){
        cssv += u(i);
        double t = (cssv - 1)/(i+1);
        if(u(i)-t > 0)
            rho = i;
    }

    double theta = (u.head(rho+1).sum() - 1)/(rho+1);
    VectorXd w = (v.array() - theta).max(0);
    return w;
}

//Optimización PG con turnover
VectorXd optimize_pg_turnover(
        MatrixXd Sigma,
        VectorXd wb,
        VectorXd w_prev,
        double lambda,
        int max_iter = 1000,
        double alpha = 0.01)
{
    int n = wb.size();
    VectorXd w = wb;

    for(int k = 0; k < max_iter; k++){
        // gradiente: tracking error + turnover penalty
        VectorXd grad = 2*Sigma*(w - wb) + lambda*(w - w_prev).array().sign().matrix();

        // paso de descenso
        w = w - alpha*grad;

        // proyectar al simplex
        w = project_simplex(w);
    }

    return w;
}

// --- wrapper pybind11 ---
py::array_t<double> optimize_portfolio(
        py::array_t<double> Sigma_np,
        py::array_t<double> wb_np,
        py::array_t<double> w_prev_np,
        double lambda)
{
    auto Sigma_buf = Sigma_np.request();
    auto wb_buf = wb_np.request();
    auto w_prev_buf = w_prev_np.request();

    int n = wb_buf.shape[0];

    double* Sigma_ptr = (double*) Sigma_buf.ptr;
    double* wb_ptr = (double*) wb_buf.ptr;
    double* w_prev_ptr = (double*) w_prev_buf.ptr;

    Map<MatrixXd> Sigma(Sigma_ptr, n, n);
    Map<VectorXd> wb(wb_ptr, n);
    Map<VectorXd> w_prev(w_prev_ptr, n);

    VectorXd w = optimize_pg_turnover(Sigma, wb, w_prev, lambda);

    py::array_t<double> result(n);
    auto r = result.mutable_unchecked<1>();
    for(int i=0; i<n; i++)
        r(i) = w(i);

    return result;
}

PYBIND11_MODULE(markowitz_cpp, m)
{
    m.def("optimize_portfolio", &optimize_portfolio,
          "Optimize portfolio minimizing variance tracking error with turnover penalty");
}