from kubectl.commands.base import KubectlBase
import kubectl.util as util

class Scale(KubectlBase):
  def __init__(self):
    super().__init__()

  def run(self):
    if self.request.args == None:
      self.fail("RESOUCE_TYPE/RESOURCE_NAME required")

    resource = self.request.args[0]
    opts = self._get_opts()
    result = self.call_capture('scale', resource, *opts)
    print(result)

  def _get_opts(self):
    opts=[]
    opts.append("--replicas=%i" % int(self.request.options["REPLICAS"]))
    current_replicas=self.request.get_optional_option('CURRENT-REPLICAS')
    if current_replicas is not None:
      opts.append("--current-replicas=%i" % int(current_replicas))
    return opts
