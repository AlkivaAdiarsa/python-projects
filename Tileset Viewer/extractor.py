import pygame
import os

class Tile:
    """A container class to hold a Pygame Surface and its metadata."""
    def __init__(self, surface, name, source_path, source_rect):
        self.surface = surface
        self.name = name
        self.source_path = source_path
        self.source_rect_source = source_rect
        self.width, self.height = surface.get_size()

def extract_named_tiles(root_folder):
    # ... (Initialization code remains the same)
    tile_dict = {}
    if not pygame.display.get_init():
         pygame.display.init()
         try:
            pygame.display.set_mode((1, 1), pygame.HIDDEN) 
         except pygame.error:
            pass # Keep previous warning for non-graphical environments

    valid_extensions = ('.png', '.jpg', '.jpeg', '.bmp')

    for root, _, files in os.walk(root_folder):
        for filename in files:
            if filename.lower().endswith(valid_extensions):
                path = os.path.join(root, filename)
                try:
                    image = pygame.image.load(path).convert_alpha()
                    w, h = image.get_size()
                    
                    tile_height = h
                    tile_width = h 

                    relative_path = os.path.relpath(path, root_folder)
                    name_base = os.path.splitext(relative_path)[0].replace(os.sep, '/')

                    for y in range(0, h, tile_height):
                        for x in range(0, w, tile_width):
                            if x + tile_width <= w and y + tile_height <= h:
                                row, col = y // tile_height, x // tile_width
                                tile_name = f"{name_base}_{row}_{col}"
                                rect_source = (x, y, tile_width, tile_height)
                                
                                surface = image.subsurface(rect_source).copy()
                                
                                # --- FIXED: Store data in the new Tile object ---
                                new_tile = Tile(surface, tile_name, relative_path, rect_source)
                                tile_dict[tile_name] = new_tile

                except pygame.error as e:
                    print(f"Could not load {path}: {e}")
                    continue
                except IndexError as e:
                    print(f"Path manipulation error with {path}: {e}")
                    continue

    return tile_dict

if __name__ == '__main__':
    # Optional: Test the extractor standalone
    print("Running extractor.py directly for testing.")
    tiles = extract_named_tiles("assets")
    print(f"Found {len(tiles)} tiles.")