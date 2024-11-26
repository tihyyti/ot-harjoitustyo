import pygame
import sqlite3
import math
import os
import json
import tkinter as tk
from tkinter import messagebox

# Initialize PyGame
pygame.init()

# Set up the display
WIDTH, HEIGHT = 1200, 800
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Gig Stage Floor Plan Designer")

# Colors
WHITE = (255, 255, 255, 188)   # Slight transparency
BLACK = (0, 0, 0)
PASTEL_PEACH_PUFF = (255, 218, 185, 188)  # Slight transparency
PASTEL_MOCCASIN = (255, 228, 181, 188)  # Slight transparency
PASTEL_PAPAYA_WHIP = (255, 239, 213, 188)  # Slight transparency
PASTEL_CORNSILK = (255, 248, 220, 188)  # Slight transparency
PASTEL_LEMON_CHIFFON = (255, 250, 205, 188)  # Slight transparency
PASTEL_LIGHT_GOLDENROD_YELLOW = (250, 250, 210, 188)  # Slight transparency
PASTEL_KHAKI = (240, 230, 140, 188)  # Slight transparency
PASTEL_LAVENDER = (230, 230, 250, 188)  # Slight transparency
PASTEL_THISTLE = (216, 191, 216, 188)  # Slight transparency
PASTEL_PLUM = (221, 160, 221, 188)  # Slight transparency
PASTEL_VIOLET = (238, 130, 238, 188)  # Slight transparency
PASTEL_WHEAT = (245, 222, 179, 188)  # Slight transparency
PASTEL_HONEYDEW = (240, 255, 240, 188)  # Slight transparency
PASTEL_AZURE = (240, 255, 255, 188)  # Slight transparency
PASTEL_LIGHT_CYAN = (224, 255, 255, 188)  # Slight transparency
PASTEL_PALE_TURQUOISE = (175, 238, 238, 188)  # Slight transparency
PASTEL_LIGHT_BLUE = (173, 216, 230, 188)  # Slight transparency
PASTEL_POWDER_BLUE = (176, 224, 230, 188)  # Slight transparency
PASTEL_LIGHT_SKY_BLUE = (135, 206, 250, 188)  # Slight transparency
PASTEL_LIGHT_STEEL_BLUE = (176, 196, 222, 188)  # Slight transparency

# Symbols for musicians and equipment
symbols = {
    "El.Gtr1": pygame.Rect(100, 100, 70, 50),
    "El.Gtr2": pygame.Rect(130, 100, 70, 50),
    "Ac.Gtr1": pygame.Rect(180, 100, 70, 50),
    "Ac.Gtr2": pygame.Rect(210, 100, 70, 50),
    "Vocalist": pygame.Rect(250, 100, 80, 70),
    "Drums": pygame.Rect(600, 300, 110, 90), 
    "Keyboard": pygame.Rect(400, 100, 90, 60),
    "El.G Combo1": pygame.Rect(500, 100, 70, 50),
    "El.G Combo2": pygame.Rect(550, 100, 70, 50),
    "Ac.G Combo3": pygame.Rect(600, 100, 70, 50),
    "Baseman": pygame.Rect(700, 100, 70, 50),
    "B Combo": pygame.Rect(750, 100, 70, 50),
    "Brass": pygame.Rect(800, 100, 120, 66),  
    "Backgrnd Vocalists": pygame.Rect(900, 100, 120, 70), 
    "Mixing Board": pygame.Rect(600, 400, 100, 70)
}

# Parameters
num_rows = 5
stage_width = WIDTH
stage_height = HEIGHT

# Create directory for saving floor plans
if not os.path.exists("FloorPlans"):
    os.makedirs("FloorPlans")

# Function to draw the background grid
def draw_grid(rows):
    for row in range(rows):
        y = stage_height // rows * row
        pygame.draw.line(win, PASTEL_LIGHT_BLUE, (0, y), (stage_width, y))
    for col in range(12):  # Adjust the number of columns as needed
        x = stage_width // 12 * col
        pygame.draw.line(win, PASTEL_LIGHT_BLUE, (x, 0), (x, stage_height))

