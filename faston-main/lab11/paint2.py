"""
Practice 11 – Game 3: Paint
Extensions from Practice 8:
  1. Draw square
  2. Draw right triangle
  3. Draw equilateral triangle
  4. Draw rhombus
  5. Commented code throughout
"""

import pygame
import sys
import math

# ──────────────────────────────────────────────
# CONSTANTS
# ──────────────────────────────────────────────
SCREEN_W  = 900
SCREEN_H  = 650
TOOLBAR_W = 160   # width of left-side toolbar
CANVAS_X  = TOOLBAR_W
CANVAS_W  = SCREEN_W - TOOLBAR_W
CANVAS_H  = SCREEN_H

# Colours (R, G, B)
WHITE       = (255, 255, 255)
BLACK       = (0,   0,   0)
BG_TOOLBAR  = (40,  42,  54)   # dark toolbar background
BG_CANVAS   = (255, 255, 255)  # white canvas
HIGHLIGHT   = (80, 140, 255)   # selected-tool indicator
TEXT_COLOUR = (220, 220, 220)
GRID_COLOUR = (230, 230, 230)

# Palette of selectable drawing colours
PALETTE = [
    (0,   0,   0),       # Black
    (220, 40,  40),      # Red
    (30,  120, 255),     # Blue
    (50,  200, 80),      # Green
    (255, 220, 0),       # Yellow
    (255, 140, 0),       # Orange
    (180, 60,  200),     # Purple
    (0,   200, 200),     # Cyan
    (255, 105, 180),     # Pink
    (139, 90,  43),      # Brown
    (128, 128, 128),     # Grey
    (255, 255, 255),     # White (eraser colour)
]

# Brush size options (in pixels)
BRUSH_SIZES = [2, 4, 8, 16]

# Tool IDs
TOOL_PENCIL      = "pencil"
TOOL_LINE        = "line"
TOOL_RECT        = "rect"         # bounding rectangle (freeform)
TOOL_SQUARE      = "square"       # ← NEW: forces equal width & height
TOOL_CIRCLE      = "circle"
TOOL_RTRIANGLE   = "right_tri"    # ← NEW: right-angle triangle
TOOL_EQTRIANGLE  = "eq_tri"       # ← NEW: equilateral triangle
TOOL_RHOMBUS     = "rhombus"      # ← NEW: rhombus (diamond)
TOOL_FILL        = "fill"         # flood fill
TOOL_ERASER      = "eraser"

# Tool display names for the toolbar buttons
TOOL_LABELS = {
    TOOL_PENCIL:    "✏ Pencil",
    TOOL_LINE:      "╱ Line",
    TOOL_RECT:      "▭ Rectangle",
    TOOL_SQUARE:    "■ Square",
    TOOL_CIRCLE:    "○ Circle",
    TOOL_RTRIANGLE: "◺ R-Triangle",
    TOOL_EQTRIANGLE:"△ Eq-Triangle",
    TOOL_RHOMBUS:   "◇ Rhombus",
    TOOL_FILL:      "🪣 Fill",
    TOOL_ERASER:    "⬜ Eraser",
}

# Order tools appear in the toolbar (top → bottom)
TOOL_ORDER = [
    TOOL_PENCIL, TOOL_LINE,
    TOOL_RECT, TOOL_SQUARE,
    TOOL_CIRCLE,
    TOOL_RTRIANGLE, TOOL_EQTRIANGLE,
    TOOL_RHOMBUS,
    TOOL_FILL, TOOL_ERASER,
]

# ──────────────────────────────────────────────
# GEOMETRY HELPERS
# ──────────────────────────────────────────────

def points_for_right_triangle(x1, y1, x2, y2):
    """
    Build a right-angle triangle from two corner points.
    Right angle is at bottom-left; the 90° legs are axis-aligned.
      P0 = top-left  (x1, y1)
      P1 = bottom-left (x1, y2)   ← right angle here
      P2 = bottom-right (x2, y2)
    """
    return [(x1, y1), (x1, y2), (x2, y2)]


