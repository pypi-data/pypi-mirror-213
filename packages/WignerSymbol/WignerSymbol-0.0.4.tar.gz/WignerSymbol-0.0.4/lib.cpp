#include <pybind11/pybind11.h>
#include "WignerSymbol/WignerSymbol.hpp"

#define STRINGIFY(x) #x
#define MACRO_STRINGIFY(x) STRINGIFY(x)

namespace py = pybind11;
using namespace util;

static WignerSymbols wigner;

inline void wigner_init(int num, std::string type, int rank)
{
    wigner.reserve(num, type, rank);
}

inline double trunc_binomial(int n, int k)
{
    return wigner.binomial(n, k);
}

inline double CG(int dj1, int dj2, int dj3, int dm1, int dm2, int dm3)
{
    return wigner.CG(dj1, dj2, dj3, dm1, dm2, dm3);
}

inline double CG0(int j1, int j2, int j3)
{
    return wigner.CG0(j1, j2, j3);
}

inline double wigner_3j(int dj1, int dj2, int dj3, int dm1, int dm2, int dm3)
{
    return wigner.f3j(dj1, dj2, dj3, dm1, dm2, dm3);
}

inline double wigner_6j(int dj1, int dj2, int dj3, int dj4, int dj5, int dj6)
{
    return wigner.f6j(dj1, dj2, dj3, dj4, dj5, dj6);
}

inline double Racah(int dj1, int dj2, int dj3, int dj4, int dj5, int dj6)
{
    return wigner.Racah(dj1, dj2, dj3, dj4, dj5, dj6);
}

inline double wigner_9j(int dj1, int dj2, int dj3, int dj4, int dj5, int dj6, int dj7, int dj8, int dj9)
{
    return wigner.f9j(dj1, dj2, dj3, dj4, dj5, dj6, dj7, dj8, dj9);
}

inline double dfunc(int dj, int dm1, int dm2, double beta)
{
    return wigner.dfunc(dj, dm1, dm2, beta);
}

inline double Moshinsky(int N, int L, int n, int l, int n1, int l1, int n2, int l2, int lambda, double tan_beta)
{
    return wigner.Moshinsky(N, L, n, l, n1, l1, n2, l2, lambda, tan_beta);
}

using namespace pybind11::literals;

PYBIND11_MODULE(WignerSymbol, m){
    m.doc() = "A fast library to evaluate Winger-Symbols.";
    py::class_<WignerSymbols>(m, "WignerSymbols")
        .def(py::init<>())
        .def("reserve", &WignerSymbols::reserve, "nmax"_a, "type"_a, "rank"_a)
        .def("CG", &WignerSymbols::CG, "dj1"_a, "dj2"_a, "dj3"_a, "dm1"_a, "dm2"_a, "dm3"_a)
        .def("CG0", &WignerSymbols::CG0, "dj1"_a, "dj2"_a, "dj3"_a)
        .def("f3j", &WignerSymbols::f3j, "dj1"_a, "dj2"_a, "dj3"_a, "dm1"_a, "dm2"_a, "dm3"_a)
        .def("f6j", &WignerSymbols::f6j, "dj1"_a, "dj2"_a, "dj3"_a, "dj4"_a, "dj5"_a, "dj6"_a)
        .def("f9j", &WignerSymbols::f9j, "dj1"_a, "dj2"_a, "dj3"_a, "dj4"_a, "dj5"_a, "dj6"_a, "dj7"_a, "dj8"_a, "dj9"_a)
        .def("dfunc", &WignerSymbols::dfunc, "dj"_a, "dm1"_a, "dm2"_a, "beta"_a)
        .def("Moshinsky", &WignerSymbols::Moshinsky, "Nc"_a, "Lc"_a, "nr"_a, "lr"_a, "n1"_a, "l1"_a, "n2"_a, "l2"_a, "lambda"_a, "tan_beta"_a);
    m.attr("_wigner") = wigner;
    m.def("init", &wigner_init, "init binomial table", "nmax"_a, "type"_a, "rank"_a);
    m.def("CG", &CG, "dj1"_a, "dj2"_a, "dj3"_a, "dm1"_a, "dm2"_a, "dm3"_a);
    m.def("CG0", &CG0, "dj1"_a, "dj2"_a, "dj3"_a);
    m.def("f3j", &wigner_3j, "dj1"_a, "dj2"_a, "dj3"_a, "dm1"_a, "dm2"_a, "dm3"_a);
    m.def("f6j", &wigner_6j, "dj1"_a, "dj2"_a, "dj3"_a, "dj4"_a, "dj5"_a, "dj6"_a);
    m.def("f9j", &wigner_9j, "dj1"_a, "dj2"_a, "dj3"_a, "dj4"_a, "dj5"_a, "dj6"_a, "dj7"_a, "dj8"_a, "dj9"_a);
    m.def("dfunc", &dfunc, "dj"_a, "dm1"_a, "dm2"_a, "beta"_a);
    m.def("Moshinsky", &Moshinsky, "Nc"_a, "Lc"_a, "nr"_a, "lr"_a, "n1"_a, "l1"_a, "n2"_a, "l2"_a, "lambda"_a, "tan_beta"_a);
#ifdef VERSION
    m.attr("__version__") = MACRO_STRINGIFY(VERSION);
#else
    m.attr("__version__") = "dev";
#endif
}