# Function to draw symbols
def draw_symbols():
    for name, rect in symbols.items(): 
        if "Gtr" in name:
            color = PASTEL_PEACH_PUFF if "Gtr" or "Baseman" in name else PASTEL_PEACH_PUFF
            text = ["Vocalmic:", "0-1"] 
        elif "Combo" in name:
            color = PASTEL_MOCCASIN
            text = ["Instrumic", "0-1"]
        elif "Keyboard" in name:
            color = PASTEL_LIGHT_BLUE
            text = ["Vocalmics:", "0-1"]
        elif "Drums" in name:
            color = PASTEL_PALE_TURQUOISE
            text = ["Instrumics:", "0-8"]
        elif "Brass" in name:
            color = PASTEL_PLUM
            text = ["Instrumics:", "0-3"]
        elif "Backgrnd Vocalists" in name:
            color = PASTEL_LIGHT_GOLDENROD_YELLOW
            text = ["Vocalmics:", "1-3"]
        elif "Vocalist" in name:
            color = PASTEL_LIGHT_GOLDENROD_YELLOW
            text = ["Vocalmics:", "1"]
        else:
            color = PASTEL_LIGHT_BLUE
            text = ["", ""]
            
        pygame.draw.rect(win, color, rect)
        font = pygame.font.Font(None, 18)
        for i, line in enumerate(text):
            text_surface = font.render(line, True, BLACK)
            text_rect = text_surface.get_rect(center=(rect.centerx, rect.centery - 10 + i * 20))
            win.blit(text_surface, text_rect) 
            
        # Draw the name of the symbol above the rectangle 
        name_surface = font.render(name, True, BLACK)
        name_rect = name_surface.get_rect(center=(rect.centerx, rect.y - 10))
        win.blit(name_surface, name_rect)
            
        # Draw cable length below the symbol 
        cable_length = calculate_cable_length(rect)
        length_text = font.render(f"{cable_length} m", True, BLACK)
        win.blit(length_text, (rect.x, rect.y + rect.height + 5))
                               
# Function to draw cables
def draw_cables():
    mixer_center = symbols["Mixing Board"].center
    for name, rect in symbols.items():
        if name != "Mixing Board":
            if "Vocalist" in name or "Backgrnd Vocalists" in name or "Gtr" in name or "Baseman" in name:
                color = PASTEL_PEACH_PUFF
            elif "G Combo"  in name or "Brass" in name or "Drums" in name:
                color = PASTEL_PALE_TURQUOISE
            elif "B Combo" in name or "Keyboard" in name:
                color = BLACK
            else:
                color = PASTEL_LIGHT_BLUE
                
            pygame.draw.line(win, color, mixer_center, rect.center, 2)

    # Draw additional cables
    # 2 black cables from Keyboard to Mixing Board
    pygame.draw.line(win, BLACK, mixer_center, symbols["Keyboard"].center, 2)
    pygame.draw.line(win, BLACK, mixer_center, symbols["Keyboard"].center, 2)

    # 4 green cables between Drum Set and Mixing Board
    for i in range(2):
        pygame.draw.line(win, PASTEL_PALE_TURQUOISE, mixer_center, symbols["Drums"].center, 2)
        pygame.draw.line(win, PASTEL_PALE_TURQUOISE, mixer_center, symbols["Drums"].center, 2)

# Function to calculate cable length
def calculate_cable_length(rect):
    mixer_center = symbols["Mixing Board"].center
    distance = math.sqrt((rect.centerx - mixer_center[0])**2 + (rect.centery - mixer_center[1])**2) / 100
    cable_length = math.ceil(distance + 1.2)
    return cable_length

