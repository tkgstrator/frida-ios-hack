import argparse
import frida
import sys


def _compare_applications(a, b):
    a_is_running = a.pid != 0
    b_is_running = b.pid != 0
    if a_is_running == b_is_running:
        if a.identifier > b.identifier:
            return 1
        elif a.identifier < b.identifier:
            return -1
        else:
            return 0
    elif a_is_running:
        return -1
    else:
        return 1


def _compare_by_key(cmp):
    class K:
        def __init__(self, obj):
            self.obj = obj

        def __lt__(self, other):
            return cmp(self.obj, other.obj) < 0

        def __gt__(self, other):
            return cmp(self.obj, other.obj) > 0

        def __eq__(self, other):
            return cmp(self.obj, other.obj) == 0

        def __le__(self, other):
            return cmp(self.obj, other.obj) <= 0

        def __ge__(self, other):
            return cmp(self.obj, other.obj) >= 0

        def __ne__(self, other):
            return cmp(self.obj, other.obj) != 0
    return K


def get_applications(device):
    try:
        applications = device.enumerate_applications()
    except Exception as e:
        sys.exit('Failed to enumerate applications: %s' % e)
    return applications


def list_applications():
    print('Listing installed apps')
    manager = frida.get_device_manager()
    device = manager.add_remote_device('192.168.13.17')
    applications = get_applications(device)
    print(f"{'PID':<8}{'IDENTIFIER':<48}{'NAME':<64}")
    print("-" * 64)
    identifier_width = int((max(len(application.identifier)
                                for application in applications) * 0.25 + 1) * 4)
    name_width = max(len(application.name) for application in applications)
    for application in sorted(applications, key=_compare_by_key(_compare_applications)):
        print(f"{application.pid:<8}{
              application.identifier:<{identifier_width}}{application.name:<{identifier_width+name_width}}")


def dump_applications():
    print('Decrypting the installed app')


if __name__ == '__main__':
    print('iOS app manager')
    parser = argparse.ArgumentParser(description='iOS app manager')
    parser.add_argument('-l', '--list', dest='list_applications',
                        action='store_true', help='List installed apps')
    parser.add_argument('-d', '--dump', dest='dump_application',
                        action='store_true', help='Dump the installed app')
    parser.add_argument(
        'target', nargs='?', help='Bundle identifier of the target app')
    args = parser.parse_args()

    if args.list_applications:
        list_applications()

    if args.dump_application:
        dump_applications()
