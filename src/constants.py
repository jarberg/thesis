import decimal
import os

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

EPSILON = 0.00000000001
EPISLON_LEN = abs(decimal.Decimal(str(EPSILON)).as_tuple().exponent)

PI =3.14159265358979323846264338327950288419716939937510

