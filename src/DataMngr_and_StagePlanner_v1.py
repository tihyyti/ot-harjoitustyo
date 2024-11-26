import pygame
from services import BandService, ArtistService, GearService, GearBundleService, GearBundleSoundService, BandGearBundleService, ArtistGearBundleService

# Initialize PyGame
pygame.init()

# Set up the display
WIDTH, HEIGHT = 1200, 800
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Gig Stage Floor Plan Designer")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PASTEL_YELLOW = (255, 255, 204)
PASTEL_BLUE = (173, 216, 230)
PASTEL_GREEN = (144, 238, 144)
PASTEL_RED = (255, 182, 193)

# Initialize services
db_path = 'soundslite_v1.db'
band_service = BandService(db_path)
artist_service = ArtistService(db_path)
gear_service = GearService(db_path)
gearbundle_service = GearBundleService(db_path)
gearbundlesound_service = GearBundleSoundService(db_path)
bandgearbundle_service = BandGearBundleService(db_path)
artistgearbundle_service = ArtistGearBundleService(db_path)

# Function to draw the "Data Management" button
def draw_data_management_button():
    font = pygame.font.Font(None, 28)
    data_management_button = pygame.Rect(WIDTH - 150, 10, 140, 60)
    pygame.draw.rect(win, PASTEL_YELLOW, data_management_button)
    text = font.render("Data", True, BLACK)
    win.blit(text, (WIDTH - 140, 15))
    text = font.render("Management", True, BLACK)
    win.blit(text, (WIDTH - 140, 45))
    return data_management_button

# Function to draw the "Back to Floor Planner" button
def draw_back_button():
    font = pygame.font.Font(None, 28)
    back_button = pygame.Rect(WIDTH - 150, 10, 140, 60)
    pygame.draw.rect(win, PASTEL_BLUE, back_button)
    text = font.render("Back to", True, BLACK)
    win.blit(text, (WIDTH - 140, 15))
    text = font.render("Floor Planner", True, BLACK)
    win.blit(text, (WIDTH - 140, 45))
    return back_button

# Function to draw CRUD buttons
def draw_crud_buttons():
    font = pygame.font.Font(None, 28)
    create_button = pygame.Rect(50, 200, 140, 60)
    read_button = pygame.Rect(200, 200, 140, 60)
    update_button = pygame.Rect(350, 200, 140, 60)
    delete_button = pygame.Rect(500, 200, 140, 60)
    
    pygame.draw.rect(win, PASTEL_GREEN, create_button)
    pygame.draw.rect(win, PASTEL_BLUE, read_button)
    pygame.draw.rect(win, PASTEL_YELLOW, update_button)
    pygame.draw.rect(win, PASTEL_RED, delete_button)
    
    win.blit(font.render("Create", True, BLACK), (create_button.x + 20, create_button.y + 20))
    win.blit(font.render("Read", True, BLACK), (read_button.x + 20, read_button.y + 20))
    win.blit(font.render("Update", True, BLACK), (update_button.x + 20, update_button.y + 20))
    win.blit(font.render("Delete", True, BLACK), (delete_button.x + 20, delete_button.y + 20))
    
    return create_button, read_button, update_button, delete_button

# Function to open the Data Management window
def open_data_management():
    running = True
    input_active = False
    bandname_text = ""
    font = pygame.font.Font(None, 24)
    max_length = 20  # Maximum length of the input text
    cursor_visible = True
    cursor_position = len(bandname_text)
    cursor_timer = pygame.time.get_ticks()
    band_id = 1  # Initialize band_id
    
    while running:
        win.fill(WHITE)
        back_button = draw_back_button()
        create_button, read_button, update_button, delete_button = draw_crud_buttons()
        
        # Draw some basic UI elements
        title_font = pygame.font.Font(None, 36)
        text = title_font.render("Data Management", True, BLACK)
        win.blit(text, (WIDTH // 2 - 100, HEIGHT // 2 - 20))
        
        # Example form for creating a band
        bandname_label = font.render("Band Name:", True, BLACK)
        win.blit(bandname_label, (50, 100))
        bandname_input = pygame.Rect(200, 100, 200, 30)
        pygame.draw.rect(win, BLACK, bandname_input, 2)
        bandname_surface = font.render(bandname_text, True, BLACK)
        win.blit(bandname_surface, (bandname_input.x + 5, bandname_input.y + 5))
        
        # Draw the cursor
        if input_active and cursor_visible:
            cursor_x = bandname_input.x + 5 + font.size(bandname_text[:cursor_position])[0]
            pygame.draw.line(win, BLACK, (cursor_x, bandname_input.y + 5), (cursor_x, bandname_input.y + 25), 2)
        
        # Blink the cursor
        if pygame.time.get_ticks() - cursor_timer > 500:
            cursor_visible = not cursor_visible
            cursor_timer = pygame.time.get_ticks()
        
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if back_button.collidepoint(event.pos):
                    running = False
                if bandname_input.collidepoint(event.pos):
                    input_active = True
                else:
                    input_active = False
                if create_button.collidepoint(event.pos):
                    try:
                        band_service.create_band(band_id, bandname_text, "", "")
                        print(f"Band created successfully with ID: {band_id}")
                        band_id += 1  # Increment band_id for the next band
                    except Exception as e:
                        print(f"Error creating band: {e}")
                if read_button.collidepoint(event.pos):
                    try:
                        band = band_service.read_band(band_id - 1)  # Read the last created band
                        print(f"Band with ID {band_id - 1}: {band}")
                    except Exception as e:
                        print(f"Error reading band: {e}")
                if update_button.collidepoint(event.pos):
                    try:
                        band_service.update_band(band_id - 1, 1, bandname_text, "", "")
                        print(f"Band updated successfully with ID: {band_id - 1}")
                    except Exception as e:
                        print(f"Error updating band: {e}")
                if delete_button.collidepoint(event.pos):
                    try:
                        band_service.delete_band(band_id - 1)  # Delete the last created band
                        print(f"Band deleted successfully with ID: {band_id - 1}")
                        band_id -= 1  # Decrement band_id after deletion
                    except Exception as e:
                        print(f"Error deleting band: {e}")
            elif event.type == pygame.KEYDOWN:
                if input_active:
                    try:
                        if event.key == pygame.K_BACKSPACE:
                            if cursor_position > 0:
                                bandname_text = bandname_text[:cursor_position - 1] + bandname_text[cursor_position:]
                                cursor_position -= 1
                        elif event.key == pygame.K_DELETE:
                            if cursor_position < len(bandname_text):
                                bandname_text = bandname_text[:cursor_position] + bandname_text[cursor_position + 1:]
                        elif event.key == pygame.K_LEFT:
                            if cursor_position > 0:
                                cursor_position -= 1
                        elif event.key == pygame.K_RIGHT:
                            if cursor_position < len(bandname_text):
                                cursor_position += 1
                        elif len(bandname_text) < max_length:
                            bandname_text = bandname_text[:cursor_position] + event.unicode + bandname_text[cursor_position:]
                            cursor_position += 1
                    except Exception as e:
                        print(f"Error handling key event: {e}")

# Main loop
run = True
while run:
    win.fill(WHITE)
    data_management_button = draw_data_management_button()
    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if data_management_button.collidepoint(event.pos):
                open_data_management()

pygame.quit()
