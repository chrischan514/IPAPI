
import requests, sys, argparse
parser = argparse.ArgumentParser(description="IPAPI")
parser.add_argument('-i', dest="customDNS", action='store_true', help="Enable DNS proxy")
parser.add_argument('-v', dest="verbose", action='store_true', help="Verbose mode")

if parser.parse_args().customDNS is True:
    import dns.resolver
    customresolver = dns.resolver.Resolver()
    customresolver.nameservers = ['1.1.1.1','1.0.0.1','8.8.8.8','8.8.4.4']

    from urllib3.util import connection

    _orig_create_connection = connection.create_connection

    def patched_create_connection(address, *args, **kwargs):
        host, port = address

        dnsquery = customresolver.resolve(host, "a")
        for item in dnsquery:
            hostname = str(item)
            if parser.parse_args().verbose is True:
                print("Resolved IP Address: ",str(item))
        return _orig_create_connection((hostname, port), *args, **kwargs)

    connection.create_connection = patched_create_connection

print("To exit, type in exit() or exit")
combo = 0
def runQuery():
    global combo
    ip = input("> IP Address: ")
    apimap = ["http://ip-api.com/json/", "https://ipapi.co/"]
    suffix = ["", "/json/"]
    if ip == "exit()" or ip == "exit":
        sys.exit()
    status = 0
    while status == 0:
        try:
            response = requests.get("".join([apimap[combo], ip, suffix[combo]]))
        except:
            if combo < 1:
                print("Network Error! Trying Again...")
                combo = combo + 1
            else:
                print("Unable to solve the error, try again later!")
                sys.exit()
            pass
        else:
            if response.status_code != 429:
                status = 1
                json = response.json()
                if combo == 0:
                    if json["status"]=="success":
                        print("".join(["IP Address: ", json["query"], "\n", "Country: ", json["country"], "\n", "Region: ", json["regionName"], "\n", "City: ", json["city"], "\n", "ISP: ", json["isp"], "\n", "Organisation: ", json["org"], "\n", "AS: ", json["as"], "\n"]))
                    else:
                        print("Error, Try Again!")
                elif combo == 1:
                    if response.status_code == 200:
                        print("".join(["IP Address: ", json["ip"], "\n", "Country: ", json["country_name"], "\n", "Region: ", json["region"], "\n", "City: ", json["city"], "\n", "Organisation: ", json["org"], "\n", "AS Number: ", json["asn"], "\n"])
            else:
                combo = combo + 1


while 1:
    runQuery()
