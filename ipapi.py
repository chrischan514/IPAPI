import requests, sys
print("To exit, type in exit() or exit")
def runQuery():
    ip = input("> IP Address: ")
    if ip == "exit()" or ip == "exit":
        sys.exit()
    try:
        response = requests.get("".join(["http://ip-api.com/json/", ip]))
    except:
        print("Error occurred! Please Try Again!")
        pass
    else:
        json = response.json()
        if json["status"]=="success":
            print("".join(["IP Address: ", json["query"], "\n", "Country: ", json["country"], "\n", "Region: ", json["regionName"], "\n", "City: ", json["city"], "\n", "ISP: ", json["isp"], "\n", "Organisation: ", json["org"], "\n", "AS: ", json["as"], "\n"]))
        else:
            print("Error, Try Again!")

while 1:
    runQuery()
