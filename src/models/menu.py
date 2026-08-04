from dataclasses import dataclass
from collections.abc import Callable

from models.video import VideoContext
from pipelines import (
    cut_video_pipeline, 
    speed_up_video_pipeline, 
    video_to_gif_pipeline
)


@dataclass(frozen=True)
class MenuItem:
    key: str
    title: str
    action: Callable[[VideoContext], None] | None
    

MENU_ITEMS: dict[str, MenuItem] = {
    "1": MenuItem("1", "Cut Video", cut_video_pipeline),
    "2": MenuItem("2", "Convert to GIF", video_to_gif_pipeline),
    "3": MenuItem("3", "Speed Up Video", speed_up_video_pipeline),
    "4": MenuItem("4", "Exit", None),
}


def display_menu() -> None:
    """Display all available menu options."""
    print("\n===== Video Editor =====")

    for item in MENU_ITEMS.values():
        print(f"{item.key}. {item.title}")


    
def execute_choice(choice: str, video: VideoContext) -> bool:
    """
    Executes the selected menu option.

    Returns:
        True  -> Continue running the application.
        False -> Exit the application.
    """
    item = MENU_ITEMS.get(choice)

    if item is None:
        print("Invalid option.")
        return True

    if item.action is None:
        print("Goodbye!")
        return False

    item.action(video)
    return True