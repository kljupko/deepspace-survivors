"""A module containing project-wide helper functions."""

from typing import Iterable

from pathlib import Path
import pygame

from . import config

def load_image(filename: str | None = None,
               dflt_color: str = "pink",
               dflt_size: tuple[int, int] = (24, 24)
               ) -> pygame.Surface:
    """
    Returns an image with the given name from the images directory.
    If the file name is not provided or the image cannot be loaded,
    returns a rectangle by default of the given color and size (w, h).
    """

    default = pygame.Surface(dflt_size)
    pygame.draw.rect(default, dflt_color, default.get_rect())

    if filename is None:
        return default

    path = Path(config.images_path, filename)

    if not path.exists():
        print(f"Image not found at: {path}.")
        print("Returning with default.")
        return default
    
    try:
        img = pygame.image.load(path)
        img.convert_alpha()
        return img
    except Exception as e:
        print(f"Error while loading image!\n{e}")
        print("Returning with default.")
        return default

def copy_image(surface: pygame.Surface) -> pygame.Surface:
    """Return an identical copy of the given image (surface)."""

    image = pygame.Surface(surface.get_size())
    image.blit(surface, surface.get_rect())
    return image

def shorten_number(number: int) -> str:
    """Returnes a shortened number, so 1,200 becomes 1.2K."""

    if number < 1000:
        return str(number)
    
    n = number / 1000
    return f"{n:.2f}K"

def cycle_values[T](
        current_value: T, values: Iterable[T]
        ) -> T | None:

    if not values:
        return None
    
    first_value = None
    reached_current = False


    for value in values:
        if first_value is None:
            first_value = value
        if value == current_value:
            reached_current = True
            continue
        if reached_current:
            return value
    
    return first_value
