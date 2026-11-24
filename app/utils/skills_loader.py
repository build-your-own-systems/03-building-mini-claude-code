from pathlib import Path
from app.config import Config
from app.utils.console import log, RED


def __parse_skill(file: Path) -> tuple[str | None, str | None]:
    """
    This function parse skill name and it's description from SKILLS.md file
    present for given skills like log etc.

    Parameters
    ----------
    file: Path
        The file i.e SKILLS.md.

    Returns
    -------
    skill_name: str | None
        This is skill name for give SKILL.md.
    skill_description: str | None
        This is skill description for give SKILL.md.
    """
    skill_name, skill_description = None, None
    try:
        with Path.open(file, mode="r") as f:
            content = f.readlines()
    except FileExistsError as fe:
        print(fe)
        return skill_name, skill_description

    get_name = False
    get_description = False

    for sk in content:
        if "name:" in sk and not get_name:
            skill_name = sk.split(":")[1].replace("\n", "").strip()
            get_name = True
        if "description:" in sk and get_name:
            skill_description = sk.split(":")[1].replace("\n", "").strip()
            get_description = True

        if get_name and get_description:
            break

    return skill_name, skill_description


def __convert_skills_to_text_form(skills: dict) -> str:
    """
    This convert the skills dictionary in text form to add
    in system prompt.
    Ex:
    You have access to the following skills:

    - apple: Deploys the apple service to production.
    - grape: Runs the grape test suite and reports failures.

    Parameters
    ----------
    skills: dict
        This the dict containing skills name and description.

    Returns
    -------
    skills_str: str
        This is string form of skills.
    """
    skills_str = ""
    for skill_name, skill_description in skills.items():
        skills_str += f"- {skill_name}: {skill_description}\n"
    return skills_str


def __find_claude_skills_path() -> list[Path]:
    """
    This function scan the .claude path in the parent folder.

    Parameters
    ----------
    None

    Returns
    -------
    claude__skills_paths: list[Path]
        Claude path list or empty list of path if no .claude/skills found.
    """
    parent_path = Config.PARENT_FOLDER_PATH
    claude__skills_paths = []
    for path in parent_path.rglob(".claude/skills"):
        if path.is_dir():
            claude__skills_paths.append(path)
    return claude__skills_paths


def __load_skills() -> str:
    """
    This function loads all the skills present in .claude/skills folder
    in the current working directory and pass it to llm.

    Parameters
    ----------
    None

    Returns
    -------
    skills_str: str
        This is string form of skills as follow.
        \nYou have access to the following skills:
            - apple: Deploys the apple service to production.
            - grape: Runs the grape test suite and reports failures.
    """
    # Get the working path of skills
    skills = {}
    try:
        claude_skills_paths = __find_claude_skills_path()

        if claude_skills_paths == Path(""):
            return ""  # Empty skills

        for skills_path in claude_skills_paths:
            for file in skills_path.rglob("SKILL.md"):
                skill_name, skill_description = __parse_skill(file)
                if skill_name and skill_description:
                    skills[skill_name] = skill_description
        skill_str = __convert_skills_to_text_form(skills)
    except Exception as e:
        log(f"Unable to load skills reason {e.__str__()}", RED)
        return ""  # No skills to load due to some issue.
    return skill_str
