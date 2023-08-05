from typing import List, Optional

from pydantic import BaseModel, validator


class RequestDestination(BaseModel):
    """A super-class for classes representing a Sym Request Destination."""

    allow_self: bool = False
    """A boolean indicating whether or not the requestor may approve this request"""

    timeout: Optional[int] = None
    """An optional integer representing the duration until this request will expire, in seconds"""


class SlackChannelID(RequestDestination):
    """A Request to be sent to a Slack Channel, identified by a Slack Channel ID"""

    channel_id: str

    @validator("channel_id")
    def validate_channel_id_format(cls, value):
        value = value.strip()

        if not value:
            raise ValueError("channel_id must be non-empty")

        if not value[0] in {"C", "D", "G"}:
            raise ValueError(
                f"{value} is not a valid Slack Channel ID. Channel IDs must start with one of 'C', 'D', or 'G'."
            )

        return value

    def __str__(self):
        return f"SlackChannelID '{self.channel_id}'"


class SlackChannelName(RequestDestination):
    channel_name: str

    def __str__(self):
        return f"SlackChannelName '{self.channel_name}'"

    @validator("channel_name")
    def validate_channel_name_format(cls, value):
        value = value.strip()

        if not value:
            raise ValueError("channel_name must be non-empty")

        return value


class SlackUser(RequestDestination):
    user_id: str

    @validator("user_id")
    def validate_user_id_format(cls, value):
        value = value.strip()

        if not value:
            raise ValueError("user_id must be non-empty")

        if not value.startswith("U"):
            raise ValueError(
                f"{value} is not a valid Slack User ID. Slack User IDs must start with 'U'."
            )

        return value

    def mention(self):
        return f"<@{self.user_id}>"

    def __str__(self):
        return f"SlackUser '{self.user_id}'"


class SlackUserGroup(RequestDestination):
    users: List[SlackUser]

    @validator("users")
    def validate_users_list(cls, value):
        if not value:
            raise ValueError("users must be a non-empty list")

        if len(value) > 7:
            raise ValueError("A Slack User Group maybe only contain a maximum of 7 users.")

        return value

    def __str__(self):
        user_ids = [user.user_id for user in self.users]
        return f"SlackUserGroup '{user_ids}'"


class RequestDestinationFallback(BaseModel):
    """A list of RequestDestinations to attempt to send requests to. The next RequestDestination will be attempted
    based on the failure mode configuration.
    """

    destinations: List[RequestDestination]
    continue_on_delivery_failure: bool
    # continue_on_timeout: bool  # TODO: To be implemented as part of backup approvers
