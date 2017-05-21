from kubectl.commands.base import KubectlBase
import kubectl.util as util

class Get(KubectlBase):
  def __init__(self):
    super().__init__()

  def run(self):
    if self.request.args == None:
        self.fail("Missing resource type to get")

    resource_type = self.request.args[0]
    # resource_types = resource_type.split(",")

    args = self._get_args()
    result = self.call_json('get',resource_type, *args)

    parsed_results=self._parse(result)
    self.response.content(parsed_results, template="resource_list").send()

  def _get_args(self):
    args=[]
    if self.request.get_optional_option('ALL-NAMESPACES') == "true":
      args.append("--all-namespaces")
    if self.request.get_optional_option('SHOW-ALL') == "true":
      args.append("--show-all")
    selector=self.request.get_optional_option('SELECTOR')
    if selector is not None:
      args.append("--selector=%s" %selector)
    sort_by=self.request.get_optional_option('SORT-BY')
    if sort_by is not None:
      args.append("--sort-by=%s" %sort_by)
    return args

  def _parse(self,data):
    results = []
    if data["kind"] == "List":
        for i in data["items"]:
            results.append(self._parse_item(i))
    else:
        results.append(self._parse_item(data))
    return results

  def _parse_item(self,item):
    if item["kind"] == 'Pod':
      return {
        "Kind": item["kind"],
        "Namespace": item["metadata"]["namespace"],
        "Name": item["metadata"]["name"],
        "Count": len(item["status"]["containerStatuses"]),
        "ReadyCount": len([c for c in item["status"]["containerStatuses"] if c["ready"]]),
        "Restarts" : sum([c["restartCount"] for c in item["status"]["containerStatuses"]]),
        "Status": item["status"]["phase"],
        "Color": {
            "Pending": "yellow",
            "Failed": "red",
            "Succeeded": "green",
            "Running": "green",
        }.get(item["status"]["phase"],"gray"),
        "Node": item["spec"]["nodeName"],
        "Timestamp": item["metadata"]["creationTimestamp"]
      }
    elif item["kind"] == 'Service':
        return {
          "Kind": item["kind"],
          "Namespace": item["metadata"]["namespace"],
          "Name": item["metadata"]["name"]
        }
