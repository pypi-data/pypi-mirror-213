"""Terminal widgets."""
from typing import TypeVar

from readchar import config, key, readkey

from aws_ecs_exec.colors import colored, colorise

# Use ctrl+d as an interrupt key too
config.INTERRUPT_KEYS += [key.CTRL_D]

UP = [key.UP, "k"]  # Support vim style binding
DOWN = [key.DOWN, "j"]  # Support vim style binding
CONFIRM = [key.ENTER]
TOP = ["g"]
BOTTOM = ["G"]


ESCSEQ = "\033["


def replace_line(text):
    """Replace the current line with the given text."""
    print(f"{ESCSEQ}K{text}")


def move_up(lines=1):
    """Move the cursor up the specified number of lines."""
    print(f"{ESCSEQ}{lines}A")


_T = TypeVar("_T")


def select(
    message: str, choices: list[tuple[_T, str]], default_selected_index: int = 0
) -> _T:
    """Select an option from a list."""
    unselected_option = colorise("<b>[ ]</b> ")
    selected_option = colorise("<b>[<g>x</g>]</b> ")
    message_prefix = colorise("<b>[<y>?</y>]</b> ")
    choice_message_prefix = colorise("<b><y>Choice:</y></b> ")

    num_options = len(choices)

    assert default_selected_index < num_options, (
        "The default selected index is greater than the number of "
        f"choices. Default: '{default_selected_index}', Number of "
        f"options: '{num_options}'."
    )

    selected_index = default_selected_index

    print(f"{message_prefix}{message}")
    print("\n" * (num_options - 1))
    previous_keypress = None
    while True:
        move_up(num_options + 1)
        for idx, option in enumerate(choices):
            prefix = selected_option if idx == selected_index else unselected_option
            replace_line(f"{prefix}{option[1]}")
        keypress = readkey()
        if keypress in TOP and previous_keypress in TOP:
            selected_index = 0
        if keypress in BOTTOM:
            selected_index = num_options - 1
        if keypress in UP:
            selected_index = max(0, min(selected_index - 1, num_options - 1))
        elif keypress in DOWN:
            selected_index = max(0, min(selected_index + 1, num_options - 1))
        elif keypress in CONFIRM:
            break
        previous_keypress = keypress
    print(f"{choice_message_prefix}'{choices[selected_index][1]}'\n")
    return choices[selected_index][0]


def confirm(message: str, default=True) -> bool:
    """Prompt the user to input yes or no."""
    answer = default
    yes_value = "y"
    no_value = "n"
    yesno_text: str
    if default:
        yesno_text = f"{yes_value.upper()}{no_value}"
    else:
        yesno_text = f"{yes_value}{no_value.upper()}"
    question = f"{colored(message, bold=True)} ({yesno_text}): "
    break_keys = set(CONFIRM + [yes_value, no_value])

    print(question, end="", flush=True)

    keypress: str
    while True:
        keypress = readkey()
        answer_raw = keypress.lower()
        if answer_raw == yes_value:
            answer = True
        elif answer_raw == no_value:
            answer = False
        if answer_raw in break_keys:
            break

    move_up()
    replace_line(f"{question}{keypress}\n")
    return answer
