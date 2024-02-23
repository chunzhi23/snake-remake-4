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


def draw_table(window, table_data, font, frame, x, y):
  cell_width = 0
  cell_height = 0

  for i, row in enumerate(table_data):
    for j, cell in enumerate(row):
      if j == 0:
          cell_width = cell_height = 50
          cell_x = x + j * 50 + frame[0] // 4
      else:
          cell_width = 100
          cell_height = 50
          cell_x = x + 50 + (j - 1) * 100 + frame[0] // 4

      cell_y = y + i * cell_height + 50

      # Draw cell border
      pygame.draw.rect(window, Color.black, (cell_x, cell_y, cell_width, cell_height), 1)

      # Render text
      text_surface = font.render(str(cell) if j != 0 or i == 0 else str(i), True, Color.black)
      text_rect = text_surface.get_rect(center=(cell_x + cell_width // 2, cell_y + cell_height // 2))
      window.blit(text_surface, text_rect)
