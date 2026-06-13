#include <pybind11/pybind11.h>
#include <pybind11/numpy.h>
#include <pybind11/stl.h>
#include <vector>
#include <algorithm>
#include <limits>

namespace py = pybind11;
using namespace std;

double sum_total(const vector<int>& medoids, const vector<vector<double>>& dist) {
    int n = dist.size();
    double total_sum = 0;

    for (int i = 0; i < n; i++) {
        double best_dist = 100000; 

        for (int m : medoids) {
            if (dist[i][m] < best_dist) {
                best_dist = dist[i][m];
            }
        }
        total_sum += best_dist;
    }
    return total_sum;
}

vector<int> assign_clusters(const vector<vector<double>>& dist, const vector<int>& medoids) {
    int n = dist.size();
    int k = medoids.size();
    vector<int> cluster_assign(n);

    for (int i = 0; i < n; i++) {
        double min_dist = numeric_limits<double>::infinity();
        for (int j = 0; j < k; j++) {
            if (dist[i][medoids[j]] < min_dist) {
                cluster_assign[i] = medoids[j];
                min_dist = dist[i][medoids[j]];
            }
        }
    }
    return cluster_assign;
}

vector<int> run_clustering(vector<vector<double>> dist, vector<int> medoids) {
    int n = dist.size();
    int k = medoids.size();
    bool improvement = true;

    while (improvement) {
        improvement = false;
        double best_sum = sum_total(medoids, dist);

        for (int m = 0; m < k; m++) {
            for (int i = 0; i < n; i++) {
                vector<int> next_medoids = medoids;
                next_medoids[m] = i;

                double current_sum = sum_total(next_medoids, dist);

                if (current_sum < best_sum) {
                    medoids = next_medoids;
                    best_sum = current_sum;
                    improvement = true;
                }
            }
        }
    }
    return assign_clusters(dist, medoids);
}

PYBIND11_MODULE(cluster_module_cpp, m) {
    m.doc() = "K-Medoids clustering implementation using pybind11";
    m.def("run_clustering", &run_clustering, 
          "A function that optimizes medoids and returns cluster assignments",
          py::arg("dist"), py::arg("medoids"));
}