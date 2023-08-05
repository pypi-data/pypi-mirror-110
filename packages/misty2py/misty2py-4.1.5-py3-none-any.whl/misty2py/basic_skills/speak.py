"""The script that enables speech with extended return message.
"""
from typing import Callable, Dict

from misty2py.utils.generators import get_random_string
from misty2py.utils.messages import compose_json_reply


def speak(misty: Callable, utterance: str) -> Dict:
    """Speaks an utterance and returns descriptive message.

    Args:
        utterance (str): The utterance to speak.

    Returns:
        Dict: the response, including the "status" keyword and a "message"
        keyword which contains the utterance spoken.
    """
    result = misty.perform_action(
        "speak",
        data={
            "Text": utterance,
            "UtteranceId": "utterance_" + get_random_string(6)
            },
    )
    return compose_json_reply(
        result,
        success_message="Talking successful. Utterance: `%s`." % utterance,
        fail_message="Talking failed. Utterance: `%s`." % utterance,
    )
