try:
    from benchmark_apis.hpobench.hpobench import HPOBench
except ModuleNotFoundError:
    pass

try:
    from benchmark_apis.hpolib.hpolib import HPOLib
except ModuleNotFoundError:
    pass

try:
    from benchmark_apis.jahs.jahs import JAHSBench201
except ModuleNotFoundError:
    pass

try:
    from benchmark_apis.lcbench.lcbench import LCBench
except ModuleNotFoundError:
    pass

try:
    from benchmark_apis.synthetic.branin import MFBranin
except ModuleNotFoundError:
    pass

try:
    from benchmark_apis.synthetic.hartmann import MFHartmann
except ModuleNotFoundError:
    pass


__version__ = "1.0.2"
__copyright__ = "Copyright (C) 2023 Shuhei Watanabe"
__licence__ = "Apache-2.0 License"
__author__ = "Shuhei Watanabe"
__author_email__ = "shuhei.watanabe.utokyo@gmail.com"
__url__ = "https://github.com/nabenabe0928/mfhpo-benchmark-api/"


__all__ = ["HPOBench", "HPOLib", "JAHSBench201", "LCBench", "MFBranin", "MFHartmann"]
