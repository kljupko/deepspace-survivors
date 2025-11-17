"""A module containing the classes for the top and bottom tray."""

from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from ..game import Game

from .base import Tray
from .menu_setups import build_top_tray_elements, build_bot_tray_elements
from .menu_setups import build_bot_tray_unions

class TopTray(Tray):
    """A class representing the top tray."""

    name: str = "Top Tray"
    height: int = 23

    def __init__(self, game: Game) -> None:
        """Initialize the top tray."""

        name = TopTray.name
        height = TopTray.height
        super().__init__(game, name, height=height)
    
    def _load_elements(self) -> None:
        """Populate the tray with UI Elements."""

        self._add_elements_from_dicts(build_top_tray_elements(self))
        # no need to call self._expand_height
    
    def get_session_duration(self) -> str:
        """Return the duration of the current session."""

        duration = self.game.state.session_duration

        mins, secs = divmod(duration // 1000, 60)
        hours, mins = divmod(mins, 60)
        time = f"{mins:02d}:{secs:02d}"
        if hours > 0:
            time = f"{hours:02d}:" + time
        
        return time

    def get_fps(self) -> str:
        """Return the fps if 'show_fps' setting is True. Else blank."""
        fps = ""
        if self.game.settings.data['show_fps']:
            fps = str(self.game.fps)
        return fps

class BottomTray(Tray):
    """A class representing the bottom tray."""

    name: str = "Bottom Tray"

    def __init__(self, game: Game) -> None:
        """Initialize the bottom tray."""

        name = BottomTray.name
        height = game.screen.height - game.play_surf.height + 11

        super().__init__(game, name, height=height)
        self.rect.y = self.game.screen.height - self.rect.height
    
    def _load_elements(self) -> None:
        """Populate the tray with UI Elements"""

        self._add_elements_from_dicts(build_bot_tray_elements(self))
        # no need to call self._expand_height

        self._add_element_unions_from_dicts(build_bot_tray_unions(self))
