#include <Eigen/Dense>
using namespace Eigen;

VectorXd solve_markowitz(MatrixXd Sigma, VectorXd wb)
{
    int n = wb.size();

    MatrixXd KKT(n+1,n+1);
    KKT.setZero();

    KKT.block(0,0,n,n) = 2*Sigma;
    KKT.block(0,n,n,1) = VectorXd::Ones(n);
    KKT.block(n,0,1,n) = VectorXd::Ones(n).transpose();

    VectorXd rhs(n+1);
    rhs.head(n) = 2*Sigma*wb;
    rhs(n) = 1;

    VectorXd sol = KKT.colPivHouseholderQr().solve(rhs);

    return sol.head(n);
}