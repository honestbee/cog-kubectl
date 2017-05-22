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

  ## TODO: Fix this ugly hack
  def _parse_item(self, item):
    self.response.debug(json.dumps(item))
    common = {
      "Kind": item["kind"],
      "Namespace": item["metadata"]["namespace"],
      "Name": item["metadata"]["name"],
      "Timestamp": item["metadata"]["creationTimestamp"],
      "Color": "gray"
    }
    if item["kind"] == 'Pod':
      common.update({
        "Count": len(item["status"]["containerStatuses"]),
        "ReadyCount": len([c for c in item["status"]["containerStatuses"] if c["ready"]]),
        "Restarts" : sum([c["restartCount"] for c in item["status"]["containerStatuses"]]),
        "Status": item["status"]["phase"],
        "Color": {
            "Pending": "blue",
            "Failed": "red",
            "Succeeded": "green",
            "Running": "green"
        }.get(item["status"]["phase"],"gray"),
        "Node": item["spec"]["nodeName"]
      })
    elif item["kind"] == 'Service':
      common.update({
        "ClusterIP": item["spec"]["clusterIP"],
        "Ports": item["spec"]["ports"],
        "Type": item["spec"]["type"]
      })
      if common["Type"] == "ClusterIP":
        common["ExternalIP"] = "None"
      elif common["Type"] == "NodePort":
        common["ExternalIP"] = "Nodes"
      elif common["Type"] == "LoadBalancer":
        ingress = item["status"]["loadBalancer"].get("ingress")
        if ingress is not None:
          common["ExternalIP"] = ",".join([i["hostname"] for i in ingress])
        else:
          common["ExternalIP"] = "Pending"
      else:
        common["ExternalIP"] == "Unknown"
    elif item["kind"] == 'Deployment':
      common.update({
        "Desired": item["spec"]["replicas"],
        "Color": "gray"
      })
      status = item.get("status")
      common.update({} if status is None else {"Current": status.get("replicas")})
      common.update({} if status is None else {"Available": status.get("availableReplicas")})
      common.update({} if status is None else {"Unavailable": status.get("unavailableReplicas")})
      common.update({} if status is None else {"Updated": status.get("updatedReplicas")})
      if common["Available"] is not None and common["Desired"] <= common["Available"]:
        common["Color"] = "green"
      elif common["Current"] is not None and common["Desired"] <= common["Current"]:
        common["Color"] = "orange"
      else:
        common["Color"] = "red"
    # self.response.debug(json.dumps(common))
    return common
