import os
import subprocess
import datetime
import time
import re

from rich import print
from rich.console import Console
from rich.table import Table
from rich.live import Live

# global variables
console = Console()

services = {
    "postgresql2": {
        "type": "docker",
        "activated": False
    },

    "nginx": {
        "type": "systemctl",
        "activated": False
    },

    "rabbitmq": {
        "type": "docker",
        "activated": False
    },

    "php7.4-fpm": {
        "type": "systemctl",
        "activated": False
    },

    "redis-stack": {
        "type": "docker",
        "activated": False
    },

    "spring-android-users-locations.service": {
        "type": "systemctl",
        "activated": False
    }
}

def show_table() -> Table:
    table = Table(show_header=True, header_style="bold orange1")

    # headers
    table.add_column("Date", style="dim", width=28)
    table.add_column("Service", min_width=28)
    table.add_column("Commands", style="dim", width=20)

    # rows
    current_ts = datetime.datetime.now().isoformat()
    
    #if isDockerStarted("postgresql2"):
    if services["postgresql2"]["activated"]:
        table.add_row(current_ts, "[bold white on green]postgresql[/bold white on green]", "[1r] Run / [1s] Stop")
    else:
        table.add_row(current_ts, "[dim]postgresql[/dim]", "[1r] Run / [1s] Stop")

    #if isSystemCtlStarted("nginx"):
    if services["nginx"]["activated"]:
        table.add_row(current_ts, "[bold white on green]nginx[/bold white on green]", "[2r] Run / [2s] Stop")
    else:
        table.add_row(current_ts, "[dim]nginx[/dim]", "[2r] Run / [2s] Stop")
        
    if isPM2Started("crawlee.server"):
        table.add_row(current_ts, "[bold white on green]crawlee.server[/bold white on green]", "[3r] Run / [3s] Stop")
    else:
        table.add_row(current_ts, "[dim]crawlee.server[/dim]", "[3r] Run / [3s] Stop")

    #if isDockerStarted("rabbitmq"):
    if services["rabbitmq"]["activated"]:
        table.add_row(current_ts, "[bold white on green]rabbitMQ[/bold white on green]", "[4r] Run / [4s] Stop")
    else:
        table.add_row(current_ts, "[dim]rabbitMQ[/dim]", "[4r] Run / [4s] Stop")

    #if isSystemCtlStarted("php7.4-fpm"):
    if services["php7.4-fpm"]["activated"]:
        table.add_row(current_ts, "[bold white on green]php7.4-fpm[/bold white on green]", "[5r] Run / [5s] Stop")
    else:
        table.add_row(current_ts, "[dim]php7.4-fpm[/dim]", "[5r] Run / [5s] Stop")

    #if isSystemCtlStarted("spring-android-users-locations.service"):
    if services["spring-android-users-locations.service"]["activated"]:
        table.add_row(current_ts, "[bold white on green]spring-android-users-locations.service[/bold white on green]", "[6r] Run / [6s] Stop")
    else:
        table.add_row(current_ts, "[dim]spring-android-users-locations.service[/dim]", "[6r] Run / [6s] Stop")

    #if isDockerStarted("redis-stack"):
    if services["redis-stack"]["activated"]:
        table.add_row(current_ts, "[bold white on green]redis[/bold white on green]", "[7r] Run / [7s] Stop")
    else:
        table.add_row(current_ts, "[dim]redis[/dim]", "[7r] Run / [7s] Stop")

    return table

def switch(operation):
    if operation == "1r":
        return dockerService("postgresql2", "start")
    elif operation == "1s":
        return dockerService("postgresql2", "stop")
    if operation == "2r":
        return systemctlService("nginx", "start")
    elif operation == "2s":
        return systemctlService("nginx", "stop")
    elif operation == "3r":
        return startCrawleeServer()
    elif operation == "3s":
        return stopCrawleeServer()
    elif operation == "4r":
        return dockerService("rabbitmq", "start")
    elif operation == "4s":
        return dockerService("rabbitmq", "stop")
    elif operation == "5r":
        return systemctlService("php7.4-fpm", "start")
    elif operation == "5s":
        return systemctlService("php7.4-fpm", "stop")
    elif operation == "6r":
        return startSpringAndroidUsersLocations()
    elif operation == "6s":
        return stopSpringAndroidUsersLocations()
    elif operation == "7r":
        return dockerService("redis-stack", "start")
    elif operation == "7s":
        return dockerService("redis-stack", "stop")
    
def startCrawleeServer():
    print("Starting crawlee server...")
    subprocess.run(["./src/bash/start_crawlee_server.sh", ""], shell=True)

def stopCrawleeServer():
    print("Stopping crawlee server...")
    subprocess.run(["./src/bash/stop_crawlee_server.sh", ""], shell=True)

def startSpringAndroidUsersLocations():
    print("[bold yellow]Starting SpringAndroidUssersLocations...[/bold yellow]")

    # dependency: rabbitmq
    if not isDockerStarted("rabbitmq"):
        dockerService("rabbitmq", "start")

    os.system("systemctl start  ")
    systemctlService("spring-android-users-locations.service", "start")

def stopSpringAndroidUsersLocations():
    print("[bold yellow]Stopping SpringAndroidUssersLocations...[/bold yellow]")
    systemctlService("spring-android-users-locations.service", "stop")
    
def isSystemCtlStarted(service: str) -> bool:
    cmd = "systemctl status " + service
    result = os.popen(cmd).read()
    regx = re.findall("Active.*", result)
    status: str = regx[0].split(": ")[1]

    print(f'isSystemCtlStarted({service}) - status: {status}')

    if (status.startswith("inactive")):
        return False
    else:
        return True

def isDockerStarted(service: str) -> bool:
    cmd = "docker ps"
    result = os.popen(cmd).read()
    regx = re.findall(service, result)

    print(f'isDockerStarted({service}) - regx: {regx} - status: {len(regx)}')

    if len(regx) > 0:
        return True
    else:
        return False

def isPM2Started(service: str) -> bool:
    subp = subprocess.run(["./src/bash/status_pm2.sh", ""], shell=True, text=True, capture_output=True)
    pm2Res = subp.stdout
    lineApp = pm2Res.split("\n")[3]

    regx = re.findall(service, lineApp)

    stripLineApp = lineApp.replace(' ', '')
    tokens = stripLineApp.split(chr(9474))
    status = tokens[9]

    print(f'isPM2Started({service}) - lineApp: {lineApp}')
    print(f'isPM2Started({service}) - regx: {regx} - status: {status}')

    if status == "online":
        return True
    else:
        return False
    
def systemctlService(service: str, action: str):
    command = f'systemctl {action} {service}'
    print(command)
    os.system(command)

    # update services
    if action == "start":
        services[service]["activated"] = True
    elif action == "stop":
        services[service]["activated"] = False


def dockerService(service: str, action: str):
    command = f'docker {action} {service}'
    print(command)
    os.system(command)

    # update services
    if action == "start":
        services[service]["activated"] = True
    elif action == "stop":
        services[service]["activated"] = False

def initServices():
    print("=== initServices() ===")
    for service, value in services.items():
        if value["type"] == "docker":
            value["activated"] = isDockerStarted(service)
            
        elif value["type"] == "systemctl":
            value["activated"] = isSystemCtlStarted(service)

    for service, value in services.items():
        print(service, value)

#
# main
#
operation = ""

initServices()

with Live(show_table(), refresh_per_second=6) as live:
    while (operation != "x"):
        #os.system("clear")
        time.sleep(0.4)
        live.update(show_table())
        operation = input("Choose an operation ('x' to exit): ")
        switch(operation)

