from kubectl.commands.base import KubectlBase
import kubectl.util as util

class Expose(KubectlBase):
  def __init__(self):
    super().__init__()

  def run(self):
    if self.request.args == None:
      self.fail("Resource type and name to expose missing")
    elif len(self.request.args) < 2:
      self.fail("Resource name to expose missing")
    elif len(self.request.args) > 2:
      self.fail("Too many arguments")

    resource_type = self.request.args[0]
    resource_name = self.request.args[1]
    opts=[]
    try:
      opts = self._get_opts()
    except:
      pass

    result = self.call_json('expose', resource_type, resource_name, *opts)

    parsed_results=self._parse(result)
    self.response.content(parsed_results, template="resource_list").send()

  def _get_opts(self):
    opts=[]
    service_type=self.request.get_optional_option('TYPE')
    if service_type is not None:
      opts.append("--type=%s" % service_type)
    port=self.request.get_optional_option('PORT')
    if port is not None:
      opts.append("--port=%i" % int(port))
    target_port=self.request.get_optional_option('TARGET-PORT')
    if target_port is not None:
      opts.append("--target-port=%i" % int(target_port))
    return opts
