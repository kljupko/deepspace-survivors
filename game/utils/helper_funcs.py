"""A module containing project-wide helper functions."""

from pathlib import Path
import pygame

from . import config

def load_image(filename=None, dflt_color="pink", dflt_size=(24, 24)):
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