import os
import time
from typing import Callable, NoReturn
import json

import requests

from nacl.exceptions import BadSignatureError
from nacl.signing import VerifyKey

from deta_discord_interactions.models.option import Option

from deta_discord_interactions.command import Command, SlashCommandGroup
from deta_discord_interactions.context import Context, ApplicationCommandType
from deta_discord_interactions.models import Message, Modal, ResponseType, Permission


class AbortError(Exception):
    def __init__(self, http_code):
        self.http_code = http_code

class PongResponse:
    def encode(self):
        return json.dumps({"type": ResponseType.PONG}).encode('UTF-8'), "application/json"


class InteractionType:
    PING = 1
    APPLICATION_COMMAND = 2
    MESSAGE_COMPONENT = 3
    APPLICATION_COMMAND_AUTOCOMPLETE = 4
    MODAL_SUBMIT = 5


class DiscordInteractionsBlueprint:
    """
    Represents a collection of :class:`ApplicationCommand` s.

    Useful for splitting a bot across multiple files.
    """

    def __init__(self):
        self.discord_commands: dict[str, Command] = {}
        self.custom_id_handlers: dict[str, Callable] = {}
        self.deta_actions: dict[str, Callable] = {}

    def add_command(
        self,
        command: Callable,
        name: str = None,
        description: str = None,
        *,
        options: list[Option] = None,
        annotations: dict[str, str] = None,
        type: int = ApplicationCommandType.CHAT_INPUT,
        default_member_permissions: int = None,
        dm_permission: bool = None,
        name_localizations: dict[str, str] = None,
        description_localizations: dict[str, str] = None,
    ):
        """
        Create and add a new :class:`ApplicationCommand`.

        Parameters
        ----------
        command: Callable
            Function to execute when the command is run.
        name: str
            The name of the command, as displayed in the Discord client.
        name_localizations: dict[str, str]
            A dictionary of localizations for the name of the command.
        description: str
            The description of the command.
        description_localizations: dict[str, str]
            A dictionary of localizations for the description of the command.
        options: list[Option]
            A list of options for the command, overriding the function's
            keyword arguments.
        annotations: dict[str, str]
            If ``options`` is not provided, descriptions for each of the
            options defined in the function's keyword arguments.
        type: int
            The class:`.ApplicationCommandType` of the command.
        default_member_permissions: int
            A permission integer defining the required permissions a user must have to run the command.
        dm_permission: bool
            Indicates whether the command can be used in DMs.
        """
        command = Command(
            command=command,
            name=name,
            description=description,
            options=options,
            annotations=annotations,
            type=type,
            default_member_permissions=default_member_permissions,
            dm_permission=dm_permission,
            name_localizations=name_localizations,
            description_localizations=description_localizations,
            discord=self,
        )
        self.discord_commands[command.name] = command
        return command

    def command(
        self,
        name: str = None,
        description: str = None,
        *,
        options: list[Option] = None,
        annotations: dict[str, str] = None,
        type: int = ApplicationCommandType.CHAT_INPUT,
        default_member_permissions: int = None,
        dm_permission: bool = None,
        name_localizations: dict[str, str] = None,
        description_localizations: dict[str, str] = None,
    ) -> Callable[[Callable], Command]:
        """
        Decorator to create a new :class:`Command`.

        Parameters
        ----------
        name: str
            The name of the command, as displayed in the Discord client.
        name_localizations: dict[str, str]
            A dictionary of localizations for the name of the command.
        description: str
            The description of the command.
        description_localizations: dict[str, str]
            A dictionary of localizations for the description of the command.
        options: list[Option]
            A list of options for the command, overriding the function's
            keyword arguments.
        annotations: dict[str, str]
            If ``options`` is not provided, descriptions for each of the
            options defined in the function's keyword arguments.
        type: int
            The ``ApplicationCommandType`` of the command.
        default_member_permissions: int
            A permission integer defining the required permissions a user must have to run the command
        dm_permission: bool
            Indicates whether the command can be used in DMs

        Returns
        -------
        Callable[Callable, Command]
        """

        def decorator(func):
            nonlocal name, description, type, options
            command = self.add_command(
                func,
                name=name,
                description=description,
                options=options,
                annotations=annotations,
                type=type,
                default_member_permissions=default_member_permissions,
                dm_permission=dm_permission,
                name_localizations=name_localizations,
                description_localizations=description_localizations,
            )
            return command

        return decorator

    def action(self, action_id: str):
        """
        Decorator to add a new Deta (Scheduled) Action.
        You must remember to register it in the Spacefile for it to run.
        """
        def decorator(func):
            self.deta_actions[action_id] = func
            return func
        return decorator

    def command_group(
        self,
        name: str,
        description: str = "No description",
        *,
        default_member_permissions: int = None,
        dm_permission: bool = None,
        name_localizations: dict[str, str] = None,
        description_localizations: dict[str, str] = None,
    ):
        """
        Create a new :class:`SlashCommandGroup`
        (which can contain multiple subcommands)

        Parameters
        ----------
        name: str
            The name of the command group, as displayed in the Discord client.
        name_localizations: dict[str, str]
            A dictionary of localizations for the name of the command group.
        description: str
            The description of the command group.
        description_localizations: dict[str, str]
            A dictionary of localizations for the description of the command group.
        default_member_permissions: int
            A permission integer defining the required permissions a user must have to run the command
        dm_permission: bool
            Indicates whether the command can be used in DMs

        Returns
        -------
        SlashCommandGroup
            The newly created command group.
        """

        group = SlashCommandGroup(
            name=name,
            description=description,
            default_member_permissions=default_member_permissions,
            dm_permission=dm_permission,
            name_localizations=name_localizations,
            description_localizations=description_localizations,
        )
        self.discord_commands[name] = group
        return group

    def add_custom_handler(self, handler: Callable, custom_id: str):
        """
        Add a handler for an incoming interaction with the specified custom ID.

        Parameters
        ----------
        handler: Callable
            The function to call to handle the incoming interaction.
        custom_id: str
            The custom ID to respond to.

        Returns
        -------
        str
            The custom ID that the handler will respond to.
        """
        self.custom_id_handlers[custom_id] = handler
        return custom_id

    def custom_handler(self, custom_id: str):
        """
        Returns a decorator to register a handler for a custom ID.

        Parameters
        ----------
        custom_id
            The custom ID to respond to.

        Returns
        -------
        Callable[Callable, str]
        """

        def decorator(func):
            nonlocal custom_id
            custom_id = self.add_custom_handler(func, custom_id)
            return custom_id

        return decorator


