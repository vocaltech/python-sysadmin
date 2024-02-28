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

def switch(operation):
    if operation == "1r":
        return startPostgres()
    elif operation == "1s":
        return stopPostgres()
    elif operation == "3r":
        return startCrawleeServer()
    elif operation == "3s":
        return stopCrawleeServer()
    
def startPostgres():
    print("Starting postgres...")
    os.system("docker start postgresql2")

def stopPostgres():
    print("Stopping postgres...")
    os.system("docker stop postgresql2")

def startCrawleeServer():
    print("Starting crawlee server...")
    subprocess.run(["./src/bash/start_crawlee_server.sh", ""], shell=True)

def stopCrawleeServer():
    print("Stopping crawlee server...")
    subprocess.run(["./src/bash/stop_crawlee_server.sh", ""], shell=True)

#
# main
#
show_ops()
print()

operation = ""

while (operation != "x"):
    operation = input("Choose an operation ('x' to exit): ")
    switch(operation)