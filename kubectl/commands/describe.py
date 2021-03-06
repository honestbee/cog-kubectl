from kubectl.commands.base import KubectlBase
import kubectl.util as util
from sys import stdout

class Describe(KubectlBase):
  def __init__(self):
    super().__init__()

  def run(self):
    if self.request.args == None:
      self.fail("You must specify the type of resource to describe")

    opts=[]
    try:
      opts = self._get_opts()
    except:
      pass

    opts.extend(self.request.args)

    try:
      # takes in array of objects from stdin
      if self.request.input is not None:
        self.response.debug(json.dumps(self.request.input))
        # assume all input objects have a "Name" key or fail
        opts.extend([i["Name"] for i in self.request.input])
    except:
      pass

    result = self.call_capture('describe', *opts)

    # another hack to force output
    print("COG_TEMPLATE: pre")
    print(result)
    stdout.flush()

  def _get_opts(self):
    opts=[]
    selector=self.request.get_optional_option('SELECTOR')
    if selector is not None:
      opts.append("--selector=%s" % ",".join(selector))
    return opts
