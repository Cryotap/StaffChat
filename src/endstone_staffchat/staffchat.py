from endstone.plugin import Plugin
from endstone import ColorFormat
from endstone.command import *
from endstone.event import EventPriority, ServerLoadEvent, event_handler
from endstone.event import PlayerChatEvent
from endstone.event import PlayerQuitEvent
from endstone import Player
from endstone import Server


class StaffChat(Plugin):
    name = "StaffChat"
    version = "0.1.0"
    api_version = "0.4"
    description = "Talk in staff chat!"

    commands = {
        "staffchat": {
            "description": "Set the motd's that the server will shullfe.",
            "usages": ["/staffchat"],
            "aliases": ["sc"],
            "permissions": ["staffchat.use"],
        },
    }

    permissions = {
        "staffchat.use": {
            "description": "Allow users to talk in Staff Chat.",
            "default": "op",
        },
    }

    sc = []
    cf = ColorFormat

    def checksc(self, uname, sc=sc):
        if uname in sc:
            return True

    def remsc(self, uname, sc=sc):
        if uname in sc:
            sc.remove(str(uname))

    def broadcast(self, pl, msg, cf=cf):
        name = pl.name
        mes = f"{cf.MINECOIN_GOLD}{cf.BOLD}[StaffChat]{cf.RESET}{cf.MATERIAL_GOLD} " + name + f"{cf.GOLD} > {cf.YELLOW}" + msg
        Server.broadcast(self.server, mes, "staffchat.use")

    @event_handler
    def leaving(self, event: PlayerQuitEvent):
        player = event.player
        test = player.name
        self.remsc(test)


    @event_handler
    def chat_event(self, event: PlayerChatEvent):
        player = event.player
        test = player.name
        msg = event.message
        if self.checksc(test):
            self.broadcast(player, msg)
            event.cancelled = True


    def on_load(self) -> None:
        self.logger.info("Loaded!")

    def on_enable(self) -> None:
        self.logger.info("Enabled!")
        self.register_events(self)

    def on_disable(self) -> None:
        self.logger.info("Disabled!")

    def on_command(self, sender: CommandSender, command: Command, args: list[str], cf=cf, sc=sc) -> bool:
        if command.name == "staffchat":
            player = sender.as_player()
            if player is not None:
                if sender.name not in sc:
                    sc.append(str(sender.name))
                    sender.send_message(f"{cf.MATERIAL_DIAMOND}" + "All messages will now be sent to staff chat ")
                    return True
                else:
                    sc.remove(str(sender.name))
                    sender.send_message(f"{cf.MATERIAL_REDSTONE}" + "Your messages will no longer be sent to staff chat")
            else:
                sender.send_error_message(f"{cf.MATERIAL_REDSTONE}" + "You must be a player to run this command")
                return False

        return True
