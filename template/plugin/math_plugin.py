import math
import random
import re

from template.plugin import Plugin
from template.util import numify


OCT_REGEX = re.compile(r'^\s*(0[xb]?)?')

OCT_DIGITS = {
  '0b': (2, re.compile(r'[01]*')),
  '0': (8, re.compile(r'[0-7]*')),
  None: (8, re.compile(r'[0-7]*')),
  '0x': (16, re.compile(r'[0-9A-Fa-f]*')),
}

# Our global random number object:
Random = random.Random()

# A casual search finds no obvious Python counterpart to Perl's
# Math::TrulyRandom module.  If you have one, set the following global
# variable to the function you want.
TrulyRandomFunction = None


# A trivial local error class.
class Error(Exception):
  pass


class Math(Plugin):
  def __init__(self, context, config=None):
    Plugin.__init__(self)
    self.__config = config  # unused

  def abs(self, x):
    # The built-in abs always returns a float, which is here cast back to
    # the type of the input argument, so that (for example) the absolute
    # value of an int is returned as an int.
    return type(x)(abs(numify(x)))

  def atan2(self, x, y):
    return math.atan2(numify(x), numify(y))

  def cos(self, x):
    return math.cos(numify(x))

  def exp(self, x):
    return math.exp(numify(x))

  def hex(self, x):
    return int(str(numify(x)), 16)

  def int(self, x):
    return int(numify(x))

  def log(self, x):
    return math.log(numify(x))

  def oct(self, x):
    x = str(x)
    match = OCT_REGEX.match(x)
    base, regex = OCT_DIGITS[match.group(1)]
    digits = regex.match(x[len(match.group()):]).group()
    if len(digits) == 0:
      return 0
    else:
      return int(digits, base)

  def rand(self, x):
    return Random.uniform(0, numify(x))

  def sin(self, x):
    return math.sin(numify(x))

  def sqrt(self, x):
    root = math.sqrt(numify(x))
    trunc = long(root)
    # Try to return an integer, if possible:
    if root == trunc:
      return trunc
    else:
      return root

  def srand(self, x):
    return Random.seed(numify(x))

  def truly_random(self, x):
    if TrulyRandomFunction is None:
      raise Error("No truly_random dispatch function has been defined")
    return TrulyRandomFunction(numify(x))

  def pi(self):
    return math.pi

  def tan(self, x):
    return math.tan(numify(x))

  def csc(self, x):
    return 1.0 / math.sin(numify(x))

  cosec = csc

  def sec(self, x):
    return 1.0 / math.cos(numify(x))

  def cot(self, x):
    return 1.0 / math.tan(numify(x))

  cotan = cot

  def asin(self, x):
    return math.asin(numify(x))

  def acos(self, x):
    return math.acos(numify(x))

  def atan(self, x):
    return math.atan(numify(x))

  def acsc(x):
    return math.pi / 2.0 - self.asec(x)

  acosec = acsc

  def asec(self, x):
    return math.acos(1.0 / numify(x))

  def acot(self, x):
    return math.pi / 2.0 - math.atan(numify(x))

  acotan = acot

  def sinh(self, x):
    return math.sinh(numify(x))

  def cosh(self, x):
    return math.cosh(numify(x))

  def tanh(self, x):
    return math.tanh(numify(x))

  def csch(self, x):
    return 1.0 / math.sinh(numify(x))

  cosech = csch

  def sech(self, x):
    return 1.0 / math.cosh(numify(x))

  def coth(self, x):
    return 1.0 / math.tanh(numify(x))

  cotanh = coth

  def asinh(self, x):
    x = numify(x)
    return math.log(x + math.sqrt(x*x + 1))

  def acosh(self, x):
    pass  # Not sure what to do here...

  def atanh(self, x):
    x = numify(x)
    return math.log((1.0 + x) / (1.0 - x)) / 2.0

  def acsch(self, x):
    x = numify(x)
    if x < 0:
      return math.log((1.0 - math.sqrt(1.0 + x * x)) / x)
    else:
      return math.log((1.0 + math.sqrt(1.0 + x * x)) / x)

  acosech = acsch

  def asech(self, x):
    pass  # Not sure what to do here either...

  def acoth(self, x):
    x = numify(x)
    return math.log((1.0 + x) / (1.0 - x)) / 2.0

  acotanh = acoth

  def rad2deg(self, x):
    return math.degrees(numify(x))

  def rad2grad(self, x):
    return math.degrees(numify(x)) * 10.0 / 9.0

  def deg2rad(self, x):
    return math.radians(numify(x))

  def deg2grad(self, x):
    return numify(x) * 10.0 / 9.0

  def grad2rad(self, x):
    return math.radians(numify(x) * 0.9)

  def grad2deg(self, x):
    return numify(x) * 0.9
