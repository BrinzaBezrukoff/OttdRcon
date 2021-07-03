from libottdadmin2.client.tracking import TrackingMixIn
from libottdadmin2.client.sync import OttdSocket, DefaultSelector
from libottdadmin2.packets import AdminRcon
from libottdadmin2.enums import DestType, ChatAction

from app import app, scheduler


dests = {
    DestType.BROADCAST: "All",
    DestType.TEAM: "Team",
    DestType.CLIENT: "Client"
}


class Client(TrackingMixIn, OttdSocket):
    def __init__(self, *args, **kwargs):
        super(Client, self).__init__(*args, **kwargs)
        self.__console = ""
        self.users = {}

    @property
    def console(self):
        t = self.__console
        self.__console = ""
        return t

    def on_server_rcon(self, colour, result):
        self.__console += result + "\n"

    def send_command(self, command):
        arp = AdminRcon()
        arp.encode(command)
        self.send_packet(arp)

    def on_server_chat(self, action, type, client_id, message, extra):
        if client_id == 1 or action != ChatAction.CHAT:
            return
        self.__console += f"[{dests[type]}] {self.users[client_id]['name']}: {message}\n"

    def on_server_client_info(self, client_id, hostname, name, language, joindate, play_as):
        self.users[client_id] = {
            "name": name,
            "hostname": hostname,
            "lang": language,
            "join_date": joindate,
            "play_as": play_as
        }


selector = DefaultSelector()
client = Client(password=app.config["OTTD_PASSWORD"])
client.connect((app.config["OTTD_HOST"], app.config["OTTD_PORT"]))
client.setblocking(False)
client.register_to_selector(selector)


def updater():
    while selector.get_map():
        events = selector.select()
        for key, mask in events:
            callback = key.data
            callback(key.fileobj, mask)


scheduler.add_job("updater", updater)
