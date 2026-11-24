from functools import cache
from pathlib import Path
import yaml
from app.config import Config

PROMPTS_FILE_PATH = Config.PARENT_FOLDER_PATH / "prompts" / "prompts.yaml"


@cache
def __load_prompts() -> dict:
    """
    This function loads all the prompts from prompts.yaml only once.

    Parameters
    ----------
    None

    Returns
    -------
    prompts: dict
        This is dict of all prompts present in prompts.yaml.
    """
    with Path.open(PROMPTS_FILE_PATH, mode="r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def __get_prompt(name: str, **placeholders) -> str:
    """
    This function gets the prompt from prompts.yaml and fills its placeholders.
    Ex:
    __get_prompt("reactive_agent.system", skills="- apple: Deploys apple.")

    Parameters
    ----------
    name: str
        This is dotted path of prompt in prompts.yaml like "guardrail.user".
    placeholders:
        This are values for {placeholders} present in the prompt.

    Returns
    -------
    prompt: str
        This is prompt with all placeholders filled.
    """
    prompt = __load_prompts()
    for key in name.split("."):
        prompt = prompt[key]
    return prompt.format(**placeholders)