def points_for_equilateral_triangle(x1, y1, x2, y2):
    """
    Build an equilateral triangle whose base spans from x1 to x2
    at the lower y (y2), and apex is centred above.
    """
    bx1 = min(x1, x2)
    bx2 = max(x1, x2)
    by  = max(y1, y2)           # base y (bottom)
    cx  = (bx1 + bx2) / 2       # centre x
    side = bx2 - bx1             # base length = all sides
    height = side * math.sqrt(3) / 2
    ay  = by - height            # apex y (above base)
    return [(cx, ay), (bx1, by), (bx2, by)]


def points_for_rhombus(x1, y1, x2, y2):
    """
    Build a rhombus (diamond) inscribed in the bounding box
    (x1,y1) → (x2,y2).  The 4 vertices are the midpoints of
    each edge of the bounding box.
    """
    lx = min(x1, x2); rx = max(x1, x2)
    ty = min(y1, y2); by = max(y1, y2)
    cx = (lx + rx) / 2
    cy = (ty + by) / 2
    return [(cx, ty), (rx, cy), (cx, by), (lx, cy)]


def flood_fill(surface, pos, fill_colour):
    """
    Simple iterative flood fill starting from pixel `pos` on `surface`.
    Replaces all connected pixels of the same original colour with `fill_colour`.
    """
    target_colour = surface.get_at(pos)[:3]    # ignore alpha
    if target_colour == fill_colour:
        return    # nothing to do

    width, height = surface.get_size()
    stack = [pos]
    visited = set()

    while stack:
        x, y = stack.pop()
        if (x, y) in visited:
            continue
        if x < 0 or x >= width or y < 0 or y >= height:
            continue
        if surface.get_at((x, y))[:3] != target_colour:
            continue

        surface.set_at((x, y), fill_colour)
        visited.add((x, y))
        stack += [(x+1, y), (x-1, y), (x, y+1), (x, y-1)]


# ──────────────────────────────────────────────
# TOOLBAR UI COMPONENT
# ──────────────────────────────────────────────

