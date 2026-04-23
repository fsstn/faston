import os
import pygame

SONG_END = pygame.USEREVENT + 1


class MusicPlayer:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.SysFont("Arial", 30, bold=True)
        self.small_font = pygame.font.SysFont("Arial", 22)

        self.songs = [
            r"C:\Users\Nurali\Downloads\Classical Study Music Meditation Relaxing Music Relaxing Piano Music Lyudvig van Betkhoven - Эзотерика (128k).mp3",
            r"C:\Users\Nurali\Downloads\Л.Бетховен Лунная соната - Ludwig Van Beethoven - Moonlight Sonata - Людмила Нарыжная (128k).mp3",
        ]

        self.names = [
            "Track 1: Fur Elise",
            "Track 2: Moonlight Sonata",
        ]

        self.current = 0
        self.is_playing = False

        for path in self.songs:
            if not os.path.exists(path):
                raise FileNotFoundError(f"File not found: {path}")

        pygame.mixer.music.set_endevent(SONG_END)

    def load_current(self):
        pygame.mixer.music.load(self.songs[self.current])

    def play(self):
        if not self.is_playing:
            self.load_current()
            pygame.mixer.music.play(0)
            self.is_playing = True

    def stop(self):
        pygame.mixer.music.stop()
        self.is_playing = False

    def next_track(self):
        self.current = (self.current + 1) % len(self.songs)
        self.load_current()
        pygame.mixer.music.play(0)
        self.is_playing = True

    def previous_track(self):
        self.current = (self.current - 1) % len(self.songs)
        self.load_current()
        pygame.mixer.music.play(0)
        self.is_playing = True

    def get_position_seconds(self):
        pos_ms = pygame.mixer.music.get_pos()
        return max(0, pos_ms // 1000)

    def draw(self):
        self.screen.fill((25, 25, 35))

        title = self.font.render("Music Player with Keyboard Controller", True, (255, 255, 255))
        self.screen.blit(title, (40, 30))

        current_track = self.small_font.render(
            f"Current track: {self.names[self.current]}",
            True,
            (230, 230, 230)
        )
        self.screen.blit(current_track, (40, 100))

        status_text = "Playing" if self.is_playing else "Stopped"
        status = self.small_font.render(f"Status: {status_text}", True, (230, 230, 230))
        self.screen.blit(status, (40, 140))

        position = self.get_position_seconds()
        pos_text = self.small_font.render(f"Track position: {position} sec", True, (230, 230, 230))
        self.screen.blit(pos_text, (40, 180))

        controls = [
            "P = Play",
            "S = Stop",
            "N = Next track",
            "B = Previous track",
            "Q = Quit",
        ]

        y = 250
        for line in controls:
            txt = self.small_font.render(line, True, (200, 200, 200))
            self.screen.blit(txt, (40, y))
            y += 35