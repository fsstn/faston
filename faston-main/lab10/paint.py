"""
Practice 10 – Game 3: Paint
A simple drawing app extending the nerdparadise tutorial with:
  • Pencil (freehand drawing)
  • Rectangle tool   (click-drag to define bounding box)
  • Circle tool      (click-drag; radius = half the diagonal)
  • Eraser tool
  • Colour palette   (click any swatch to select)
  • Brush-size slider
  • Clear canvas button
"""

import pygame
import sys
import math

pygame.init()

# ── Screen layout constants ───────────────────────────────────────────────────
SCREEN_W     = 900
SCREEN_H     = 650
TOOLBAR_H    = 70                         # toolbar height at the top
CANVAS_TOP   = TOOLBAR_H                 # y-coordinate where canvas begins
CANVAS_H     = SCREEN_H - TOOLBAR_H
CANVAS_RECT  = pygame.Rect(0, CANVAS_TOP, SCREEN_W, CANVAS_H)

# ── Colours ───────────────────────────────────────────────────────────────────
BLACK   = (0,   0,   0  )
WHITE   = (255, 255, 255)
LT_GRAY = (230, 230, 230)
MID_GRY = (160, 160, 160)
DK_GRAY = (80,  80,  80 )

# Colour palette shown as swatches in the toolbar
PALETTE = [
    (0,   0,   0  ),   # black
    (255, 255, 255),   # white
    (220, 30,  30 ),   # red
    (30,  180, 30 ),   # green
    (30,  80,  220),   # blue
    (255, 220, 0  ),   # yellow
    (255, 130, 0  ),   # orange
    (140, 0,   200),   # purple
    (0,   200, 200),   # cyan
    (255, 0,   180),   # magenta
    (120, 80,  40 ),   # brown
    (100, 100, 100),   # gray
    (255, 160, 180),   # pink
    (0,   100, 60 ),   # dark green
]

# ── Tool identifiers ──────────────────────────────────────────────────────────
PENCIL    = "pencil"
RECTANGLE = "rectangle"
CIRCLE    = "circle"
ERASER    = "eraser"
TOOLS     = [PENCIL, RECTANGLE, CIRCLE, ERASER]
ICONS     = ["✏ Pencil", "▭ Rect", "◯ Circle", "⌫ Eraser"]

screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
pygame.display.set_caption("Paint")
clock  = pygame.time.Clock()
font   = pygame.font.SysFont("Arial", 15, bold=True)
small  = pygame.font.SysFont("Arial", 13)


