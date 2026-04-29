"""
player.py — Music Player Logic
================================
Manages the playlist and pygame.mixer playback.
Supports: play, stop, next, previous, and status queries.
"""

import pygame
import os


class MusicPlayer:
    """
    Encapsulates all playlist management and audio playback.
    Works with any list of audio file paths (WAV or MP3).
    """

    def __init__(self, music_folder="music"):
        pygame.mixer.init()

        self.music_folder  = music_folder
        self.playlist      = []      # List of absolute file paths
        self.current_index = 0       # Index of currently loaded track
        self.is_playing    = False
        self.is_stopped    = True

        self._load_playlist()

    # ── Playlist management ───────────────────────────────────────────────────

    def _load_playlist(self):
        """Scan music_folder for .wav and .mp3 files and build playlist."""
        supported = (".wav", ".mp3", ".ogg")
        if not os.path.isdir(self.music_folder):
            print(f"[Player] Warning: '{self.music_folder}' folder not found.")
            return

        for filename in sorted(os.listdir(self.music_folder)):
            if filename.lower().endswith(supported):
                full_path = os.path.join(self.music_folder, filename)
                self.playlist.append(full_path)

        if self.playlist:
            print(f"[Player] Loaded {len(self.playlist)} track(s).")
        else:
            print(f"[Player] No audio files found in '{self.music_folder}'.")

    def get_track_name(self, index=None):
        """Return display name (filename without extension) of a track."""
        if not self.playlist:
            return "No tracks loaded"
        idx = index if index is not None else self.current_index
        return os.path.splitext(os.path.basename(self.playlist[idx]))[0]

    def get_total_tracks(self):
        return len(self.playlist)

    # ── Playback controls ─────────────────────────────────────────────────────

    def play(self):
        """Play the current track from the beginning."""
        if not self.playlist:
            print("[Player] No tracks to play.")
            return

        track = self.playlist[self.current_index]
        try:
            pygame.mixer.music.load(track)
            pygame.mixer.music.play()
            self.is_playing = True
            self.is_stopped = False
            print(f"[Player] Playing: {self.get_track_name()}")
        except pygame.error as e:
            print(f"[Player] Error loading track: {e}")

    def stop(self):
        """Stop playback."""
        pygame.mixer.music.stop()
        self.is_playing = False
        self.is_stopped = True
        print("[Player] Stopped.")

    def pause_resume(self):
        """Toggle pause / resume."""
        if self.is_playing:
            pygame.mixer.music.pause()
            self.is_playing = False
            print("[Player] Paused.")
        else:
            pygame.mixer.music.unpause()
            self.is_playing = True
            print("[Player] Resumed.")

    def next_track(self):
        """Advance to the next track (wraps around)."""
        if not self.playlist:
            return
        self.current_index = (self.current_index + 1) % len(self.playlist)
        self.play()

    def prev_track(self):
        """Go back to the previous track (wraps around)."""
        if not self.playlist:
            return
        self.current_index = (self.current_index - 1) % len(self.playlist)
        self.play()

    # ── Status ────────────────────────────────────────────────────────────────

    def update(self):
        """
        Call once per frame.
        Auto-advance to next track when the current one finishes.
        """
        if self.is_playing and not pygame.mixer.music.get_busy():
            print("[Player] Track ended, advancing to next.")
            self.next_track()

    def get_position_seconds(self):
        """Return playback position in seconds (pygame gives milliseconds)."""
        if self.is_playing or not self.is_stopped:
            pos_ms = pygame.mixer.music.get_pos()
            return max(pos_ms // 1000, 0)
        return 0

    def get_status(self):
        """Return a human-readable status string."""
        if self.is_stopped:
            return "⏹ Stopped"
        if self.is_playing:
            return "▶ Playing"
        return "⏸ Paused"