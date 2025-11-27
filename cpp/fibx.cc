#include <pybind11/pybind11.h>

int fib(int n) {
    if (n < 2) return n;
    return fib(n - 1) + fib(n - 2);
}

namespace py = pybind11;

PYBIND11_MODULE(fib_module, m) {
    m.def("fib", &fib, "Compute Fibonacci in C++");
}
