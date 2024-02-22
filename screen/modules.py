import pygame
from items import Color

def draw_text(window, text, font, color, x, y):
  text_surface = font.render(text, True, color)
  text_rect = text_surface.get_rect()
  text_rect.center = (x, y)
  window.blit(text_surface, text_rect)

def draw_image(window, image, x, y):
  # Calculate the position to center the image at the top
  image_rect = image.get_rect()
  x_pos = x - image_rect.width / 2
  y_pos = y

  # Draw the image
  window.blit(image, (x_pos, y_pos))

def draw_button(window, text, font, color, x, y, width, height):
  # Draw shadow
  shadow_color = (max(0, color[0] - 30), max(0, color[1] - 30), max(0, color[2] - 30))
  pygame.draw.rect(window, shadow_color, (x + 3, y + 3, width, height))
  
  # Draw main button
  pygame.draw.rect(window, color, (x, y, width, height))
  
  # Draw text
  draw_text(window, text, font, Color.black, x + width / 2, y + height / 2)