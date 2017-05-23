from kubectl.commands.base import KubectlBase
import kubectl.util as util

class Set_image(KubectlBase):
  def __init__(self):
    super().__init__()

  def run(self):
    if self.request.args == None:
      self.fail("Resource type and name missing")

    result = self.call_capture('set','image', *self.request.args)
    print(result)
