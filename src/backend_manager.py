import os
import subprocess

def show_ops():
    print("=============================")
    print("=     Backend Manager       =")
    print("=============================")
    print()
    print("--- postgresql ---")
    print()
    print("    [1r] Run")
    print("    [1s] Stop")
    print()
    print("--- nginx ---")
    print()
    print("    [2r] Run")
    print("    [2s] Stop")
    print()
    print("--- crawlee.server ---")
    print()
    print("    [3r] Run ")
    print("    [3s] Stop")
    print()
    print("--- rabbitmq ---")
    print()
    print("    [4r] Run ")
    print("    [4s] Stop")
    print()

    print("--- php7.4-fpm ---")
    print()
    print("    [5r] Run ")
    print("    [5s] Stop")
    print()

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

#
# main
#
show_ops()
print()

operation = ""

while (operation != "x"):
    operation = input("Choose an operation ('x' to exit): ")
    switch(operation)