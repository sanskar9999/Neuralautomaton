import pygame
import sys
import numpy as np

# --- Simulation Parameters (Updated) ---
MATRIX_WIDTH = 1280
MATRIX_HEIGHT = 720
THRESHOLD = 1.0  # Potential level at which neuron fires
FLUCTUATION_AMOUNT = 0.01 # Max random potential added each frame
RELEASE_ENERGY = 0.9 # Amount of energy released by a firing neuron TO BE DISTRIBUTED (use float)
NEIGHBOR_COUPLING = 0.8 # Percentage of released energy distributed to neighbors (total) (use float)
RESET_POTENTIAL_LOW = 0.0
RESET_POTENTIAL_HIGH = 0.1

# --- Interaction Parameters (Updated) ---
CLICK_RADIUS = 200 # Radius around the click center (0 for 1x1, 1 for 3x3, 2 for 5x5, etc.)

# --- Pygame Setup ---
pygame.init()
infoObject = pygame.display.Info()
screen_width = infoObject.current_w
screen_height = infoObject.current_h
screen = pygame.display.set_mode((screen_width, screen_height), pygame.FULLSCREEN)
pygame.display.set_caption("Interactive Neural Grid Simulation (8 Neighbors, L Click / X Key)")

# --- Initialize Neuron State ---
# Ensure shape is (height, width) for consistency with image processing / array indexing
neuron_potential = np.random.uniform(RESET_POTENTIAL_LOW, RESET_POTENTIAL_HIGH,
                                     size=(MATRIX_HEIGHT, MATRIX_WIDTH)).astype(np.float32)

# --- Main Loop ---
running = True
clock = pygame.time.Clock() # Use clock to see FPS

while running:
    # --- Event Handling ---
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            # --- Add X Key Handling ---
            if event.key == pygame.K_x:
                # Get current mouse position (screen coordinates)
                mouse_x, mouse_y = pygame.mouse.get_pos()

                # Convert screen coordinates to matrix indices
                matrix_x = int((mouse_x / screen_width) * MATRIX_WIDTH)
                matrix_y = int((mouse_y / screen_height) * MATRIX_HEIGHT)

                # Define the area boundaries based on CLICK_RADIUS
                y_start = max(0, matrix_y - CLICK_RADIUS)
                y_end = min(MATRIX_HEIGHT, matrix_y + CLICK_RADIUS + 1)
                x_start = max(0, matrix_x - CLICK_RADIUS)
                x_end = min(MATRIX_WIDTH, matrix_x + CLICK_RADIUS + 1)

                # Set the potential in the defined area to the minimum (suppress)
                neuron_potential[y_start:y_end, x_start:x_end] = RESET_POTENTIAL_LOW

        # --- Mouse Click Handling (Left Click Only) ---
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Check if it's the left mouse button (button 1)
            if event.button == 1:
                # Get mouse position (screen coordinates)
                mouse_x, mouse_y = event.pos

                # Convert screen coordinates to matrix indices
                matrix_x = int((mouse_x / screen_width) * MATRIX_WIDTH)
                matrix_y = int((mouse_y / screen_height) * MATRIX_HEIGHT)

                # Define the area boundaries based on CLICK_RADIUS
                y_start = max(0, matrix_y - CLICK_RADIUS)
                y_end = min(MATRIX_HEIGHT, matrix_y + CLICK_RADIUS + 1)
                x_start = max(0, matrix_x - CLICK_RADIUS)
                x_end = min(MATRIX_WIDTH, matrix_x + CLICK_RADIUS + 1)

                # Set the potential in the defined area to the threshold (excite)
                neuron_potential[y_start:y_end, x_start:x_end] = THRESHOLD


    # --- Simulation Step ---

    # 1. Add Random Fluctuations
    fluctuations = np.random.uniform(0, FLUCTUATION_AMOUNT, size=neuron_potential.shape).astype(np.float32)
    neuron_potential += fluctuations

    # 2. Identify Firing Neurons
    fired_mask = neuron_potential >= THRESHOLD

    # 3. Calculate Energy Transfer from Firing Neighbors (8 NEIGHBORS)
    padded_fired_mask = np.pad(fired_mask, ((1, 1), (1, 1)), mode='wrap')

    # Cardinal Neighbors
    neighbor_fired_up = padded_fired_mask[0:-2, 1:-1]
    neighbor_fired_down = padded_fired_mask[2:, 1:-1]
    neighbor_fired_left = padded_fired_mask[1:-1, 0:-2]
    neighbor_fired_right = padded_fired_mask[1:-1, 2:]
    # Diagonal Neighbors
    neighbor_fired_up_left = padded_fired_mask[0:-2, 0:-2]
    neighbor_fired_up_right = padded_fired_mask[0:-2, 2:]
    neighbor_fired_down_left = padded_fired_mask[2:, 0:-2]
    neighbor_fired_down_right = padded_fired_mask[2:, 2:]

    # Sum the boolean masks (True=1, False=0) to count all 8 firing neighbors
    firing_neighbor_count = (neighbor_fired_up + neighbor_fired_down +
                             neighbor_fired_left + neighbor_fired_right +
                             neighbor_fired_up_left + neighbor_fired_up_right +
                             neighbor_fired_down_left + neighbor_fired_down_right)

    # Calculate energy received by each neuron, DIVIDING BY 8
    energy_per_neighbor = (RELEASE_ENERGY * NEIGHBOR_COUPLING) / 8.0
    potential_increase = firing_neighbor_count * energy_per_neighbor

    # Add the received energy to the potential
    neuron_potential += potential_increase.astype(np.float32)

    # 4. Reset Firing Neurons
    num_fired = np.sum(fired_mask)
    if num_fired > 0:
        reset_values = np.random.uniform(RESET_POTENTIAL_LOW, RESET_POTENTIAL_HIGH, size=num_fired).astype(np.float32)
        neuron_potential[fired_mask] = reset_values

    # --- Visualization ---
    vis_potential = np.clip(neuron_potential, 0, THRESHOLD)
    gray_values = (vis_potential / THRESHOLD * 255).astype(np.uint8)
    pixel_array_rgb = np.repeat(gray_values[:, :, np.newaxis], 3, axis=2)
    pixel_array_transposed = np.transpose(pixel_array_rgb, (1, 0, 2))

    # --- Pygame Drawing ---
    temp_matrix_surface = pygame.surfarray.make_surface(pixel_array_transposed)
    scaled_surface = pygame.transform.scale(temp_matrix_surface, (screen_width, screen_height))
    screen.blit(scaled_surface, (0, 0))
    pygame.display.flip()

    # Print FPS to console
    # print(f"FPS: {clock.get_fps():.2f}")
    clock.tick() # Limit framerate slightly if needed, or just measure

# --- Cleanup ---
pygame.quit()
sys.exit()
