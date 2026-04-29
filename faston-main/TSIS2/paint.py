import pygame
import datetime
from tools import draw_shape, flood_fill

# start up pygame and fonts
pygame.init()
pygame.font.init()

# screen size and speed
WIDTH, HEIGHT = 1000, 700
FPS = 120

# my color palette
COLORS = {
    'black': (0, 0, 0),
    'white': (255, 255, 255),
    'red': (255, 0, 0),
    'green': (0, 255, 0),
    'blue': (0, 0, 255),
}

# set up the main window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Extended Paint App - TSIS 2")

# this is the main drawing surface where things stay permanently
canvas = pygame.Surface((WIDTH, HEIGHT))
canvas.fill(COLORS['white'])

# fonts for the ui and text tool
font = pygame.font.SysFont('Arial', 24)
ui_font = pygame.font.SysFont('Arial', 16)

def draw_ui(current_tool, current_color, current_size):
    """just draws a bar at the top showing what tool/color is active"""
    ui_rect = pygame.Rect(0, 0, WIDTH, 30)
    pygame.draw.rect(screen, (200, 200, 200), ui_rect)
    pygame.draw.line(screen, (100, 100, 100), (0, 30), (WIDTH, 30), 2)
    
    status_text = f"Tool: {current_tool.upper()} | Color: {current_color} | Size (1,2,3): {current_size}px"
    controls_text = "Press 'T' for Text | 'F' for Fill | 'S' to Save | Keys 1-3 for Size"
    
    status_surf = ui_font.render(status_text, True, COLORS['black'])
    controls_surf = ui_font.render(controls_text, True, COLORS['black'])
    
    screen.blit(status_surf, (10, 5))
    screen.blit(controls_surf, (WIDTH - controls_surf.get_width() - 10, 5))

def main():
    clock = pygame.time.Clock()
    
    # variables to keep track of what's happening right now
    current_tool = 'pencil'
    current_color = 'black'
    current_color_rgb = COLORS[current_color]
    sizes = {pygame.K_1: 2, pygame.K_2: 5, pygame.K_3: 10} # Small, Medium, Large
    current_size = 5
    
    drawing = False
    last_pos = None
    start_pos = None
    
    # stuff for typing text on screen
    typing_mode = False
    text_input = ""
    text_pos = (0, 0)
    
    running = True
    while running:
        # 1. draw the saved canvas to the screen first
        screen.blit(canvas, (0, 0))
        
        # 2. check what the user is doing (clicks, keys)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            # keyboard stuff
            if event.type == pygame.KEYDOWN:
                # handle text typing
                if typing_mode:
                    if event.key == pygame.K_RETURN:
                        # user pressed enter, save the text to the canvas
                        txt_surf = font.render(text_input, True, current_color_rgb)
                        canvas.blit(txt_surf, text_pos)
                        typing_mode = False
                        text_input = ""
                    elif event.key == pygame.K_ESCAPE:
                        # hit escape to stop typing
                        typing_mode = False
                        text_input = ""
                    elif event.key == pygame.K_BACKSPACE:
                        text_input = text_input[:-1]
                    else:
                        text_input += event.unicode
                    continue # don't trigger other hotkeys if we are just typing

                # save drawing if they press ctrl+s
                if event.key == pygame.K_s and (pygame.key.get_mods() & pygame.KMOD_CTRL):
                    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                    filename = f"canvas_{timestamp}.png"
                    pygame.image.save(canvas, filename)
                    print(f"Saved canvas to {filename}")
                
                # change brush size with 1, 2, 3
                if event.key in sizes:
                    current_size = sizes[event.key]
                
                # shortcuts to pick different tools
                if event.key == pygame.K_p: current_tool = 'pencil'
                elif event.key == pygame.K_l: current_tool = 'line'
                elif event.key == pygame.K_r: current_tool = 'rect'
                elif event.key == pygame.K_c: current_tool = 'circle'
                elif event.key == pygame.K_q: current_tool = 'square'
                elif event.key == pygame.K_t: current_tool = 'text'
                elif event.key == pygame.K_f: current_tool = 'fill'
                elif event.key == pygame.K_e: current_tool = 'eraser'
                
                # Shapes shortcuts
                elif event.key == pygame.K_7: current_tool = 'right_tri'
                elif event.key == pygame.K_8: current_tool = 'eq_tri'
                elif event.key == pygame.K_9: current_tool = 'rhombus'

                # shortcuts for colors
                if event.key == pygame.K_z: current_color_rgb, current_color = COLORS['black'], 'black'
                if event.key == pygame.K_x: current_color_rgb, current_color = COLORS['red'], 'red'
                if event.key == pygame.K_v: current_color_rgb, current_color = COLORS['green'], 'green'
                if event.key == pygame.K_b: current_color_rgb, current_color = COLORS['blue'], 'blue'

            # mouse clicks and drags
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1: # Left click
                    if event.pos[1] < 30: continue # don't draw if they are clicking the top menu
                    
                    if current_tool == 'text':
                        typing_mode = True
                        text_pos = event.pos
                        text_input = ""
                    elif current_tool == 'fill':
                        flood_fill(canvas, event.pos, current_color_rgb)
                    else:
                        drawing = True
                        start_pos = event.pos
                        last_pos = event.pos
                        
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1 and drawing:
                    drawing = False
                    # user let go of mouse, so permanently draw the shape
                    if current_tool == 'line':
                        pygame.draw.line(canvas, current_color_rgb, start_pos, event.pos, current_size)
                    elif current_tool in ['rect', 'circle', 'square', 'right_tri', 'eq_tri', 'rhombus']:
                        draw_shape(canvas, current_color_rgb, start_pos, event.pos, current_tool, current_size)

            if event.type == pygame.MOUSEMOTION:
                if drawing:
                    if current_tool == 'pencil':
                        # keep drawing the pencil line as the mouse moves
                        pygame.draw.line(canvas, current_color_rgb, last_pos, event.pos, current_size)
                        last_pos = event.pos
                    elif current_tool == 'eraser':
                        # erasing is just drawing white over things
                        pygame.draw.line(canvas, COLORS['white'], last_pos, event.pos, current_size)
                        last_pos = event.pos

        # 3. show a preview of the shape while dragging (draws to screen, not canvas so it doesn't stay until release)
        if drawing and current_tool not in ['pencil', 'eraser', 'fill', 'text']:
            mouse_pos = pygame.mouse.get_pos()
            if current_tool == 'line':
                pygame.draw.line(screen, current_color_rgb, start_pos, mouse_pos, current_size)
            else:
                draw_shape(screen, current_color_rgb, start_pos, mouse_pos, current_tool, current_size)

        # 4. show the text they are currently typing
        if typing_mode:
            txt_surf = font.render(text_input + "|", True, current_color_rgb)
            screen.blit(txt_surf, text_pos)
            
            # draw a red box around text so they know it's active
            pygame.draw.rect(screen, COLORS['red'], (text_pos[0]-5, text_pos[1]-5, txt_surf.get_width()+10, txt_surf.get_height()+10), 1)

        # 5. draw the top menu last so it stays on top
        draw_ui(current_tool, current_color, current_size)

        # refresh the screen
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    main()