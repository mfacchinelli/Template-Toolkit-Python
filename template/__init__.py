import errno
import os
import sys
from template import base, service, util

class Template(base.Base):
  def __init__(self, config=None):
    if config is None:
      config = {}
    # prepare a namespace handler for any CONSTANTS definition
    # (later)
    self.SERVICE = service.Service(config)
    self.OUTPUT = config.get("OUTPUT") or sys.stdout
    self.OUTPUT_PATH = config.get("OUTPUT_PATH")

  def process(self, template, vars=None, outstream=None, **options):
    output = self.SERVICE.process(template, vars)
    if output is not None:
      outstream = outstream or self.OUTPUT
      if isinstance(outstream, str):
        if self.OUTPUT_PATH:
          outstream = os.path.join(self.OUTPUT_PATH, outstream)
      ref = util.Reference(output)
      error = _output(outstream, ref, options)
      if error:
        return self.error(error)
      return True
    else:
      return self.error(self.SERVICE.error())

  def context(self):
    return self.SERVICE.CONTEXT

  def service(self):
    return self.SERVICE


def _output(where, textref, options=None):
  error = None
  text  = textref.get()
  if callable(where):
    where(text)
  elif util.can(where, "write"):
    where.write(text)
  elif isinstance(where, util.Reference):
    where.set(str(where.get()) + text)
  elif isinstance(where, list):
    list.append(text)
  elif isinstance(where, str):
    dirname = os.path.dirname(where)
    try:
      os.makedirs(dirname)
    except OSError, e:
      if e.errno != errno.EEXIST:
        error = e
    if not error:
      mode = "w"
      if options.get("binmode"):
        mode += "b"
      try:
        fp = open(where, mode)
        fp.write(text)
        fp.close()
      except OSError, e:
        error = e
  else:
    error = "output_handler() cannot determine target type (%s)" % where
  return error
