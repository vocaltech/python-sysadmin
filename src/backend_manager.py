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

def show_table() -> Table:
    table = Table(show_header=True, header_style="bold orange1")

    # headers
    table.add_column("Date", style="dim", width=28)
    table.add_column("Service", min_width=28)
    table.add_column("Commands", style="dim", width=20)

    # rows
    current_ts = datetime.datetime.now().isoformat()
    
    """
    if isDockerStarted("postgresql2"):
        table.add_row(current_ts, "[bold white on green]postgresql[/bold white on green]", "[1r] Run / [1s] Stop")
    else:
        table.add_row(current_ts, "[dim]postgresql[/dim]", "[1r] Run / [1s] Stop")

    if isSystemCtlStarted("nginx"):
        table.add_row(current_ts, "[bold white on green]nginx[/bold white on green]", "[2r] Run / [2s] Stop")
    else:
        table.add_row(current_ts, "[dim]nginx[/dim]", "[2r] Run / [2s] Stop")
        
    if isPM2Started("crawlee.server"):
        table.add_row(current_ts, "[bold white on green]crawlee.server[/bold white on green]", "[3r] Run / [3s] Stop")
    else:
        table.add_row(current_ts, "[dim]crawlee.server[/dim]", "[3r] Run / [3s] Stop")

    if isDockerStarted("rabbitmq"):
        table.add_row(current_ts, "[bold white on green]rabbitMQ[/bold white on green]", "[4r] Run / [4s] Stop")
    else:
        table.add_row(current_ts, "[dim]rabbitMQ[/dim]", "[4r] Run / [4s] Stop")

    if isSystemCtlStarted("php7.4-fpm"):
        table.add_row(current_ts, "[bold white on green]php7.4-fpm[/bold white on green]", "[5r] Run / [5s] Stop")
    else:
        table.add_row(current_ts, "[dim]php7.4-fpm[/dim]", "[5r] Run / [5s] Stop")

    if isSystemCtlStarted("spring-android-users-locations.service"):
        table.add_row(current_ts, "[bold white on green]spring-android-users-locations.service[/bold white on green]", "[6r] Run / [6s] Stop")
    else:
        table.add_row(current_ts, "[dim]spring-android-users-locations.service[/dim]", "[6r] Run / [6s] Stop")

    """

    if isDockerStarted("postgresql2"):
        table.add_row(current_ts, "[bold white on green]postgresql[/bold white on green]", "[1r] Run / [1s] Stop")
    else:
        table.add_row(current_ts, "[dim]postgresql[/dim]", "[1r] Run / [1s] Stop")

    if isSystemCtlStarted("nginx"):
        table.add_row(current_ts, "[bold white on green]nginx[/bold white on green]", "[2r] Run / [2s] Stop")
    else:
        table.add_row(current_ts, "[dim]nginx[/dim]", "[2r] Run / [2s] Stop")

    if isPM2Started("crawlee.server"):
        table.add_row(current_ts, "[bold white on green]crawlee.server[/bold white on green]", "[3r] Run / [3s] Stop")
    else:
        table.add_row(current_ts, "[dim]crawlee.server[/dim]", "[3r] Run / [3s] Stop")

    return table

def switch(operation):
    if operation == "1r":
        return startPostgres()
    elif operation == "1s":
        return stopPostgres()
    if operation == "2r":
        return startNginx()
    elif operation == "2s":
        return stopNginx()
    elif operation == "3r":
        return startCrawleeServer()
    elif operation == "3s":
        return stopCrawleeServer()
    elif operation == "4r":
        return startRabbitMq()
    elif operation == "4s":
        return stopRabbitMq()
    elif operation == "5r":
        return startPhp()
    elif operation == "5s":
        return stopPhp()
    elif operation == "6r":
        return startSpringAndroidUsersLocations()
    elif operation == "6s":
        return stopSpringAndroidUsersLocations()
    
def startPostgres():
    print("Starting postgres...")
    os.system("docker start postgresql2")

def stopPostgres():
    print("Stopping postgres...")
    os.system("docker stop postgresql2")

def startNginx():
    print("Starting nginx...")
    os.system("systemctl start nginx")

def stopNginx():
    print("Stopping nginx...")
    os.system("systemctl stop nginx")

def startCrawleeServer():
    print("Starting crawlee server...")
    subprocess.run(["./src/bash/start_crawlee_server.sh", ""], shell=True)

def stopCrawleeServer():
    print("Stopping crawlee server...")
    subprocess.run(["./src/bash/stop_crawlee_server.sh", ""], shell=True)

def startRabbitMq():
    print("Starting rabbitmq...")
    os.system("docker start rabbitmq")

def stopRabbitMq():
    print("Stopping rabbitmq...")
    os.system("docker stop rabbitmq")

def startPhp():
    print("Starting php...")
    os.system("systemctl start php7.4-fpm")

def stopPhp():
    print("Stopping php...")
    os.system("systemctl stop php7.4-fpm")

def startSpringAndroidUsersLocations():
    print("[bold yellow]Starting SpringAndroidUssersLocations...[/bold yellow]")

    # dependency: rabbitmq
    if not isDockerStarted("rabbitmq"):
        startRabbitMq()

    os.system("systemctl start spring-android-users-locations.service ")

def stopSpringAndroidUsersLocations():
    print("[bold yellow]Stopping SpringAndroidUssersLocations...[/bold yellow]")
    os.system("systemctl stop spring-android-users-locations.service ")
    
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


#
# main
#
operation = ""

with Live(show_table(), refresh_per_second=5) as live:
    while (operation != "x"):
        os.system("clear")
        time.sleep(0.4)
        live.update(show_table())
        operation = input("Choose an operation ('x' to exit): ")
        switch(operation)

