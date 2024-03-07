import os
import re

####################################################
#
# Update some rules with a given remoteIp
#
####################################################

#
# Functions
#
def getSSHRemoteIp() -> str:
  stream = os.popen('echo $SSH_CLIENT')
  return stream.read().split()[0]

def getRuleId(currentRule: str) -> str:
  result = re.search(r"(\d+)", currentRule)
  return result.group(1)

def getUfwRules() -> list:
  stream = os.popen('ufw status numbered')
  return stream.readlines()

def deleteRule(port: str):
  ufwRules = getUfwRules()

  for i in range(len(ufwRules)):
    if i >= 4:
      currentRule = ufwRules[i]

      if port in currentRule:
        ruleId = getRuleId(currentRule)
        txt = "found " + port + " - ruleId to delete: {}"
        print(txt.format(ruleId))
        deleteRule = "echo 'y' | ufw delete " + ruleId
        os.system(deleteRule)

def addRule(fromIp: str, port: str, protocol: str):
  addRule = "ufw allow from " + fromIp + " to any port " + port  + " proto " + protocol
  os.system(addRule)

#
# main
#

# Get ssh remote ip address
txt = "Remote ip addr: {}"
print(txt.format(getSSHRemoteIp()))

# Update rule with port 5432
deleteRule("5432")
addRule(getSSHRemoteIp(), "5432", "tcp")

# Update rule with port 27017
deleteRule("27017")
addRule(getSSHRemoteIp(), "27017", "tcp")

# Update rule with port 3306
deleteRule("3306")
addRule(getSSHRemoteIp(), "3306", "tcp")

# Update rule with port 8000 (symfony)
deleteRule("8000")
addRule(getSSHRemoteIp(), "8000", "tcp")

# Update rule with port 8081 (spring-android)
deleteRule("8081")
addRule(getSSHRemoteIp(), "8081", "tcp")