class Toolbar:
    """Renders the left-side toolbar with tool buttons, palette, and size picker."""

    BTN_H    = 34
    BTN_PAD  = 4
    SEC_GAP  = 10     # gap between sections

    def __init__(self, font, small_font):
        self.font       = font
        self.small_font = small_font

        # Calculate button layout
        self.tool_rects = {}   # tool_id → pygame.Rect
        y = 10
        for tool in TOOL_ORDER:
            r = pygame.Rect(6, y, TOOLBAR_W - 12, self.BTN_H)
            self.tool_rects[tool] = r
            y += self.BTN_H + self.BTN_PAD

        self.tool_section_bottom = y + self.SEC_GAP

        # Palette swatches (3 per row)
        self.palette_rects = []   # list of (Rect, colour)
        px, py = 8, self.tool_section_bottom + 24
        SWATCH = 28
        for i, col in enumerate(PALETTE):
            col_idx = i % 4
            row_idx = i // 4
            r = pygame.Rect(px + col_idx * (SWATCH + 4), py + row_idx * (SWATCH + 4), SWATCH, SWATCH)
            self.palette_rects.append((r, col))

        self.palette_bottom = py + (len(PALETTE) // 4 + 1) * (SWATCH + 4) + self.SEC_GAP

        # Brush size buttons
        self.size_rects = []   # list of (Rect, size)
        sx, sy = 10, self.palette_bottom + 24
        for i, sz in enumerate(BRUSH_SIZES):
            r = pygame.Rect(sx + i * 34, sy, 30, 30)
            self.size_rects.append((r, sz))

        # Clear button at bottom
        self.clear_rect = pygame.Rect(10, sy + 44, TOOLBAR_W - 20, 32)

    def draw(self, surface, active_tool, active_colour, active_size):
        """Draw the entire toolbar."""
        pygame.draw.rect(surface, BG_TOOLBAR, (0, 0, TOOLBAR_W, SCREEN_H))
        pygame.draw.line(surface, HIGHLIGHT, (TOOLBAR_W - 1, 0), (TOOLBAR_W - 1, SCREEN_H), 2)

        # ── Title ──
        title = self.small_font.render("TOOLS", True, TEXT_COLOUR)
        surface.blit(title, (TOOLBAR_W // 2 - title.get_width() // 2, 2))

        # ── Tool buttons ──
        for tool, rect in self.tool_rects.items():
            colour = HIGHLIGHT if tool == active_tool else (60, 63, 78)
            pygame.draw.rect(surface, colour, rect, border_radius=5)
            txt = self.small_font.render(TOOL_LABELS[tool], True, WHITE)
            surface.blit(txt, txt.get_rect(center=rect.center))

        # ── Palette section header ──
        ph = self.small_font.render("COLOUR", True, TEXT_COLOUR)
        surface.blit(ph, (TOOLBAR_W // 2 - ph.get_width() // 2, self.tool_section_bottom + 6))

        # ── Palette swatches ──
        for rect, col in self.palette_rects:
            pygame.draw.rect(surface, col, rect, border_radius=4)
            if col == active_colour:
                pygame.draw.rect(surface, WHITE, rect, 3, border_radius=4)
            else:
                pygame.draw.rect(surface, (100, 100, 100), rect, 1, border_radius=4)

        # ── Size section header ──
        sh = self.small_font.render("SIZE", True, TEXT_COLOUR)
        surface.blit(sh, (TOOLBAR_W // 2 - sh.get_width() // 2, self.palette_bottom + 6))

        # ── Size buttons ──
        for rect, sz in self.size_rects:
            col = HIGHLIGHT if sz == active_size else (60, 63, 78)
            pygame.draw.rect(surface, col, rect, border_radius=4)
            # Draw a dot proportional to the brush size
            pygame.draw.circle(surface, WHITE, rect.center, min(sz // 2, 10))

        # ── Clear button ──
        pygame.draw.rect(surface, (180, 50, 50), self.clear_rect, border_radius=6)
        ct = self.small_font.render("🗑 Clear", True, WHITE)
        surface.blit(ct, ct.get_rect(center=self.clear_rect.center))

    def handle_click(self, pos, active_tool, active_colour, active_size):
        """
        Check if a mouse click hit any toolbar element.
        Returns (new_tool, new_colour, new_size, clear_requested).
        """
        new_tool   = active_tool
        new_colour = active_colour
        new_size   = active_size
        clear      = False

        for tool, rect in self.tool_rects.items():
            if rect.collidepoint(pos):
                new_tool = tool

        for rect, col in self.palette_rects:
            if rect.collidepoint(pos):
                new_colour = col

        for rect, sz in self.size_rects:
            if rect.collidepoint(pos):
                new_size = sz

        if self.clear_rect.collidepoint(pos):
            clear = True

        return new_tool, new_colour, new_size, clear


# ──────────────────────────────────────────────
# MAIN PAINT APPLICATION
# ──────────────────────────────────────────────

class PaintApp:
    """The main Paint application class."""

    def __init__(self):
        pygame.init()
        self.screen     = pygame.display.set_mode((SCREEN_W, SCREEN_H))
        pygame.display.set_caption("Paint – Practice 11")
        self.clock      = pygame.time.Clock()
        self.font       = pygame.font.SysFont("arial", 18, bold=True)
        self.small_font = pygame.font.SysFont("arial", 13)

        # ── Canvas (persistent drawing surface) ──
        self.canvas     = pygame.Surface((CANVAS_W, CANVAS_H))
        self.canvas.fill(BG_CANVAS)

        # ── Toolbar ──
        self.toolbar    = Toolbar(self.font, self.small_font)

        # ── Active settings ──
        self.active_tool   = TOOL_PENCIL
        self.active_colour = BLACK
        self.active_size   = 4

        # ── Interaction state ──
        self.drawing       = False    # True while LMB is held
        self.start_pos     = None     # canvas-relative start of a shape drag
        self.last_pos      = None     # last pencil/eraser point (for smooth lines)
        self.running       = True

    # ── Coordinate helper ──────────────────────

    def to_canvas(self, pos):
        """Convert screen coords → canvas coords (subtract toolbar width)."""
        return (pos[0] - CANVAS_X, pos[1])

    def on_canvas(self, pos):
        """Return True if the screen position is over the canvas area."""
        return pos[0] >= CANVAS_X

    # ── Main loop ──────────────────────────────

    def run(self):
        while self.running:
            self.clock.tick(60)
            self._handle_events()
            self._draw()
        pygame.quit()
        sys.exit()

    # ── Events ─────────────────────────────────

    def _handle_events(self):
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                self.running = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                # Keyboard shortcut Ctrl+Z: clear canvas
                if event.key == pygame.K_DELETE:
                    self.canvas.fill(BG_CANVAS)

            # ── Mouse button DOWN ──
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                pos = event.pos

                if not self.on_canvas(pos):
                    # Click is inside the toolbar
                    self.active_tool, self.active_colour, self.active_size, clear = \
                        self.toolbar.handle_click(pos, self.active_tool,
                                                  self.active_colour, self.active_size)
                    if clear:
                        self.canvas.fill(BG_CANVAS)
                else:
                    # Click is on the canvas → begin drawing
                    cp = self.to_canvas(pos)
                    self.drawing   = True
                    self.start_pos = cp
                    self.last_pos  = cp

                    # Flood fill is applied immediately on click
                    if self.active_tool == TOOL_FILL:
                        flood_fill(self.canvas, cp, self.active_colour)
                        self.drawing = False

                    # Pencil / eraser: draw a dot at the click point
                    elif self.active_tool in (TOOL_PENCIL, TOOL_ERASER):
                        colour = WHITE if self.active_tool == TOOL_ERASER else self.active_colour
                        pygame.draw.circle(self.canvas, colour, cp, self.active_size // 2)

            # ── Mouse MOTION while button held ──
            elif event.type == pygame.MOUSEMOTION and self.drawing:
                pos = event.pos
                if self.on_canvas(pos):
                    cp = self.to_canvas(pos)

                    if self.active_tool in (TOOL_PENCIL, TOOL_ERASER):
                        # Draw continuous strokes by connecting last point to current
                        colour = WHITE if self.active_tool == TOOL_ERASER else self.active_colour
                        pygame.draw.line(self.canvas, colour, self.last_pos, cp, self.active_size)
                        self.last_pos = cp

                    # For shape tools, preview is handled in _draw(); nothing committed yet

            # ── Mouse button UP ──
            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                if self.drawing and self.on_canvas(event.pos):
                    cp = self.to_canvas(event.pos)
                    # Commit the shape to the canvas
                    self._commit_shape(self.start_pos, cp)
                self.drawing   = False
                self.start_pos = None

    # ── Shape commitment ───────────────────────

    def _commit_shape(self, p1, p2):
        """
        Finalise and draw the shape from p1 to p2 onto the canvas.
        p1 = mouse-down position, p2 = mouse-up position (canvas coords).
        """
        x1, y1 = p1
        x2, y2 = p2
        col  = self.active_colour
        w    = self.active_size

        tool = self.active_tool

        if tool == TOOL_LINE:
            pygame.draw.line(self.canvas, col, p1, p2, w)

        elif tool == TOOL_RECT:
            # Bounding box rectangle (any proportions)
            rx = min(x1, x2); ry = min(y1, y2)
            rw = abs(x2 - x1); rh = abs(y2 - y1)
            pygame.draw.rect(self.canvas, col, (rx, ry, rw, rh), w)

        elif tool == TOOL_SQUARE:
            # Force equal side length (smaller of width/height)
            side = min(abs(x2 - x1), abs(y2 - y1))
            sx   = x1 if x2 >= x1 else x1 - side
            sy   = y1 if y2 >= y1 else y1 - side
            pygame.draw.rect(self.canvas, col, (sx, sy, side, side), w)

        elif tool == TOOL_CIRCLE:
            cx   = (x1 + x2) // 2; cy = (y1 + y2) // 2
            rad  = int(math.hypot(x2 - x1, y2 - y1) / 2)
            pygame.draw.circle(self.canvas, col, (cx, cy), rad, w)

        elif tool == TOOL_RTRIANGLE:
            pts = points_for_right_triangle(x1, y1, x2, y2)
            pts_int = [(int(px), int(py)) for px, py in pts]
            pygame.draw.polygon(self.canvas, col, pts_int, w)

        elif tool == TOOL_EQTRIANGLE:
            pts = points_for_equilateral_triangle(x1, y1, x2, y2)
            pts_int = [(int(px), int(py)) for px, py in pts]
            pygame.draw.polygon(self.canvas, col, pts_int, w)

        elif tool == TOOL_RHOMBUS:
            pts = points_for_rhombus(x1, y1, x2, y2)
            pts_int = [(int(px), int(py)) for px, py in pts]
            pygame.draw.polygon(self.canvas, col, pts_int, w)

    # ── Preview overlay while dragging ─────────

    def _draw_preview(self, surface, p1, p2):
        """
        Draw a ghost/preview of the shape being dragged onto the screen
        (not onto self.canvas, so it doesn't leave a permanent mark).
        """
        # Offset p1 and p2 from canvas coords → screen coords
        def sc(pt): return (pt[0] + CANVAS_X, pt[1])

        x1, y1 = p1
        x2, y2 = p2
        col = (*self.active_colour, 180)   # semi-transparent tint
        w   = self.active_size
        tool = self.active_tool

        # We draw onto the screen surface with the same geometry as _commit_shape
        if tool == TOOL_LINE:
            pygame.draw.line(surface, self.active_colour, sc(p1), sc(p2), w)

        elif tool == TOOL_RECT:
            rx = min(x1, x2) + CANVAS_X; ry = min(y1, y2)
            rw = abs(x2 - x1); rh = abs(y2 - y1)
            pygame.draw.rect(surface, self.active_colour, (rx, ry, rw, rh), w)

        elif tool == TOOL_SQUARE:
            side = min(abs(x2 - x1), abs(y2 - y1))
            sx   = (x1 if x2 >= x1 else x1 - side) + CANVAS_X
            sy   = y1 if y2 >= y1 else y1 - side
            pygame.draw.rect(surface, self.active_colour, (sx, sy, side, side), w)

        elif tool == TOOL_CIRCLE:
            cx = (x1 + x2) // 2 + CANVAS_X; cy = (y1 + y2) // 2
            rad = max(1, int(math.hypot(x2 - x1, y2 - y1) / 2))
            pygame.draw.circle(surface, self.active_colour, (cx, cy), rad, w)

        elif tool == TOOL_RTRIANGLE:
            pts = points_for_right_triangle(x1, y1, x2, y2)
            pts_sc = [(int(px) + CANVAS_X, int(py)) for px, py in pts]
            pygame.draw.polygon(surface, self.active_colour, pts_sc, w)

        elif tool == TOOL_EQTRIANGLE:
            pts = points_for_equilateral_triangle(x1, y1, x2, y2)
            pts_sc = [(int(px) + CANVAS_X, int(py)) for px, py in pts]
            pygame.draw.polygon(surface, self.active_colour, pts_sc, w)

        elif tool == TOOL_RHOMBUS:
            pts = points_for_rhombus(x1, y1, x2, y2)
            pts_sc = [(int(px) + CANVAS_X, int(py)) for px, py in pts]
            pygame.draw.polygon(surface, self.active_colour, pts_sc, w)

    # ── Rendering ──────────────────────────────

    def _draw(self):
        self.screen.fill(BLACK)

        # Blit the canvas onto the screen (right of toolbar)
        self.screen.blit(self.canvas, (CANVAS_X, 0))

        # If a shape drag is in progress, draw a live preview
        if self.drawing and self.start_pos and self.active_tool not in (
                TOOL_PENCIL, TOOL_ERASER, TOOL_FILL):
            mouse_canvas = self.to_canvas(pygame.mouse.get_pos())
            self._draw_preview(self.screen, self.start_pos, mouse_canvas)

        # Toolbar (drawn last so it sits on top)
        self.toolbar.draw(self.screen, self.active_tool, self.active_colour, self.active_size)

        # Status bar at the very bottom of the toolbar
        mx, my  = pygame.mouse.get_pos()
        cx, cy  = self.to_canvas((mx, my))
        tool_lbl = TOOL_LABELS.get(self.active_tool, "")
        status   = self.small_font.render(
            f"{tool_lbl}  ({cx},{cy})  sz:{self.active_size}", True, TEXT_COLOUR)
        pygame.draw.rect(self.screen, (25, 25, 35), (0, SCREEN_H - 18, TOOLBAR_W, 18))
        self.screen.blit(status, (4, SCREEN_H - 16))

        pygame.display.flip()


# ──────────────────────────────────────────────
# ENTRY POINT
# ──────────────────────────────────────────────
if __name__ == "__main__":
    app = PaintApp()
    app.run()