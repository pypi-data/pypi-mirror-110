#include <pybind11/pybind11.h>
namespace py = pybind11;

char *run(const char *data, const char *outputType, double _lambda, float _hI0,
          int _chargePrecision, const char *_method, int _mR, int _mK,
          double _eta, const char *ionizationDataFilename,
          const char *chargeCentersFilename);

PYBIND11_MODULE(pyeqeq_eqeq, mod)
{
    mod.def("run", &run, pybind11::return_value_policy::reference);
}
