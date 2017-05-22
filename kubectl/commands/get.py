from kubectl.commands.base import KubectlBase
import kubectl.util as util

class Get(KubectlBase):
  def __init__(self):
    super().__init__()

  def run(self):
    if self.request.args == None:
        self.fail("Missing resource type to get")

    resource_type = self.request.args[0]

    opts=[]
    try:
      opts = self._get_opts()
    except:
      pass

    result = self.call_json('get',resource_type, *opts)

    parsed_results=self._parse(result)
    self.response.content(parsed_results, template="resource_list").send()

  def _get_opts(self):
    opts=[]
    if self.request.get_optional_option('ALL-NAMESPACES') == "true":
      opts.append("--all-namespaces")
    if self.request.get_optional_option('SHOW-ALL') == "true":
      opts.append("--show-all")
    selector=self.request.get_optional_option('SELECTOR')
    if selector is not None:
      opts.append("--selector=%s" % ",".join(selector))
    sort_by=self.request.get_optional_option('SORT-BY')
    if sort_by is not None:
      opts.append("--sort-by=%s" %sort_by)
    return opts
