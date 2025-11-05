import os
import aprs
import requests
import re
import logging
import logging.handlers

call = os.environ.get("CALL", "LAMP")
admin = os.environ.get("ADMIN", "LB5JJ-2")
tasmota = os.environ.get("TASMOTA", "http://192.168.10.213/cm?")
tnc_host = os.environ.get("TNC_HOST", "192.168.10.246")
tnc_port = int(os.environ.get("TNC_PORT", "8001"))
syslog_host = os.environ.get("SYSLOG_HOST", "10.211.244.1")

logger = logging.getLogger("tasmota-aprs")
logger.setLevel(logging.DEBUG)

handler = logging.handlers.SysLogHandler(address=(syslog_host, 514))
handler.setFormatter(logging.Formatter('%(name)s: %(levelname)s - %(message)s'))
logger.addHandler(handler)

def main():
    logger.info("Starting up...")

    tnc = aprs.TCPKISS(host = tnc_host, port = tnc_port)
    tnc.start()

    while True:
        for frame in tnc.read(min_frames = 1):
            if frame.info.data_type == aprs.DataType.MESSAGE:
                to = frame.info.addressee.decode()

                if to == call:
                    sender = f"{frame.source.callsign.decode()}-{frame.source.ssid}"

                    if sender == admin:
                        command = frame.info.text.decode().lower()

                        logger.info("Command \"%s\" from \"%s\" to \"%s\" received", command, sender, to)

                        response = None

                        if re.search("power on", command, re.IGNORECASE):
                            response = requests.get(f"{tasmota}cmnd=Power%20On", timeout = 5)
                            logger.info("Executed Power On command - respons code: %i", response.status_code)
                        elif re.search("power off", command, re.IGNORECASE):
                            response = requests.get(f"{tasmota}cmnd=Power%20Off", timeout = 5)
                            logger.info("Executed Power Off command - respons code: %i", response.status_code)
                        elif re.search("power cycle", command, re.IGNORECASE):
                            response = requests.get(f"{tasmota}cmnd=Backlog%20Power%20Off%3B%20Delay%2050%3B%20Power%20On", timeout = 5)
                            logger.info("Executed Power Cycle command - respons code: %i", response.status_code)

                        if response != None and response.status_code == 200 and frame.info.number != None:
                            tnc.write(aprs.APRSFrame.ui(
                                destination = "APZ001",
                                source = call,
                                path = ["WIDE1-1", "WIDE2-1"],
                                info = f":{sender.ljust(9)}:ack{frame.info.number.decode()}".encode("utf-8")
                            ))
                            logger.info("Sent Ack: %s", frame.info.number.decode())
                    else:
                        logger.debug("Sender not admin: %s", sender)
                else:
                    logger.debug("Not for me: %s", to)
            else:
                logger.debug("Not type message: %s", frame.info.data_type)

if __name__ == "__main__":
    main()
