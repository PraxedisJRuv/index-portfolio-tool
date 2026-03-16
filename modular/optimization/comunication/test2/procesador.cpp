#include <pybind11/pybind11.h>
#include <pybind11/numpy.h>

namespace py = pybind11;

py::array_t<double> procesar(py::array_t<double> input) {

    auto buf = input.request();

    double* ptr = (double*) buf.ptr;

    int filas = buf.shape[0];
    int cols  = buf.shape[1];

    auto result = py::array_t<double>({filas, cols});
    auto buf_out = result.request();

    double* ptr_out = (double*) buf_out.ptr;

    for(int i=0;i<filas;i++){
        for(int j=0;j<cols;j++){

            int idx = i*cols + j;

            ptr_out[idx] = ptr[idx] * 2; // ejemplo
        }
    }

    return result;
}

PYBIND11_MODULE(misprocesador, m) {
    m.def("procesar", &procesar);
}