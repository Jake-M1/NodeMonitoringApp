from flask import Flask, render_template, request
import socket
import time

app = Flask(__name__)
ips = ["8.8.8.8", "0.0.0.0"]

# main route
@app.route('/')
def index():
    status, times = monitorNetworks(ips)
    return render_template('index.html', IPs=ips, status=status, times=times)

# for the form submit
@app.route('/create', methods=['POST'])
def addNewIp():
    ip = request.form["ipform"]
    ips.append(ip)
    return app.redirect('/')

# given a list of IP addresses, monitor the connectivity
def monitorNetworks(ipAddresses: list) -> list:
    print("Running...")
    status = []
    times = []
    # loop through IP Addresses and ping each
    for ipAddr in ipAddresses:
        if ping(ipAddr):
            status.append("Reachable")
            print("Reachable: " + ipAddr)
        else:
            status.append("Unreachable")
            print("Unreachable: " + ipAddr)
        currTime = time.strftime("%H:%M:%S", time.localtime())
        times.append(currTime)
    return status, times

# ping the IP Address using python socket library
def ping(ipAddr):
    try:
        # try to connect to the IP Address
        socket.setdefaulttimeout(2)
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        port = 53
        serverAddress = (ipAddr, port)
        s.connect(serverAddress)
 
    # return false on failed connection
    except OSError:
        return False
 
    # close the socket and return true if successful connection
    else:
        s.close()
        return True

# main app run
if __name__ == "__main__":
    app.run(debug=True)