# ── PaintApp ──────────────────────────────────────────────────────────────────
class PaintApp:
    def __init__(self):
        # Persistent canvas surface (white background)
        self.canvas = pygame.Surface((SCREEN_W, CANVAS_H))
        self.canvas.fill(WHITE)

        self.color       = BLACK    # active drawing colour
        self.tool        = PENCIL   # active tool
        self.brush_size  = 5        # pencil radius
        self.eraser_size = 20       # eraser radius

        # Shape drawing state
        self.drawing   = False      # True while mouse button is held
        self.start_pos = None       # canvas-coordinate start of current stroke
        self.prev_pos  = None       # last position (for smooth pencil lines)

        # Preview: snapshot of canvas before a shape is committed
        self._snapshot = None

    # ── Event dispatcher ──────────────────────────────────────────────────────
    def handle(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self._on_press(event.pos)

        elif event.type == pygame.MOUSEMOTION and self.drawing:
            self._on_drag(event.pos)

        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            self._on_release(event.pos)

    # ── Press ──────────────────────────────────────────────────────────────────
    def _on_press(self, pos):
        mx, my = pos
        if my < TOOLBAR_H:
            self._toolbar_click(mx, my)
            return

        # Convert screen → canvas coordinates
        cp = (mx, my - CANVAS_TOP)
        self.drawing   = True
        self.start_pos = cp
        self.prev_pos  = cp

        if self.tool == PENCIL:
            pygame.draw.circle(self.canvas, self.color, cp, self.brush_size)
        elif self.tool == ERASER:
            pygame.draw.circle(self.canvas, WHITE, cp, self.eraser_size)
        elif self.tool in (RECTANGLE, CIRCLE):
            # Save a snapshot of the canvas so we can overwrite it on every
            # mouse-move to give the user a live preview.
            self._snapshot = self.canvas.copy()

    # ── Drag ──────────────────────────────────────────────────────────────────
    def _on_drag(self, pos):
        mx, my = pos
        # Clamp to canvas area
        cx = max(0, min(SCREEN_W - 1, mx))
        cy = max(CANVAS_TOP, min(SCREEN_H - 1, my))
        cp = (cx, cy - CANVAS_TOP)

        if self.tool == PENCIL:
            # Draw a thick line from the previous position to smooth the stroke
            pygame.draw.line(self.canvas, self.color, self.prev_pos, cp,
                             self.brush_size * 2)
            pygame.draw.circle(self.canvas, self.color, cp, self.brush_size)
            self.prev_pos = cp

        elif self.tool == ERASER:
            pygame.draw.circle(self.canvas, WHITE, cp, self.eraser_size)
            self.prev_pos = cp

        elif self.tool in (RECTANGLE, CIRCLE):
            # Restore snapshot then draw the preview shape
            self.canvas.blit(self._snapshot, (0, 0))
            self._draw_shape(self.start_pos, cp, self.canvas)

    # ── Release ───────────────────────────────────────────────────────────────
    def _on_release(self, pos):
        if not self.drawing:
            return
        mx, my = pos
        cx = max(0, min(SCREEN_W - 1, mx))
        cy = max(CANVAS_TOP, min(SCREEN_H - 1, my))
        cp = (cx, cy - CANVAS_TOP)

        if self.tool in (RECTANGLE, CIRCLE):
            # Commit final shape
            self.canvas.blit(self._snapshot, (0, 0))
            self._draw_shape(self.start_pos, cp, self.canvas)

        self.drawing   = False
        self.start_pos = None
        self.prev_pos  = None
        self._snapshot = None

    # ── Shape drawing helper ──────────────────────────────────────────────────
    def _draw_shape(self, p1, p2, surface):
        """Draw either a rectangle or circle from corner p1 to corner p2."""
        x1, y1 = p1
        x2, y2 = p2

        if self.tool == RECTANGLE:
            rect = pygame.Rect(min(x1, x2), min(y1, y2),
                               abs(x2 - x1), abs(y2 - y1))
            pygame.draw.rect(surface, self.color, rect, 2)

        elif self.tool == CIRCLE:
            # Centre = midpoint of the drag diagonal; radius = half diagonal
            cx = (x1 + x2) // 2
            cy = (y1 + y2) // 2
            radius = int(math.hypot(x2 - x1, y2 - y1) / 2)
            if radius > 0:
                pygame.draw.circle(surface, self.color, (cx, cy), radius, 2)

    # ── Toolbar click ─────────────────────────────────────────────────────────
    def _toolbar_click(self, mx, my):
        # 1. Colour swatches (row 1)
        for i, col in enumerate(PALETTE):
            sx = 10 + i * 38
            if sx <= mx <= sx + 32 and 6 <= my <= 34:
                self.color = col
                return

        # 2. Tool buttons (row 2)
        for i, tool in enumerate(TOOLS):
            tx = 10 + i * 100
            if tx <= mx <= tx + 92 and 38 <= my <= 62:
                self.tool = tool
                return

        # 3. Brush size  –  +  buttons
        # _draw_size_control(surface, x=550, y=6) draws buttons at x+78=628 and x+104=654
        if 628 <= mx <= 650 and 6 <= my <= 28:
            self.brush_size = max(1, self.brush_size - 1)
        elif 654 <= mx <= 676 and 6 <= my <= 28:
            self.brush_size = min(40, self.brush_size + 1)

        # 4. Eraser size  –  +
        # _draw_size_control(surface, x=550, y=36) draws buttons at x+78=628 and x+104=654
        if 628 <= mx <= 650 and 36 <= my <= 58:
            self.eraser_size = max(5, self.eraser_size - 2)
        elif 654 <= mx <= 676 and 36 <= my <= 58:
            self.eraser_size = min(60, self.eraser_size + 2)

        # 5. Clear button
        if SCREEN_W - 90 <= mx <= SCREEN_W - 10 and 20 <= my <= 50:
            self.canvas.fill(WHITE)

    # ── Full draw ─────────────────────────────────────────────────────────────
    def draw(self, surface):
        # Canvas
        surface.blit(self.canvas, (0, CANVAS_TOP))

        # Live shape preview drawn directly on screen (not on canvas yet)
        mx, my = pygame.mouse.get_pos()
        if self.drawing and self.start_pos and self.tool in (RECTANGLE, CIRCLE):
            cp = (mx, my - CANVAS_TOP)
            preview_surf = pygame.Surface((SCREEN_W, CANVAS_H), pygame.SRCALPHA)
            self._draw_shape(self.start_pos, cp, preview_surf)
            # (shape is already on self.canvas from _on_drag; this is just a safety)

        # Eraser cursor ring
        if self.tool == ERASER:
            pygame.draw.circle(surface, MID_GRY, (mx, my), self.eraser_size, 2)

        # ── Toolbar ───────────────────────────────────────────────────────────
        pygame.draw.rect(surface, LT_GRAY, (0, 0, SCREEN_W, TOOLBAR_H))
        pygame.draw.line(surface, MID_GRY, (0, TOOLBAR_H), (SCREEN_W, TOOLBAR_H), 2)

        # Colour swatches
        for i, col in enumerate(PALETTE):
            sx = 10 + i * 38
            pygame.draw.rect(surface, col, (sx, 6, 32, 28))
            border = BLACK if col == self.color else DK_GRAY
            thick  = 3     if col == self.color else 1
            pygame.draw.rect(surface, border, (sx, 6, 32, 28), thick)

        # Tool buttons
        for i, (tool, icon) in enumerate(zip(TOOLS, ICONS)):
            tx = 10 + i * 100
            btn_col = (90, 140, 240) if tool == self.tool else (190, 190, 190)
            pygame.draw.rect(surface, btn_col, (tx, 38, 92, 26), border_radius=4)
            lbl = font.render(icon, True, WHITE if tool == self.tool else BLACK)
            surface.blit(lbl, (tx + 46 - lbl.get_width()//2, 44))

        # Brush / eraser size controls
        self._draw_size_control(surface, 550, 6,  "Brush", self.brush_size)
        self._draw_size_control(surface, 550, 36, "Ersr",  self.eraser_size)

        # Active-colour preview swatch
        pygame.draw.rect(surface, self.color, (SCREEN_W - 100, 8,  42, 42))
        pygame.draw.rect(surface, BLACK,      (SCREEN_W - 100, 8,  42, 42), 2)
        cl = small.render("colour", True, DK_GRAY)
        surface.blit(cl, (SCREEN_W - 100, 52))

        # Clear button
        pygame.draw.rect(surface, (210, 60, 60), (SCREEN_W - 90, 20, 74, 28), border_radius=5)
        ct = font.render("Clear", True, WHITE)
        surface.blit(ct, (SCREEN_W - 90 + 37 - ct.get_width()//2, 25))

    def _draw_size_control(self, surface, x, y, label, value):
        """Render a  Label: [–] N [+]  widget at position (x, y)."""
        lbl = small.render(f"{label}: {value}", True, DK_GRAY)
        surface.blit(lbl, (x, y + 2))
        # – button
        pygame.draw.rect(surface, MID_GRY, (x + 78, y, 22, 22), border_radius=3)
        surface.blit(font.render("−", True, BLACK), (x + 83, y + 2))
        # + button
        pygame.draw.rect(surface, MID_GRY, (x + 104, y, 22, 22), border_radius=3)
        surface.blit(font.render("+", True, BLACK), (x + 108, y + 2))


# ── Main loop ─────────────────────────────────────────────────────────────────
def main():
    app = PaintApp()

    while True:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            app.handle(event)

        screen.fill(WHITE)
        app.draw(screen)
        pygame.display.flip()


if __name__ == "__main__":
    main()