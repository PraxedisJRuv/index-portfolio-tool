#include <pybind11/pybind11.h>
#include <pybind11/numpy.h>
#include <pybind11/stl.h>

#include <vector>
#include <limits>
#include <algorithm>

namespace py = pybind11;
using namespace std;

double sum_total(
    const vector<int>& medoids,
    const double* dist,
    int n)
{
    double sum = 0.0;

    for(int i = 0; i < n; i++){
        double best = numeric_limits<double>::max();

        for(int m : medoids){
            double d = dist[i*n + m];
            best = min(best, d);
        }

        sum += best;
    }

    return sum;
}

vector<int> run_kmedoids(
    py::array_t<double, py::array::c_style | py::array::forcecast> dist_np,
    vector<int> medoids)
{
    auto buf = dist_np.request();

    int n = buf.shape[0];
    double* dist = static_cast<double*>(buf.ptr);

    int k = medoids.size();
    bool mejora = true;

    while(mejora){

        mejora = false;
        double bestsum = sum_total(medoids, dist, n);

        for(int m = 0; m < k; m++){
            for(int i = 0; i < n; i++){

                vector<int> nuevo = medoids;
                nuevo[m] = i;

                double c = sum_total(nuevo, dist, n);

                if(c < bestsum){
                    medoids = nuevo;
                    bestsum = c;
                    mejora = true;
                }
            }
        }
    }

    return medoids;
}

PYBIND11_MODULE(kmedoids_cpp, m) {
    m.def("run_kmedoids", &run_kmedoids);
}