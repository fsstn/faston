import pygame
import datetime
import os

class MickeyClock:
    def __init__(self, screen_width, screen_height):
        self.screen_size = (screen_width, screen_height)
        self.center = pygame.math.Vector2(screen_width // 2, screen_height // 2)
        
        base_dir = os.path.dirname(os.path.abspath(__file__))
        img_dir = os.path.join(base_dir, "images")

        self.bg = pygame.image.load(os.path.join(img_dir, "clock.png"))
        self.bg = pygame.transform.scale(self.bg, self.screen_size)
        
        self.mickey_body = pygame.image.load(os.path.join(img_dir, "mikkey.png")).convert_alpha()
        self.mickey_body = pygame.transform.scale(self.mickey_body, (380, 500)) 
        self.mickey_rect = self.mickey_body.get_rect(center=self.center)
        
        # You no longer need to force these into squares if using the pivot function below.
        # Just scale them to the desired length of the hand.
        self.min_hand_orig = pygame.image.load(os.path.join(img_dir, "hand_right_centered.png")).convert_alpha()
        self.min_hand_orig = pygame.transform.scale(self.min_hand_orig, (200, 300)) # Adjust to fit your clock
        
        self.sec_hand_orig = pygame.image.load(os.path.join(img_dir, "hand_left_centered.png")).convert_alpha()
        self.sec_hand_orig = pygame.transform.scale(self.sec_hand_orig, (190, 280)) # Adjust to fit your clock

    def blit_rotate_pivot(self, surface, image, pos, originPos, angle):
        """
        Rotates an image around a specific pivot point.
        pos: The screen coordinate where the pivot should be (self.center).
        originPos: The (x, y) pixel coordinate ON THE IMAGE acting as the shoulder/base.
        """
        # Calculate the offset from the pivot point to the image's geometric center
        image_rect = image.get_rect(topleft=(pos[0] - originPos[0], pos[1] - originPos[1]))
        offset_center_to_pivot = pygame.math.Vector2(pos) - image_rect.center
        
        # Rotate the offset vector (Pygame rotation is negative relative to Vector2)
        rotated_offset = offset_center_to_pivot.rotate(-angle)
        
        # Calculate the new center point for the rotated image
        rotated_image_center = (pos[0] - rotated_offset.x, pos[1] - rotated_offset.y)
        
        # Rotate the actual image and snap its center to the newly calculated point
        rotated_image = pygame.transform.rotate(image, angle)
        rotated_image_rect = rotated_image.get_rect(center=rotated_image_center)
        
        # Draw it
        surface.blit(rotated_image, rotated_image_rect)

    def render(self, surface):
        surface.blit(self.bg, (0, 0))
        surface.blit(self.mickey_body, self.mickey_rect.topleft)
        
        now = datetime.datetime.now()
        
        # Calculate angles
        min_angle = -(now.minute * 6)
        sec_angle = -(now.second * 6)

        # Define the pivot point on the hand images.
        # Assuming the hands are pointing straight UP (12 o'clock) in the source image,
        # the "shoulder" pivot will be at the bottom center of the image.
        min_pivot_x = self.min_hand_orig.get_width() // 2
        min_pivot_y = self.min_hand_orig.get_height()  # Bottom of the image
        
        sec_pivot_x = self.sec_hand_orig.get_width() // 2
        sec_pivot_y = self.sec_hand_orig.get_height()  # Bottom of the image

        # If there is transparent padding at the bottom of your images, subtract it:
        # e.g., sec_pivot_y = self.sec_hand_orig.get_height() - 20

        # Draw the hands
        self.blit_rotate_pivot(surface, self.min_hand_orig, self.center, (min_pivot_x, min_pivot_y), min_angle)
        self.blit_rotate_pivot(surface, self.sec_hand_orig, self.center, (sec_pivot_x, sec_pivot_y), sec_angle)