class DiscordInteractions(DiscordInteractionsBlueprint):
    """
    Handles registering a collection of :class:`Command` s, receiving
    incoming interaction data, and sending/editing/deleting messages via
    webhook.
    """
    DISCORD_BASE_URL = "https://discord.com/api/v10"

    def __init__(self):
        super().__init__()
        self.discord_token = None
        try:
            self.discord_client_id = os.environ["DISCORD_CLIENT_ID"]
            self.discord_public_key = os.environ["DISCORD_PUBLIC_KEY"]
            self.discord_client_secret = os.environ["DISCORD_CLIENT_SECRET"]
            self.discord_scope = os.getenv("DISCORD_SCOPE", "applications.commands.update")
            self.DONT_REGISTER_WITH_DISCORD = os.getenv("DONT_REGISTER_WITH_DISCORD", False)
            self.DONT_VALIDATE_SIGNATURE = os.getenv("DONT_VALIDATE_SIGNATURE", False)
        except KeyError:
            raise Exception("Please fill in the .env files with your application's credentials.")
        self.__routes = {}

    def fetch_token(self):
        """
        Fetch an OAuth2 token from Discord using the ``CLIENT_ID`` and
        ``CLIENT_SECRET`` with the ``applications.commands.update`` scope. This
        can be used to register new application commands.
        """
        if self.DONT_REGISTER_WITH_DISCORD:
            discord_token = {
                "token_type": "Bearer",
                "scope": self.discord_scope,
                "expires_in": 604800,
                "access_token": "DONT_REGISTER_WITH_DISCORD",
            }
            discord_token["expires_on"] = (
                time.time() + discord_token["expires_in"] / 2
            )
            return discord_token

        response = requests.post(
            self.DISCORD_BASE_URL + "/oauth2/token",
            data={
                "grant_type": "client_credentials",
                "scope": self.discord_scope,
            },
            headers={"Content-Type": "application/x-www-form-urlencoded"},
            auth=(self.discord_client_id, self.discord_client_secret),
        )

        response.raise_for_status()
        discord_token = response.json()
        discord_token["expires_on"] = (
            time.time() + discord_token["expires_in"] / 2
        )
        return discord_token

    def auth_headers(self):
        """
        Get the Authorization header required for HTTP requests to the
        Discord API.

        Returns
        -------
        dict[str, str]
            The Authorization header.
        """
        if self.discord_token is None or time.time() > self.discord_token["expires_on"]:
            self.discord_token = self.fetch_token()
        return {"Authorization": f"Bearer {self.discord_token['access_token']}"}

    def update_commands(self, guild_id: str = None, *, from_inside_a_micro: bool = False):
        """
        Update the list of commands registered with Discord.
        This method will overwrite all existing commands.

        Parameters
        ----------
        guild_id: str
            The ID of the Discord guild to register commands to. If omitted,
            the commands are registered globally.
        from_inside_a_micro: bool
            If you really want to update the commands from inside the micro, set this to True.
            I would strongly advise against it though - at least, do not run this *every time* but from a specific command or route
        """
        # It *would* work, it's just a big waste and may slow down the bot overall
        if (os.getenv("DETA_SPACE_APP") is not None) and (from_inside_a_micro == False):
            raise Exception("Cannot register commands from inside a Deta Micro")

        if guild_id:
            url = (
                f"{self.DISCORD_BASE_URL}/applications/"
                f"{self.discord_client_id}/"
                f"guilds/{guild_id}/commands"
            )
        else:
            url = (
                f"{self.DISCORD_BASE_URL}/applications/"
                f"{self.discord_client_id}/commands"
            )

        overwrite_data = [command.dump() for command in self.discord_commands.values()]

        if not self.DONT_REGISTER_WITH_DISCORD:
            response = requests.put(
                url, json=overwrite_data, headers=self.auth_headers()
            )

            try:
                response.raise_for_status()
            except requests.exceptions.HTTPError:
                raise ValueError(
                    f"Unable to register commands:"
                    f"{response.status_code} {response.text}"
                )

            for command in response.json():
                if command["name"] in self.discord_commands:
                    self.discord_commands[command["name"]].id = command["id"]
        else:
            for command in self.discord_commands.values():
                command.id = command.name

    def build_permission_overwrite_url(
        self,
        command: Command = None,
        *,
        guild_id: str,
        command_id: str = None,
    ):
        """
        Build the URL for getting or setting permission overwrites for a
        specific guild and command.
        """
        if command_id is None:
            if command:
                command_id = command.id
            else:
                raise ValueError(
                    "You must supply either a command ID or a Command instance."
                )

        url = f"{self.DISCORD_BASE_URL}/applications/{self.discord_client_id}/guilds/{guild_id}/commands/{command_id}/permissions"

        return url

    def get_permission_overwrites(
        self,
        command: Command = None,
        *,
        guild_id: str,
        command_id: str = None,
    ):
        """
        Get the list of permission overwrites in a specific guild for a
        specific command.

        Parameters
        ----------
        command: Command
            The :class:`.Command` to retrieve permissions for.
        guild_id: str
            The ID of the guild to retrieve permissions from.
        command_id: str
            The ID of the command to retrieve permissions for.

        Returns
        -------
        list[Permission]
            A list of permission overwrites for the given command.
        """

        url = self.build_permission_overwrite_url(
            command,
            guild_id=guild_id,
            command_id=command_id,
        )

        response = requests.get(
            url,
            headers=self.auth_headers(),
        )
        response.raise_for_status()

        return [Permission.from_dict(perm) for perm in response.json()]

    def set_permission_overwrites(
        self,
        permissions: list[Permission],
        command: Command = None,
        *,
        guild_id: str,
        command_id: str = None,
    ):
        """
        Overwrite the list of permission overwrites in a specific guild for a
        specific command.

        Parameters
        ----------
        command: Command
            The :class:`.Command` to retrieve permissions for.
        guild_id: str
            The ID of the guild to retrieve permissions from.
        command_id: str
            The ID of the command to retrieve permissions for.
        """

        url = self.build_permission_overwrite_url(
            command,
            guild_id=guild_id,
            command_id=command_id,
        )

        response = requests.put(
            url,
            headers=self.auth_headers(),
            json={"permissions": [perm.dump() for perm in permissions]},
        )
        response.raise_for_status()


    def register_blueprint(self, blueprint: DiscordInteractionsBlueprint):
        """
        Register a :class:`DiscordInteractionsBlueprint` to this
        DiscordInteractions class. Updates this instance's list of
        :class:`Command` s using the blueprint's list of
        :class:`Command` s.

        Parameters
        ----------
        blueprint: DiscordInteractionsBlueprint
            The :class:`DiscordInteractionsBlueprint` to add
            :class:`Command` s from.
        """
        self.discord_commands.update(blueprint.discord_commands)
        self.custom_id_handlers.update(blueprint.custom_id_handlers)
        self.deta_actions.update(blueprint.deta_actions)

    def run_command(self, data: dict):
        """
        Run the corresponding :class:`Command` given incoming interaction
        data.

        Parameters
        ----------
        data
            Incoming interaction data.

        Returns
        -------
        Message
            The resulting message from the command.
        """

        command_name = data["data"]["name"]

        command = self.discord_commands.get(command_name)

        if command is None:
            raise ValueError(f"Invalid command name: {command_name}")

        return command.make_context_and_run(discord=self, data=data)

    def run_handler(self, data: dict, *, allow_modal: bool = True):
        """
        Run the corresponding custom ID handler given incoming interaction
        data.

        Parameters
        ----------
        data
            Incoming interaction data.

        Returns
        -------
        Message
            The resulting message.
        """

        context = Context.from_data(self, data)
        handler = self.custom_id_handlers[context.primary_id]
        args = context.create_handler_args(handler)
        result = handler(context, *args)

        if isinstance(result, Modal):
            if allow_modal:
                return result
            else:
                raise ValueError("Cannot return a Modal to that interaction type.")

        return Message.from_return_value(result)

    def run_autocomplete(self, data: dict):
        """
        Run the corresponding command's autocomplete handler given incoming 
        interaction data.

        Parameters
        ----------
        data
            Incoming interaction data.

        Returns
        -------
        AutocompleteResult
            The result of the autocomplete handler.
        """

        command_name = data["data"]["name"]

        command = self.discord_commands[command_name]

        return command.make_context_and_run_autocomplete(discord=self, data=data)

    def run_deta_action(self, event: dict[str, str]):
        """Runs registered Deta Actions"""
        action = self.deta_actions.get(event.get("id"))
        if action is None:
            self.abort(400, f"Deta event tried to run an unregistered action: {event!r}")
        else:
            return action(event)

    def verify_signature(self, request):
        """
        Verify the signature sent by Discord with incoming interactions.

        Parameters
        ----------
        request
            The request to verify the signature of.
        """
        signature = request.get("HTTP_X_SIGNATURE_ED25519")
        timestamp = request.get("HTTP_X_SIGNATURE_TIMESTAMP")

        if self.DONT_VALIDATE_SIGNATURE:
            return

        if signature is None or timestamp is None:
            self.abort(401, "Missing signature or timestamp")

        message = f"{timestamp}{request['raw_data'].decode('UTF-8')}".encode("UTF-8")
        verify_key = VerifyKey(bytes.fromhex(self.discord_public_key))
        try:
            verify_key.verify(message, bytes.fromhex(signature))
        except BadSignatureError:
            try:
                body = (
                    json.dumps(
                        json.loads(
                            request['raw_data'].decode('UTF-8')
                        ),
                        separators=(',', ':'),
                    )
                    .encode('UTF-8')
                )
                message = f"{timestamp}{body}".encode("UTF-8")
                verify_key.verify(message, bytes.fromhex(signature))
            except BadSignatureError:
                self.abort(401, "Incorrect Signature")
            else:
                import warnings
                warnings.warn("The whitespace for the request data may have been modified before being sent to discord-interactions")

    def handle_interaction(self, request: dict):
        """
        Verify the signature in the incoming request and return the
        result from the corresponding handler.

        Returns
        -------
        Message | Modal | AutocompleteResult
            The response from the corresponding handler.
        """
        self.verify_signature(request)

        interaction_type = request["json"].get("type")
        if interaction_type == InteractionType.PING:
            return PongResponse()
        elif interaction_type == InteractionType.APPLICATION_COMMAND:
            return self.run_command(request["json"])
        elif interaction_type == InteractionType.MESSAGE_COMPONENT:
            return self.run_handler(request["json"])
        elif interaction_type == InteractionType.APPLICATION_COMMAND_AUTOCOMPLETE:
            return self.run_autocomplete(request["json"])
        elif interaction_type == InteractionType.MODAL_SUBMIT:
            return self.run_handler(request["json"], allow_modal=False)
        else:
            raise RuntimeWarning(
                f"Interaction type {interaction_type} is not yet supported"
            )
    
    def route(self, route_path: str):
        """Decorator to register a custom route.
        Used internally for Webhooks OAuth, but for most purposes,
        I would recommend to use another Micro with FastAPI or Flask instead.

        Example usage:
        @app.route('/')
        def home(request, start_response, abort):
            start_response('200 OK', [])
            return ['Hello World!'.encode('UTF-8')]
        """
        def decorator(function):
            self.__routes[route_path] = function
            return function
        return decorator

    def __call__(self, environ: dict, start_response: Callable):
        """
        Handles incoming interaction data
        (WSGI)
        """
        try:
            data = environ.copy()
            raw_data = environ["wsgi.input"].read()
            if raw_data:
                data["json"] = json.loads(raw_data.decode("UTF-8"))
                data["raw_data"] = raw_data

            data["path"] = data.get("PATH_INFO", '').split("?", 1)[0] or '/'


            if data["QUERY_STRING"]:
                data["query_dict"] = dict(args.split('=', 1) for args in data["QUERY_STRING"].split("&"))
            else:
                data["query_dict"] = {}
            ### Handle Discord
            if data['path'] == '/discord':
                result = self.handle_interaction(data)
                response, mimetype = result.encode()
                status = "200 OK"
                response_headers = [("Content-Type", mimetype)]
                start_response(status, response_headers)
                return [response]
            ### Catch a common mistake
            elif (  # If you set it like `https://example.deta.app` instead of `https://example.deta.app/discord`
                data['path'] == '/' 
                and '/' not in self.__routes 
                and "Discord-Interactions" in data.get("HTTP_USER_AGENT")
                and self.verify_signature(data)
            ):
                raise Exception("Please set the path to `.../discord` on the Developer Portal, not just the Micro URL")
            ### Deta special routes
            elif data['path'] == "/__space/v0/actions":
                event = data.get("json", {}).get("event")
                if event is None:
                    self.abort(400, 'Malformated deta space event')
                result = self.run_deta_action(event)
                if result:
                    start_response("200 OK", [("Content-Type", "application/json")])
                    return [json.dumps({"result": result}).encode("UTF-8")]
                else:
                    start_response('200 OK', [])
                    return []
            ### User defined routes (including Utils such as oauth)
            elif data['path'] in self.__routes:
                return self.__routes[data['path']](data, start_response, self.abort)
            ### Unexpected route
            else:
                self.abort(404, 'Page not found')
        except AbortError as err:
            status = err.http_code
            response_headers = [("Content-Type", "application/json")]
            start_response(status, response_headers)
            return [json.dumps({"error": status}).encode("UTF-8")]
        except Exception as err:
            import traceback
            traceback.print_exc()
            print(f"Unexpected error: {err}", flush=True)
            start_response('500 Internal Server Error', [("Content-Type", "application/json")])
            return [json.dumps({"error": str(type(err))}).encode("UTF-8")]

    def abort(self, code: int, reason: str) -> NoReturn:
        raise AbortError(f"{code} {reason}")
