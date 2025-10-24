import pygame
import math
import random
from pygame._sdl2 import Window, Texture

# Initialize
pygame.init()
WIDTH, HEIGHT = 1400, 750
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
font = pygame.font.SysFont("consolas", 20)

# Jet state
pos = pygame.Vector2(WIDTH // 2, HEIGHT // 2)
velocity = pygame.Vector2(0, 0)
angle = 0  # degrees
thrust = 0.2  # increased power
particles = []
lift_strength = 0.04
drag_coeff = 0.02  # stronger drag
gravity = pygame.Vector2(0, 0.3)
stall_threshold = 2.0
max_speed = 8.0

#classes

class Particle:
    def __init__(self, pos, velocity):
        self.pos = pygame.Vector2(pos)
        self.velocity = pygame.Vector2(velocity)
        self.life = 30  # frames
        self.size = 3

    def update(self):
        self.pos += self.velocity
        self.life -= 1
        self.size = max(1, self.size - 0.05)

    def draw(self, screen):
     radius = int(self.size)
     alpha = max(50, int(255 * (self.life / 60)))
     color = (180, 220, 255, alpha)

     particle_surf = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
     pygame.draw.circle(particle_surf, color, (radius, radius), radius)
     screen.blit(particle_surf, self.pos - pygame.Vector2(radius, radius))
     
# class Bullet :
    
#plane physiscs

def rotate_vector(vec, angle_deg):
    angle_rad = math.radians(angle_deg)
    return pygame.Vector2(
        vec.x * math.cos(angle_rad) - vec.y * math.sin(angle_rad),
        vec.x * math.sin(angle_rad) + vec.y * math.cos(angle_rad)
    )

def draw_hud():
    speed = velocity.length()
    altitude = HEIGHT - pos.y
    stall = speed < stall_threshold
    hud_lines = [
        f"Speed (mach): {(speed * 0.1):.2f}",
        f"Altitude: {altitude:.1f}",
        f"Angle: {angle:.1f}°",
        f"Stall: {'YES' if stall else 'NO'}",
        f"Thrust: {thrust:.1f}"
    ]
    for i, line in enumerate(hud_lines):
        color = (255, 100, 100) if "Stall" in line and "YES" in line else (200, 255, 200)
        text = font.render(line, True, color)
        screen.blit(text, (10, 10 + i * 25))

# Main loop
running = True
while running:
    screen.fill((30, 30, 30))
    
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Controls
    keys = pygame.key.get_pressed()
    if keys[pygame.K_RIGHT]: angle += 3
    if keys[pygame.K_LEFT]: angle -= 3
    if keys[pygame.K_UP]: 
        velocity += rotate_vector(pygame.Vector2(thrust, 0), angle)
        rear_offset = rotate_vector(pygame.Vector2(-20, 0), angle)
        rear_pos = pos + rear_offset
        exhaust_dir = rotate_vector(pygame.Vector2(-1, 0), angle)
        particle_velocity = exhaust_dir * thrust * 0.5 + velocity * 0.2
        print("Emitting particle")
        offset = pygame.Vector2(random.uniform(-2, 2), random.uniform(-2, 2))
        jitter = pygame.Vector2(random.uniform(-0.3, 0.3), random.uniform(-0.3, 0.3))
        particles.append(Particle(rear_pos + offset, particle_velocity + jitter))
        
    if keys[pygame.K_q]: thrust -= 0.01
    if keys[pygame.K_e]: thrust += 0.01
     
    max_speed = 8.0
    if thrust > 0.4 :
        thrust = 0.4
    if thrust < 0.2 :
        thrust = 0.2

    # Physics
    # Calculate forward direction and speed
    forward_dir = rotate_vector(pygame.Vector2(1, 0), angle)
    forward_speed = velocity.dot(forward_dir)

    # Stall detection
    stall = forward_speed < stall_threshold

    # Lift only applies when not stalled
    # Forward direction and speed
    forward_dir = rotate_vector(pygame.Vector2(1, 0), angle)
    forward_speed = velocity.dot(forward_dir)

    # Stall detection
    stall = forward_speed < stall_threshold

    if forward_dir.x < 0:  # facing left
     lift_dir = pygame.Vector2(-forward_dir.y, forward_dir.x)  # +90°
    else:
        lift_dir = pygame.Vector2(forward_dir.y, -forward_dir.x)  # −90°
    

    if velocity.length() > max_speed:
      velocity.scale_to_length(max_speed)


    # Lift magnitude based on forward speed
    lift = lift_dir * lift_strength * max(0, forward_speed) if not stall else pygame.Vector2(0, 0)
    lift = pygame.Vector2(0, lift.y)
    lift.x = 0  # Remove horizontal influence
    
    # Drag applies only to forward motion
    drag = -forward_dir * drag_coeff * forward_speed

    # Stall dampening
    if stall:
      velocity *= 0.96  # Gentle freeze

    # Apply forces
    velocity += gravity + lift + drag
    pos += velocity

    # Ground collision
    if pos.y > HEIGHT - 10:
        pos.y = HEIGHT - 10
        velocity.y = 0
        drag_coeff = 0.02
    elif pos.y < HEIGHT - 10:
        drag_coeff = 0.02


    # Edge teleportation
    if pos.x > WIDTH:
        pos.x = 0
    elif pos.x < 0:
        pos.x = WIDTH
        
    for p in particles[:]:
     p.update()
     p.draw(screen)
     if p.life <= 0:
       particles.remove(p)
     print(f"Particles: {len(particles)}")

    # Draw jet
    jet_points = [
        rotate_vector(pygame.Vector2(20, 0), angle),
        rotate_vector(pygame.Vector2(-10, 5), angle),
        rotate_vector(pygame.Vector2(-10, -5), angle)
    ]
    jet_points = [(pos + p) for p in jet_points]
    pygame.draw.polygon(screen, (200, 200, 255), jet_points)
    

    # Ground line
    pygame.draw.line(screen, (100, 255, 100), (0, HEIGHT - 10), (WIDTH, HEIGHT - 10), 2)

    # HUD
    draw_hud()

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
