from kubectl.commands.base import KubectlBase
import kubectl.util as util

class Logs(KubectlBase):
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

    result = self.call_capture('logs', *opts)
    print(result)

  def _get_opts(self):
    opts=[]
    container=self.request.get_optional_option('CONTAINER')
    if container is not None:
      opts.append("--container=%s" % container)
    selector=self.request.get_optional_option('SELECTOR')
    if selector is not None:
      opts.append("--selector=%s" % ",".join(selector))
    if self.request.get_optional_option('PREVIOUS') == "true":
      opts.append("--previous")
    since=self.request.get_optional_option('SINCE')
    if since is not None:
      opts.append("--since=%s" % since)
    tail=self.request.get_optional_option('TAIL')
    if tail is not None:
      opts.append("--tail=%i" % int(tail))
    else:
      # by default limit logs to 20
      opts.append("--tail=20")
    if self.request.get_optional_option('TIMESTAMPS') == "true":
      opts.append("--timestamps")
    return opts
