import pygame
import os
import sys
from tkinter import simpledialog
from tkinter import filedialog

# Import the extraction logic (which now includes the Tile class)
try:
    from extractor import extract_named_tiles, Tile # Import the new class
except ImportError:
    print("Error: Could not import 'extractor.py'. Ensure the file exists in the same directory.")
    sys.exit()


def render_text_box(screen, font, lines, mouse_pos, screen_width, screen_height):
    """Helper function to render a semi-transparent text overlay box."""
    PADDING = 5
    # Calculates the bounding box size required for all lines
    
    # --- FIXED LINE: Extract only the width before calling max() ---
    box_width = max(font.size(line)[0] for line in lines) + 2 * PADDING 
    
    box_height = len(lines) * font.get_linesize() + 2 * PADDING
    
    # Position the box slightly offset from the cursor
    pos_x = mouse_pos[0] + 15 # Use tuple indexing
    pos_y = mouse_pos[1] + 15 # Use tuple indexing
    
    # Adjust position if it goes off-screen
    if pos_x + box_width > screen_width:
        pos_x = screen_width - box_width - 5
    if pos_y + box_height > screen_height:
        pos_y = screen_height - box_height - 5
        
    # Draw background (semi-transparent gray)
    s = pygame.Surface((box_width, box_height), pygame.SRCALPHA)
    s.fill((50, 50, 50, 200)) 
    screen.blit(s, (pos_x, pos_y))

    # Draw text
    for i, line in enumerate(lines):
        text_surface = font.render(line, True, (255, 255, 255))
        screen.blit(text_surface, (pos_x + PADDING, pos_y + PADDING + i * font.get_linesize()))

def run_display():
    # --- Configuration ---
    SCREEN_WIDTH, SCREEN_HEIGHT = 640, 364
    SCROLL_SPEED = 30 
    #ASSETS_FOLDER = simpledialog.askstring("folder", "input assets folder").lower()

    # --- Pygame Setup ---
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption(f"TileSet Viewer [Folder not selected]")
    ASSETS_FOLDER = filedialog.askdirectory(title="input assets folder", initialdir=os.getcwd())
    pygame.display.set_caption(f"TileSet Viewer [{ASSETS_FOLDER}]")
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 18) 

    # --- Load Data ---
    if not os.path.exists(ASSETS_FOLDER):
        print(f"Error: '{ASSETS_FOLDER}' folder not found.")
        pygame.quit()
        sys.exit()

    tiles_dict = extract_named_tiles(ASSETS_FOLDER)
    
    if not tiles_dict:
        print("No tiles found. Exiting.")
        pygame.quit()
        sys.exit()

    sorted_tile_names = sorted(tiles_dict.keys())
    total_tiles = len(sorted_tile_names)

    # --- Dynamic Layout Logic ---
    current_x, current_y = 0, 0
    max_row_height = 0
    tile_positions = [] 

    for name in sorted_tile_names:
        tile_obj = tiles_dict[name] # Get the Tile object
        tile_width, tile_height = tile_obj.width, tile_obj.height # Use width/height from object

        if current_x + tile_width > SCREEN_WIDTH:
            current_y += max_row_height
            current_x = 0
            max_row_height = 0
        
        tile_positions.append((current_x, current_y))

        current_x += tile_width
        if tile_height > max_row_height:
            max_row_height = tile_height

    content_height = current_y + max_row_height

    # --- Create Virtual Canvas ---
    virtual_surface = pygame.Surface((SCREEN_WIDTH, content_height)).convert()
    virtual_surface.fill((30, 30, 30)) 

    for i, name in enumerate(sorted_tile_names):
        tile_obj = tiles_dict[name]
        pos = tile_positions[i]
        # --- FIXED: Blit the internal surface attribute ---
        virtual_surface.blit(tile_obj.surface, pos)

    # --- Scrolling Variables & Main Loop ---
    scroll_y = 0
    MAX_SCROLL = max(0, (content_height - SCREEN_HEIGHT) + 100)
    running = True
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 4: scroll_y = max(0, scroll_y - SCROLL_SPEED)
                if event.button == 5: scroll_y = min(MAX_SCROLL, scroll_y + SCROLL_SPEED)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP: scroll_y = max(0, scroll_y - SCROLL_SPEED * 2)
                if event.key == pygame.K_DOWN: scroll_y = min(MAX_SCROLL, scroll_y + SCROLL_SPEED * 2)

        # --- Hover Detection Logic ---
        mouse_x, mouse_y = pygame.mouse.get_pos()
        adjusted_mouse_y = mouse_y + scroll_y 
        hovered_tile_data = None

        for i, name in enumerate(sorted_tile_names):
            pos_x, pos_y = tile_positions[i]
            tile_obj = tiles_dict[name] # Get the Tile object
            
            tile_rect_virtual = pygame.Rect(pos_x, pos_y, tile_obj.width, tile_obj.height)
            
            if tile_rect_virtual.collidepoint(mouse_x, adjusted_mouse_y):
                # --- FIXED: Access attributes from the Tile object ---
                hovered_tile_data = {
                    'name': tile_obj.name,
                    'path': tile_obj.source_path,
                    'source_rect': tile_obj.source_rect_source,
                    'dimensions': f"{tile_obj.width}x{tile_obj.height} px"
                }
                break 

        # --- Drawing Phase ---
        screen.fill((30, 30, 30)) 
        screen.blit(virtual_surface, (0, 0), pygame.Rect(0, scroll_y, SCREEN_WIDTH, SCREEN_HEIGHT))

        # Render hover info if a tile was hit
        if hovered_tile_data:
            info_lines = [
                f"Name: {hovered_tile_data['name']}",
                f"Location: {hovered_tile_data['path']}",
                f"Source Rect: {hovered_tile_data['source_rect']}",
                f"dimensions: {hovered_tile_data['dimensions']}"
            ]
            render_text_box(screen, font, info_lines, (mouse_x, mouse_y), SCREEN_WIDTH, SCREEN_HEIGHT)

        # Update the display
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()


if __name__ == '__main__':
    run_display()