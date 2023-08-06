import argparse

parser = argparse.ArgumentParser(
                    prog='visioncar',
                    description='Find and interact with CV robot cars')
parser.add_argument("hostname", nargs="?", help="Hostname of the robot to connect to. If left blank, searches for robots")
parser.add_argument("-V", "--verbose", action="store_true", help="Verbose mode")
parser.add_argument("-v", "--novideo", action="store_true", help="Disable video stream")
parser.add_argument("-c", "--nocommand", action="store_true", help="Disable command stream")


args = parser.parse_args()

hostname = args.hostname
if not hostname:
    from zeroconf import ServiceBrowser, ServiceListener, Zeroconf

    robots = [None] # quit on 0

    class MDNSListener(ServiceListener):

        def update_service(self, zc: Zeroconf, type_: str, name: str) -> None:
            print(f"{name} updated")

        def remove_service(self, zc: Zeroconf, type_: str, name: str) -> None:
            print(f"{name} removed")

        def add_service(self, zc: Zeroconf, type_: str, name: str) -> None:
            name = name.split(".")[0]
            print(f"#{len(robots)}: {name}")
            robots.append(name)


    zeroconf = Zeroconf()
    listener = MDNSListener()

    ServiceBrowser(zeroconf, "_control-socket._udp.local.", listener)

    try:
        i = int(input("Select robot number and press Enter. Choose 0 to quit\n"))
    except:
        exit(0)
    finally:
        zeroconf.close()

    if i == 0:
        exit(0)

    hostname = robots[i]

import cv2
import threading
import time

from . import visioncar

_console = None
robot = visioncar.Robot.discover(hostname)
if not robot:
    print("failed to connect")
    exit(1)

if args.verbose:
    robot._loglevel(2)
    robot._esp_log(1)
    robot._stall_timeout(500)

def _quit():
    robot.close()
    if not args.novideo:
        cv2.destroyAllWindows()
    exit(0)

if not args.nocommand:
    robot.open_control()

    if not robot.set_speed(30):
        if not robot.set_speed(30):
            print("Failed to set initial speed")
            _quit()

# Unrelated to control socket, can be called anyway
robot.set_control("led_intensity", 0)
robot.show_video()

import code

# Work around readline only available on UNIX
try:
    import readline
except:
    pass

_console = code.InteractiveConsole(locals=globals())
_console.interact(
    banner=f"""
Exported variables: robot, hostname
Modules loaded: cv2, threading, time, visioncar
Connected to {hostname}""",
    exitmsg=f"Disconnecting from {hostname}"
)
_quit()
