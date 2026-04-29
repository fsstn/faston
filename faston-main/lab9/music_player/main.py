"""
Music Player with Keyboard Controller
======================================
Interactive music player built with Pygame.

Controls:
  P  — Play current track
  S  — Stop
  SPACE — Pause / Resume
  N  — Next track
  B  — Previous (Back) track
  Q  — Quit
"""

import pygame
import sys
from player import MusicPlayer

# ── Constants ────────────────────────────────────────────────────────────────
SCREEN_WIDTH  = 640
SCREEN_HEIGHT = 480
FPS           = 30

# Color palette
COLOR_BG        = (18,  18,  28)
COLOR_PANEL     = (30,  30,  50)
COLOR_ACCENT    = (0,   200, 120)
COLOR_WHITE     = (240, 240, 240)
COLOR_GRAY      = (150, 150, 170)
COLOR_DARK_GRAY = (80,  80,  100)
COLOR_RED       = (220, 60,  60)
COLOR_YELLOW    = (255, 220, 0)


def draw_progress_bar(screen, x, y, width, height, position_sec, color_fill, color_bg):
    """Draw a simple animated progress bar (position cycles 0-60 s for display)."""
    pygame.draw.rect(screen, color_bg, (x, y, width, height), border_radius=6)
    # Cap bar at width for display purposes (real duration unknown without mutagen)
    fill = min(position_sec % 60, 60) / 60 * width
    if fill > 0:
        pygame.draw.rect(screen, color_fill, (x, y, int(fill), height), border_radius=6)
    pygame.draw.rect(screen, COLOR_GRAY, (x, y, width, height), 2, border_radius=6)


def draw_controls_legend(screen, font, x, y):
    """Render the keyboard shortcut legend."""
    controls = [
        ("[P]", "Play"),
        ("[S]", "Stop"),
        ("[SPC]", "Pause/Resume"),
        ("[N]", "Next Track"),
        ("[B]", "Previous Track"),
        ("[Q]", "Quit"),
    ]
    for i, (key, action) in enumerate(controls):
        col = x + (i % 2) * 250
        row = y + (i // 2) * 36
        key_surf  = font.render(key, True, COLOR_ACCENT)
        act_surf  = font.render(f"  {action}", True, COLOR_WHITE)
        screen.blit(key_surf, (col, row))
        screen.blit(act_surf, (col + key_surf.get_width(), row))


def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("🎵 Music Player")
    clock = pygame.time.Clock()

    # Fonts
    font_title  = pygame.font.SysFont("Arial", 40, bold=True)
    font_track  = pygame.font.SysFont("Arial", 26, bold=True)
    font_status = pygame.font.SysFont("Arial", 22)
    font_info   = pygame.font.SysFont("Arial", 18)

    # Music player instance — loads tracks from ./music/ folder
    player = MusicPlayer(music_folder="music")

    running = True
    while running:

        # ── Event handling ───────────────────────────────────────────────
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    running = False
                elif event.key == pygame.K_p:
                    player.play()
                elif event.key == pygame.K_s:
                    player.stop()
                elif event.key == pygame.K_SPACE:
                    player.pause_resume()
                elif event.key == pygame.K_n:
                    player.next_track()
                elif event.key == pygame.K_b:
                    player.prev_track()

        # Auto-advance when a track ends
        player.update()

        # ── Drawing ──────────────────────────────────────────────────────
        screen.fill(COLOR_BG)

        # ── Header ───────────────────────────────────────────────────────
        title_surf = font_title.render("🎵 Music Player", True, COLOR_ACCENT)
        screen.blit(title_surf, title_surf.get_rect(center=(SCREEN_WIDTH // 2, 45)))

        # Divider
        pygame.draw.line(screen, COLOR_DARK_GRAY, (40, 75), (SCREEN_WIDTH - 40, 75), 2)

        # ── Track info panel ─────────────────────────────────────────────
        panel_rect = pygame.Rect(40, 90, SCREEN_WIDTH - 80, 130)
        pygame.draw.rect(screen, COLOR_PANEL, panel_rect, border_radius=12)

        if player.get_total_tracks() > 0:
            # Track name
            track_name = player.get_track_name()
            # Truncate long names
            if len(track_name) > 38:
                track_name = track_name[:35] + "..."
            track_surf = font_track.render(track_name, True, COLOR_WHITE)
            screen.blit(track_surf, track_surf.get_rect(center=(SCREEN_WIDTH // 2, 125)))

            # Track counter
            counter_str = f"Track {player.current_index + 1} / {player.get_total_tracks()}"
            counter_surf = font_info.render(counter_str, True, COLOR_GRAY)
            screen.blit(counter_surf, counter_surf.get_rect(center=(SCREEN_WIDTH // 2, 152)))

            # Progress bar
            pos = player.get_position_seconds()
            draw_progress_bar(screen, 70, 172, SCREEN_WIDTH - 140, 14,
                              pos, COLOR_ACCENT, COLOR_DARK_GRAY)

            # Position label
            pos_label = font_info.render(f"{pos // 60:02d}:{pos % 60:02d}", True, COLOR_GRAY)
            screen.blit(pos_label, (70, 190))
        else:
            no_tracks = font_track.render("No tracks found in ./music/", True, COLOR_RED)
            screen.blit(no_tracks, no_tracks.get_rect(center=(SCREEN_WIDTH // 2, 145)))

        # ── Status badge ─────────────────────────────────────────────────
        status_surf = font_status.render(player.get_status(), True, COLOR_YELLOW)
        screen.blit(status_surf, status_surf.get_rect(center=(SCREEN_WIDTH // 2, 250)))

        # Divider
        pygame.draw.line(screen, COLOR_DARK_GRAY, (40, 272), (SCREEN_WIDTH - 40, 272), 2)

        # ── Controls legend ───────────────────────────────────────────────
        legend_title = font_info.render("KEYBOARD CONTROLS", True, COLOR_GRAY)
        screen.blit(legend_title, (55, 285))
        draw_controls_legend(screen, font_info, 55, 310)

        # Divider
        pygame.draw.line(screen, COLOR_DARK_GRAY, (40, 415), (SCREEN_WIDTH - 40, 415), 2)

        # Footer hint
        hint_surf = font_info.render("Add .wav / .mp3 / .ogg files to the music/ folder", True, COLOR_DARK_GRAY)
        screen.blit(hint_surf, hint_surf.get_rect(center=(SCREEN_WIDTH // 2, 445)))

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()