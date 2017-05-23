from kubectl.commands.base import KubectlBase
import kubectl.util as util

class Delete(KubectlBase):
  def __init__(self):
    super().__init__()

  def run(self):
    opts=[]

    # test if there are any options
    try:
      opts = self._get_opts()
    except:
      pass

    # just pass through all arguments after the options
    opts.extend(self.request.args)

    result = self.call_capture('delete', *opts)
    print(result)

  def _get_opts(self):
    opts=[]
    if self.request.get_optional_option('FORCE') == "true":
      opts.append("--force")
    selector=self.request.get_optional_option('SELECTOR')
    if selector is not None:
      opts.append("--selector=%s" % ",".join(selector))
    grace_period=self.request.get_optional_option('GRACE-PERIOD')
    if grace_period is not None:
      opts.append("--grace-period=%i" % int(grace_period))
    return opts
