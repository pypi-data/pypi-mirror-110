"""This script enables cancellation of all currently running skills."""
from typing import Callable


def cancel_skills(misty: Callable):
    """Cancels all skills currently running on Misty."""
    data = misty.get_info("skills_running")
    result = data.get("result", [])
    to_cancel = []
    for dct in result:
        uid = dct.get("uniqueId", "")
        if len(uid) > 0:
            to_cancel.append(uid)
    for skill in to_cancel:
        misty.perform_action("skill_cancel", data={"Skill": skill})
