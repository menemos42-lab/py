
import math
import os

# --- 1. GAME SETTINGS ---
SCREEN_WIDTH = 60
SCREEN_HEIGHT = 20
FOV = math.pi / 3  # 60 degrees field of view

# --- 2. THE 2D MAP ---
# 1 = Wall, 0 = Empty Space
# The map is basically viewed from top-down
game_map = [
    "111111111111111",
    "100000100000001",
    "101110101111101",
    "100010000000001",
    "101011111011111",
    "101000000000001",
    "111111111111111"
]

# --- 3. THE PLAYER ---
player_x = 2.0
player_y = 2.0
player_angle = 0.0  # Facing right (0 radians)

# --- 4. THE 3D RENDERING ENGINE ---
def render_3d_view():
    screen = [[" " for _ in range(SCREEN_WIDTH)] for _ in range(SCREEN_HEIGHT)]
    
    # Cast a ray for every single column on the screen
    for x in range(SCREEN_WIDTH):
        # Calculate the angle of the current ray
        ray_angle = (player_angle - FOV / 2.0) + (float(x) / float(SCREEN_WIDTH)) * FOV
        
        # Ray direction vectors
        eye_x = math.cos(ray_angle)
        eye_y = math.sin(ray_angle)
        
        distance_to_wall = 0.0
        hit_wall = False
        
        # Move the ray forward until it hits a wall
        while not hit_wall and distance_to_wall < 15.0:
            distance_to_wall += 0.1
            
            # Calculate the ray's current position
            test_x = int(player_x + eye_x * distance_to_wall)
            test_y = int(player_y + eye_y * distance_to_wall)
            
            # Check if the ray is out of bounds
            if test_x < 0 or test_x >= len(game_map[0]) or test_y < 0 or test_y >= len(game_map):
                hit_wall = True
                distance_to_wall = 15.0
            # Check if the ray hit a wall block ('1')
            elif game_map[test_y][test_x] == '1':
                hit_wall = True

        # Correct "fish-eye" lens distortion
        distance_to_wall *= math.cos(ray_angle - player_angle)
        
        # Calculate ceiling and floor heights
        ceiling = int(float(SCREEN_HEIGHT / 2.0) - SCREEN_HEIGHT / float(distance_to_wall))
        floor = SCREEN_HEIGHT - ceiling
        
        # Draw the vertical column on the screen
        for y in range(SCREEN_HEIGHT):
            if y < ceiling:
                screen[y][x] = " " # Sky
            elif y > ceiling and y <= floor:
                # Shade the wall based on distance
                if distance_to_wall <= 2.0:
                    screen[y][x] = "█"
                elif distance_to_wall < 5.0:
                    screen[y][x] = "▓"
                elif distance_to_wall < 8.0:
                    screen[y][x] = "▒"
                else:
                    screen[y][x] = "░"
            else:
                screen[y][x] = "." # Floor

    # Print the screen to the terminal
    os.system('cls' if os.name == 'nt' else 'clear')
    for row in screen:
        print("".join(row))

# Run the renderer once
render_3d_view()
