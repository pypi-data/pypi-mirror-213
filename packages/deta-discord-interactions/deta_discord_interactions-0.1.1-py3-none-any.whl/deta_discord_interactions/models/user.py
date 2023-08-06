import dataclasses
from datetime import datetime
from typing import Optional

from deta_discord_interactions.models.utils import LoadableDataclass


@dataclasses.dataclass
class User(LoadableDataclass):
    """
    Represents a User (the identity of a Discord user, not tied to any
    specific guild).

    Attributes
    ----------
    id
        The ID (snowflake) of the user.
    username
        The Discord username of the user.
    discriminator
        The code following the # after the username.
    avatar_hash
        The unique hash identifying the profile picture of the user.
    bot
        Whether the user is a bot account.
    system
        Whether the user is a Discord system account.
    mfa_enabled
        Whether the user has enabled Two-Factor Authentication.
    banner
        The unique hash identifying the banner of the user.
    accent_color
        The user's banner color encoded as an integer representation of hexadecimal color code
    locale
        The locale of the user.
    verified
        Whenever the user has verified their email. Only available via OAuth with email scope.
    email
        The user's email. Only available via OAuth with email scope.
    flags
        Miscellaneous information about the user.
    premium_type
        The Nitro status of the user.
    public_flags
        Miscellaneous information about the user.
    """

    id: str = None
    username: str = None
    discriminator: str = None
    avatar_hash: str = None
    # avatar_decoration: str = None
    bot: bool = None
    system: bool = None
    mfa_enabled: bool = None
    # banner: str = None
    # banner_color: str = None
    # accent_color: str = None
    locale: str = None
    verified: bool = None  # Only available via OAuth with email scope
    email: str = None  # Only available via OAuth with email scope
    flags: int = None
    premium_type: int = None
    public_flags: Optional[int] = None

    @classmethod
    def from_dict(cls, data):
        data = {**data, **data.get("user", {})}
        data["avatar_hash"] = data.get("avatar")
        return super().from_dict(data)

    @property
    def display_name(self):
        """
        The displayed name of the user (the username).

        Returns
        -------
        str
            The displayed name of the user.
        """
        return self.username

    @property
    def avatar_url(self):
        """
        The URL of the user's profile picture.

        Returns
        -------
        str
            The URL of the user's profile picture.
        """
        if self.avatar_hash is None:
            return f"https://cdn.discordapp.com/embed/avatars/{int(self.discriminator) % 5}.png"
        elif str(self.avatar_hash).startswith("a_"):
            return (
                f"https://cdn.discordapp.com/avatars/{self.id}/{self.avatar_hash}.gif"
            )
        else:
            return (
                f"https://cdn.discordapp.com/avatars/{self.id}/{self.avatar_hash}.png"
            )


@dataclasses.dataclass
class Member(User):
    """
    Represents a Member (a specific Discord :class:`User` in one particular
    guild.)

    Attributes
    ----------
    nick
        The guild nickname of the user.
    roles
        An array of role IDs that the user has.
    joined_at
        The timestamp that the user joined the guild at.
    premium_since
        The timestamp that the user started Nitro boosting the guild at.
    permissions
        The permissions integer of the user.
    deaf
        Whether the user has been server deafened.
    mute
        Whether the user has been server muted.
    pending
        Whether the user has passed the membership requirements of a guild.
    communication_disabled_until
        Timestamp when the member's timeout will expire (if existing)
    """

    pending: Optional[bool] = None
    nick: Optional[str] = None
    roles: Optional[list[str]] = None
    permissions: Optional[int] = None
    deaf: bool = False
    mute: bool = False
    joined_at: datetime = None
    premium_since: Optional[datetime] = None
    communication_disabled_until: Optional[datetime] = None

    def __post_init__(self):
        if isinstance(self.permissions, str):
            self.permissions = int(self.permissions)
        if isinstance(self.joined_at, str):
            self.joined_at = datetime.fromisoformat(self.joined_at)
        if isinstance(self.premium_since, str):
            self.premium_since = datetime.fromisoformat(self.premium_since)
        if isinstance(self.communication_disabled_until, str):
            self.communication_disabled_until = datetime.fromisoformat(self.communication_disabled_until)

    @property
    def display_name(self):
        """
        The displayed name of the user (their nickname, or if none exists,
        their username).

        Returns
        -------
        str
            The displayed name of the user.
        """
        return self.nick or self.username