# Function to calculate cable lengths
def calculate_cable_lengths():
    cable_lengths = {}
    for name, rect in symbols.items():
        if name != "Mixing Board":
            cable_length = calculate_cable_length(rect)
            cable_lengths[name] = cable_length
    return cable_lengths

# Function to quantize cable lengths by row
def quantize_cable_lengths():
    rows = {1: [], 2: [], 3: [], 4: [], 5: []}
    for name, rect in symbols.items():
        if name != "Mixing Board":
            row = rect.y // (stage_height // num_rows) + 1
            rows[row].append(name)
    
    cable_lengths = calculate_cable_lengths()
    quantized_lengths = {}
    for row, names in rows.items():
        if names:
            total_length = sum(cable_lengths[name] for name in names)
            quantized_lengths[row] = {
                "count": len(names),
                "length": total_length // len(names)
            }
    return quantized_lengths

# Function to save the stage floor plan as a .png file
def save_as_png(filename):
    pygame.image.save(win, filename)

# Function to save system parameters as a .json file
def save_system_parameters(filename, parameters):
    with open(filename, 'w') as f:
        json.dump(parameters, f)

# Function to draw the parameter UI
def draw_ui():
    font = pygame.font.Font(None, 24)
    text = font.render(f"Rows: {num_rows}", True, BLACK)
    win.blit(text, (10, 10))
    text = font.render(f"Stage Width: {stage_width/100} m", True, BLACK)
    win.blit(text, (10, 40))
    text = font.render(f"Stage Height: {stage_height/100} m", True, BLACK)
    win.blit(text, (10, 70))

    # Draw legend for cable colors
    legend_header = font.render("Cable coloring:", True, BLACK)
    win.blit(legend_header, (10, 110))
    legend_red = font.render("Red: Vocalist mic", True, PASTEL_PEACH_PUFF)
    win.blit(legend_red, (10, 140))
    legend_green = font.render("Green: Instrument mic", True, PASTEL_PALE_TURQUOISE)
    win.blit(legend_green, (10, 170))
    legend_black = font.render("Black: Line-level I/F", True, BLACK)
    win.blit(legend_black, (10, 200))

# Function to draw the floating window UI
def draw_floating_ui():
    font = pygame.font.Font(None, 20)
    pygame.draw.rect(win, PASTEL_LIGHT_SKY_BLUE, (WIDTH - 300, 10, 290, 300), 0)
    pygame.draw.rect(win, BLACK, (WIDTH - 300, 10, 290, 300), 2)

    # Venue name input
    text = font.render("Venue name:", True, BLACK)
    win.blit(text, (WIDTH - 290, 20))
    entry_venue_name = pygame.Rect(WIDTH - 290, 50, 270, 30)
    pygame.draw.rect(win, WHITE, entry_venue_name, 0)
    pygame.draw.rect(win, BLACK, entry_venue_name, 2)

    # Floor dimensions input
    text = font.render("Width (m):", True, BLACK)
    win.blit(text, (WIDTH - 290, 90))
    entry_width = pygame.Rect(WIDTH - 200, 90, 50, 30)
    pygame.draw.rect(win, WHITE, entry_width, 0)
    pygame.draw.rect(win, BLACK, entry_width, 2)
    text = font.render("Depth (m):", True, BLACK)
    win.blit(text, (WIDTH - 290, 130))
    entry_depth = pygame.Rect(WIDTH - 200, 130, 50, 30)
    pygame.draw.rect(win, WHITE, entry_depth, 0)
    pygame.draw.rect(win, BLACK, entry_depth, 2)

    # Save button and input
    text = font.render("Save as:", True, BLACK)
    win.blit(text, (WIDTH - 290, 170))
    entry_save_as = pygame.Rect(WIDTH - 200, 170, 150, 30)
    pygame.draw.rect(win, WHITE, entry_save_as, 0)
    pygame.draw.rect(win, BLACK, entry_save_as, 2)
    save_button = pygame.Rect(WIDTH - 290, 210, 100, 30)
    pygame.draw.rect(win, PASTEL_LIGHT_BLUE, save_button)
    text = font.render("Save", True, BLACK)
    win.blit(text, (WIDTH - 270, 215))

    # Pause and Quit buttons
    pause_button = pygame.Rect(WIDTH - 170, 210, 100, 30)
    pygame.draw.rect(win, PASTEL_LIGHT_BLUE, pause_button)
    text = font.render("Pause", True, BLACK)
    win.blit(text, (WIDTH - 150, 215))

    quit_button = pygame.Rect(WIDTH - 290, 250, 100, 30)
    pygame.draw.rect(win, PASTEL_LIGHT_BLUE, quit_button)
    text = font.render("Quit", True, BLACK)
    win.blit(text, (WIDTH - 270, 255))

    return entry_venue_name, entry_width, entry_depth, entry_save_as, save_button, pause_button, quit_button

