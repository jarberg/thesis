import decimal
import os
import sys
ROOT_DIR = os.path.dirname(os.path.abspath(__file__).split("utils")[0])

EPSILON = 0.00000000001
EPISLON_LEN = abs(decimal.Decimal(str(EPSILON)).as_tuple().exponent)

PI =3.14159265358979323846264338327950288419716939937510

