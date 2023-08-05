import pytest

from sym.sdk import SlackChannelID


class TestRequestDestination:
    def test_slack_channel_id(self):
        assert SlackChannelID(channel_id="C12345").channel_id == "C12345"
        assert SlackChannelID(channel_id="D12345").channel_id == "D12345"
        assert SlackChannelID(channel_id="G12345").channel_id == "G12345"
        assert SlackChannelID(channel_id="  C12345 ").channel_id == "C12345"

    @pytest.mark.parametrize(
        "channel_id, match_error",
        [
            ("", "must be non-empty"),
            (" ", "must be non-empty"),
            ("X123", "not a valid Slack Channel ID"),
        ],
    )
    def test_slack_channel_id_errors(self, channel_id, match_error):
        with pytest.raises(ValueError, match=match_error):
            SlackChannelID(channel_id=channel_id)

    # TODO: Remaining unit tests