# Function to draw the "Venue UI" button
def draw_venue_ui_button():
    font = pygame.font.Font(None, 28)
    venue_ui_button = pygame.Rect(WIDTH - 100, 10, 90, 30)
    pygame.draw.rect(win, PASTEL_LIGHT_BLUE, venue_ui_button)
    text = font.render("Venue UI", True, BLACK)
    win.blit(text, (WIDTH - 95, 15))
    return venue_ui_button

# Main loop
run = True
selected_symbol = None
offset_x = 0
offset_y = 0
clock = pygame.time.Clock()
show_ui = False

while run:
    win.fill(WHITE)
    draw_grid(num_rows)
    draw_symbols()
    draw_cables()
    draw_ui()
    venue_ui_button = draw_venue_ui_button()
    if show_ui:
        entry_venue_name, entry_width, entry_depth, entry_save_as, save_button, pause_button, quit_button = draw_floating_ui()
    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            for name, rect in symbols.items():
                if rect.collidepoint(event.pos):
                    selected_symbol = name
                    offset_x = rect.x - event.pos[0]
                    offset_y = rect.y - event.pos[1]
                    break
            if venue_ui_button.collidepoint(event.pos):
                show_ui = not show_ui
            if show_ui:
                if save_button.collidepoint(event.pos):
                    filename = "FloorPlans/FloorPlanOf_" + entry_venue_name + ".png"
                    save_as_png(filename)
                    parameters = {
                        "venue_name": entry_venue_name,
                        "stage_width": stage_width,
                        "stage_height": stage_height,
                        "filename": filename
                    }
                    save_system_parameters("FloorPlans/system_parameters.json", parameters)
                elif pause_button.collidepoint(event.pos):
                    show_ui = not show_ui
                elif quit_button.collidepoint(event.pos):
                    run = False
                    save_prompt = True
        elif event.type == pygame.MOUSEBUTTONUP:
            selected_symbol = None
        elif event.type == pygame.MOUSEMOTION:
            if selected_symbol:
                symbols[selected_symbol].x = event.pos[0] + offset_x
                symbols[selected_symbol].y = event.pos[1] + offset_y
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                num_rows = min(num_rows + 1, 5)
            elif event.key == pygame.K_DOWN:
                num_rows = max(num_rows - 1, 1)
            elif event.key == pygame.K_LEFT:
                stage_width = max(stage_width - 50, 600)
            elif event.key == pygame.K_RIGHT:
                stage_width = min(stage_width + 50, 1600)
            elif event.key == pygame.K_w:
                stage_height = max(stage_height - 50, 400)
            elif event.key == pygame.K_s:
                stage_height = min(stage_height + 50, 1200)

    # Calculate and print quantized cable lengths
    quantized_lengths = quantize_cable_lengths()
    for row, data in quantized_lengths.items():
        print(f"Row {row}: {data['count']} mic-cables (XLR), length: {data['length']} m")

    # Save the stage floor plan as a .png file
    save_as_png("stage_floor_plan.png")

    # Control the frame rate
    clock.tick(30)

pygame.quit()