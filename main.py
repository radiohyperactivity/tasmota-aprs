import os
import aprs
import requests
import re

call = os.environ.get("CALL")
admin = os.environ.get("ADMIN")
tasmota = os.environ.get("TASMOTA")
tnc_host = os.environ.get("TNC_HOST")
tnc_port = int(os.environ.get("TNC_PORT"))

def main():
    tnc = aprs.TCPKISS(host = tnc_host, port = tnc_port)
    tnc.start()

    while True:
        for frame in tnc.read(min_frames = 1):
            sender = f"{frame.source.callsign.decode()}-{frame.source.ssid}"

            if frame.info.data_type == aprs.DataType.MESSAGE:
                if frame.info.addressee.decode() == call:
                    if sender == admin:
                        command = frame.info.text.decode().lower()

                        response = None

                        if re.search("power on", command, re.IGNORECASE):
                            response = requests.get(f"{tasmota}cmnd=Power%20On", timeout = 5)
                        elif re.search("power off", command, re.IGNORECASE):
                            response = requests.get(f"{tasmota}cmnd=Power%20Off", timeout = 5)
                        elif re.search("power cycle", command, re.IGNORECASE):
                            response = requests.get(f"{tasmota}cmnd=Backlog%20Power%20Off%3B%20Delay%20300%3B%20Power%20On", timeout = 5)

                        if response != None and response.status_code == 200 and frame.info.number != None:
                            tnc.write(aprs.APRSFrame.ui(
                                destination = "APZ001",
                                source = call,
                                path = ["WIDE1-1", "WIDE2-1"],
                                info = f":{sender.ljust(9)}:ack{frame.info.number.decode()}".encode("utf-8")
                            ))

if __name__ == "__main__":
    main()