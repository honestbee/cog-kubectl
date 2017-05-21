from cog.command import Command
import subprocess
import json
import base64


CERT_PATH = "/etc/kube/ca.pem"

class KubectlBase(Command):
  def __init__(self):
    super().__init__()
    self.kubernetes_token = None
    self.kubernetes_server = None
    self.kubernetes_cert = None
    self._kubectl = "/usr/local/bin/kubectl"

  def prepare(self):
    self.kubernetes_token = self.config("KUBERNETES_TOKEN")
    if self.kubernetes_token == None:
      self.fail("Missing dynamic configuration variable 'KUBERNETES_TOKEN'.")

    self.kubernetes_server = self.config("KUBERNETES_SERVER")
    if self.kubernetes_server == None:
      self.fail("Missing dynamic configuration variable 'KUBERNETES_SERVER'.")

    # decode cert to disk
    self.kubernetes_cert = self.config("KUBERNETES_CERT")
    if self.kubernetes_cert == None:
      self.fail("Missing dynamic configuration variable 'KUBERNETES_CERT' (base64 encoded CA cert).")
    else:
      with open(CERT_PATH, "wb") as fh:
        fh.write(base64.b64decode(self.kubernetes_cert))

  def call_json(self, cmd, *args):
    return json.loads(self.call_capture(cmd, '--output=json', *args))

  def call_capture(self, cmd, *args):
    cl = self._commandline(cmd, *args)
    val = subprocess.check_output(cl)
    return val.decode('utf-8')

  def _commandline(self, command, *args):
    commandline = [self._kubectl]
    commandline.extend(['--server', self.kubernetes_server])
    commandline.extend(['--token', self.kubernetes_token])
    commandline.extend(['--certificate-authority', CERT_PATH])
    commandline.append(command)
    commandline.extend(args)
    # self.response.debug(json.dumps(list(map(str, commandline))))
    return commandline

  def _parse(self, data):
    results = []
    if data["kind"] == "List":
        for i in data["items"]:
            results.append(self._parse_item(i))
    else:
        results.append(self._parse_item(data))
    return results

  def _parse_item(self, item):
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
    elif item["kind"] == 'Deployment':
      return {
        "Kind": item["kind"],
        "Namespace": item["metadata"]["namespace"],
        "Name": item["metadata"]["name"]
      }