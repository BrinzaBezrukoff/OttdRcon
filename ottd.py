import time
import hashlib
from functools import wraps

from flask import request, jsonify

from libottdadmin2.client.tracking import TrackingMixIn
from libottdadmin2.client.sync import OttdSocket, DefaultSelector
from libottdadmin2.packets import AdminRcon
from libottdadmin2.enums import DestType, ChatAction


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


class Session:
    def __init__(self, user_id, token, host, port, password):
        self.web_user_id = user_id
        self.token = token
        self.selector = DefaultSelector()
        self.client = Client(password=password)
        self.client.connect((host, port))
        self.client.setblocking(False)
        self.client.register_to_selector(self.selector)
        self._job = None

    def update(self):
        while self.selector.get_map():
            events = self.selector.select()
            for key, mask in events:
                callback = key.data
                callback(key.fileobj, mask)

    def register_job(self, scheduler):
        self._job = scheduler.add_job(f"updater#{self.token}", self.update)

    def close(self):
        self._job.remove()
        self.client.close()


class SessionManager:
    def __init__(self, app, scheduler):
        self.host = app.config["OTTD_HOST"]
        self.port = app.config["OTTD_PORT"]
        self.password = app.config["OTTD_PASSWORD"]
        self.sessions = []
        self.scheduler = scheduler

    def new_session(self, u):
        token_string = f"{u.id}:{u.password}:{time.time()}"
        token = hashlib.sha256(token_string.encode("utf-8")).hexdigest()
        session = Session(u.id, token, self.host, self.port, self.password)
        session.register_job(self.scheduler)
        self.sessions.append(session)
        return session

    def get_session(self, token):
        for s in self.sessions:
            if s.token == token:
                return s
        return None

    def close_session(self, token):
        client = self.get_session(token)
        self.sessions.remove(client)
        client.close()

    def session_required(self, func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            j = request.get_json()
            token = j.get("token")
            if not token:
                return jsonify({"result": False, "message": "token_not_passed"})
            session = self.get_session(token)
            if not session:
                return jsonify({"result": False, "message": "session_not_active"})
            return func(session, *args, **kwargs)
        return wrapper
