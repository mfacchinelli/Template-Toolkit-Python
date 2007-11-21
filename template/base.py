import re
import sys


class Base:
  """Base class for all core Template Toolkit classes.

  This class mainly provides Perl-style error-reporting semantics that
  are better accomplished in Python by simple exception-throwing.  It
  should therefore probably be removed in the near future, if possible.
  """
  def __init__(self):
    self.__error = None

  def error(self, *args):
    if args:
      self.__error = self.__ErrorMessage(args)
    else:
      return self.__error

  def DEBUG(self, *args):
    sys.stderr.write("DEBUG: ")
    for arg in args:
      sys.stderr.write(str(arg))

  @classmethod
  def Error(cls, *args):
    if args:
      cls.__ERROR = self.__ErrorMessage(args)
    else:
      try:
        return cls.__ERROR
      except AttributeError:
        return None

  @staticmethod
  def __ErrorMessage(args):
    if len(args) == 1:
      return args[0]
    else:
      return "".join(args)


class TemplateException(Exception):
  def __init__(self, type, info, buffer=None):
    Exception.__init__(self, type, info)
    self.__type = type
    self.__info = info
    self.__buffer = buffer

  def text(self, buffer=None):
    if buffer:
      if self.__buffer and self.__buffer is not buffer:
        buffer.reset(buffer.get() + self.__buffer.get())
      self.__buffer = buffer
      return ""
    elif self.__buffer:
      return self.__buffer.get()
    else:
      return ""

  def select_handler(self, options):
    type = str(self.__type)
    hlut = dict((str(option), True) for option in options)
    while type:
      if hlut.get(type):
        return type
      type = re.sub(r'\.?[^.]*$', '', type)
    return None

  def type(self):
    return self.__type

  def info(self):
    return self.__info

  def type_info(self):
    return self.__type, self.__info

  def __str__(self):
    return "%s error - %s" % (self.__type or "", self.__info)

  @classmethod
  def convert(cls, exception):
    if not isinstance(exception, TemplateException):
      exception = TemplateException(None, exception)
    return exception
