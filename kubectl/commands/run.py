from kubectl.commands.base import KubectlBase
import kubectl.util as util

class Run(KubectlBase):
  def __init__(self):
    super().__init__()

  def run(self):
    if self.request.args == None:
        self.fail("Missing name")

    name = self.request.args[0]
    command = self.request.args[2]
    opts = self._get_opts()
    result = self.call_json('run',name, *opts)

    parsed_results=self._parse(result)
    self.response.content(parsed_results, template="resource_list").send()

  def _get_opts(self):
    opts=[]
    opts.append(self.request.get_option("IMAGE"))
    if self.request.get_optional_option('expose') == "true":
      opts.append("--expose")
    port=self.request.get_optional_option('PORT')
    if port is not None:
      opts.append("--port=%s" % port)
    return opts
