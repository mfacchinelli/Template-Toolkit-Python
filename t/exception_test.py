from template import base, test, util


class ExceptionTest(test.TestCase):
  def testException(self):
    text = "the current output buffer"
    e1 = base.Exception("e1.type", "e1.info")
    e2 = base.Exception("e2.type", "e2.info", util.Reference(text))
    self.assertEquals("e1.type", e1.type())
    self.assertEquals("e2.info", e2.info())
    ti = e1.type_info()
    self.assertEquals("e1.type", ti[0])
    self.assertEquals("e1.info", ti[1])
    self.assertEquals("e2.type error - e2.info", str(e2))
    self.assertEquals("the current output buffer", e2.text())
    prepend = "text to prepend "
    e2.text(util.Reference(prepend))
    self.assertEquals("text to prepend the current output buffer", e2.text())
    handlers = ("something", "e2", "e1.type")
    self.assertEquals("e1.type", e1.select_handler(*handlers))
    self.assertEquals("e2", e2.select_handler(*handlers))
    e3 = base.Exception("e3.type", "e3.info", None)
    self.assertEquals("", e3.text())
    self.assertEquals("e3.type error - e3.info", str(e3))


test.main()
