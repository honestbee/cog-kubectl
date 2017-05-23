from kubectl.commands.base import KubectlBase
import kubectl.util as util

class Set_image(KubectlBase):
  def __init__(self):
    super().__init__()

  def run(self):
    if self.request.args == None:
      self.fail("Resource type and name missing")
    elif len(self.request.args) < 2:
      self.fail("Resource name to expose missing")
    elif len(self.request.args) > 2:
      self.fail("Too many arguments")

    resource = self.request.args[0]
    kvpairs = self.request.args[1:]
    result = self.call_capture('set','image', resource, *kvpairs)
    print(result)
