import ISS_Info
import turtle
import time
from tkinter import *
from tkinter import scrolledtext
import threading
import math
import random

# Planet characteristics
planet_info = {
    "Mercury": "Mercury: Small, rocky planet closest to the Sun.",
    "Venus": "Venus: Hot, thick atmosphere, second planet from the Sun.",
    "Earth": "Earth: Home planet with life, water, and a breathable atmosphere.",
    "Mars": "Mars: Red planet with evidence of past water and potential for life.",
    "Jupiter": "Jupiter: Gas giant with a Great Red Spot, the largest planet.",
    "Saturn": "Saturn: Gas giant known for its beautiful ring system.",
    "Uranus": "Uranus: Ice giant with a tilted rotation and faint rings.",
    "Neptune": "Neptune: Ice giant with strong winds and the farthest planet."
}

# Function to update ISS location on the map
def update_iss_position(iss_turtle):
    while True:
        location = ISS_Info.iss_current_loc()
        lat = location['iss_position']['latitude']
        lon = location['iss_position']['longitude']
        print(f"Position: latitude: {lat}, longitude: {lon}")
        iss_turtle.goto(float(lon), float(lat))
        time.sleep(5)

# Function for the AI assistant
def ai_assistant():
    user_input = ai_input.get()
    if user_input.strip():
        ai_chat.insert(END, "User: " + user_input + "\n")
        ai_chat.insert(END, "AI: How can I help you with that?\n")
    ai_input.delete(0, END)

# Function to simulate planetary orbits
def simulate_planets(planet_turtles, sun_turtle, radii, speeds):
    while True:
        for i, planet in enumerate(planet_turtles):
            angle = time.time() * speeds[i]  # Dynamic angle for orbit
            x = radii[i] * math.cos(angle)
            y = radii[i] * math.sin(angle)
            planet.goto(x, y)
        time.sleep(0.05)  # Delay for smooth animation

# Function to animate stars (twinkling effect)
def animate_stars(star_turtles):
    while True:
        for star in star_turtles:
            star.shapesize(random.uniform(0.1, 0.3))  # Random star size
        time.sleep(0.5)  # Twinkling speed

# Function to display planet information on click
def planet_click_handler(planet_name):
    ai_chat.insert(END, f"{planet_name}: {planet_info[planet_name]}\n")

# Click and drag functionality for solar system view
def start_drag(event):
    global last_drag_x, last_drag_y
    last_drag_x = event.x
    last_drag_y = event.y

def drag_move(event):
    global last_drag_x, last_drag_y
    dx = event.x - last_drag_x
    dy = event.y - last_drag_y
    solar_canvas.xview_scroll(int(-dx / 2), "units")
    solar_canvas.yview_scroll(int(-dy / 2), "units")
    last_drag_x = event.x
    last_drag_y = event.y

# Setup the main Tkinter window
root = Tk()
root.title("AI and ISS Tracker with Space Simulation")
root.geometry("1200x700")  # Adjust the window size as needed
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)

# Add title label at the top
title_label = Label(root, text="VOYAGEVERSE AI", font=("Arial", 24), bg="black", fg="white")
title_label.grid(row=0, column=0, columnspan=2, pady=(10, 0), sticky="nsew")

# Left side: AI assistant bot occupying full left side, top to bottom
ai_frame = Frame(root, width=600, height=600)
ai_frame.grid(row=1, column=0, rowspan=2, padx=10, pady=10, sticky="nsew")

ai_label = Label(ai_frame, text="AI ASSISTANT", font=("Arial", 16))
ai_label.pack(pady=10)

ai_chat = scrolledtext.ScrolledText(ai_frame, wrap=WORD, width=60, height=30)
ai_chat.pack(pady=10, padx=10)

ai_input = Entry(ai_frame, width=50)
ai_input.pack(pady=(0, 10), anchor="center")

send_button = Button(ai_frame, text="Send", command=ai_assistant)
send_button.pack(pady=(0, 10), anchor="center")

# Right side: ISS map and planetary simulation
right_frame = Frame(root, width=600, height=600)
right_frame.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")

# Embed turtle graphics for ISS map (upper half of right side)
canvas = Canvas(right_frame, width=600, height=300)
canvas.pack(padx=10, pady=10)

screen = turtle.TurtleScreen(canvas)
screen.bgcolor("black")  # Black sky background
screen.setworldcoordinates(-180, -90, 180, 90)
screen.bgpic("world.png")
screen.register_shape("iss.gif")

iss_turtle = turtle.RawTurtle(screen)
iss_turtle.shape("iss.gif")
iss_turtle.penup()


# Space simulation (solar system view with black sky and stars)
solar_canvas = Canvas(right_frame, width=600, height=300, bg='black')
solar_canvas.pack(padx=10, pady=10)

# Create a TurtleScreen on the solar canvas
solar_screen = turtle.TurtleScreen(solar_canvas)
solar_screen.bgcolor("black")  # Black sky for space simulation

# Create Sun and planets
sun_turtle = turtle.RawTurtle(solar_screen)
sun_turtle.shape("circle")
sun_turtle.color("yellow")
sun_turtle.shapesize(2.5)  # Smaller sun size to fit the space
sun_turtle.penup()
sun_turtle.goto(0, 0)

# Planet properties for all 8 planets
planet_names = ["Mercury", "Venus", "Earth", "Mars", "Jupiter", "Saturn", "Uranus", "Neptune"]
planet_colors = ["gray", "orange", "blue", "red", "brown", "gold", "lightblue", "darkblue"]
radii = [50, 80, 110, 150, 200, 260, 330, 400]  # Larger orbital radii to avoid overlap
speeds = [0.02, 0.017, 0.015, 0.012, 0.009, 0.007, 0.005, 0.003]  # Orbital speeds

planet_turtles = []
for i, color in enumerate(planet_colors):
    planet = turtle.RawTurtle(solar_screen)
    planet.shape("circle")
    planet.color(color)
    planet.shapesize(1.0)  # Scaled down planet size
    planet.penup()
    planet.goto(radii[i], 0)
    planet.onclick(lambda x, y, name=planet_names[i]: planet_click_handler(name))
    planet_turtles.append(planet)

# Create stars for the background (twinkling stars) across full canvas
star_turtles = []
for _ in range(10,50):  # Add more stars for full coverage
    star = turtle.RawTurtle(solar_screen)
    star.shape("circle")
    star.color("white")
    star.penup()
    star.goto(random.randint(-300, 300), random.randint(-200, 200))  # Cover larger area
    star_turtles.append(star)

# Initialize dragging
last_drag_x = 0
last_drag_y = 0
solar_canvas.bind("<ButtonPress-1>", start_drag)
solar_canvas.bind("<B1-Motion>", drag_move)

# Start the thread for space simulation (planet orbits)
threading.Thread(target=simulate_planets, args=(planet_turtles, sun_turtle, radii, speeds), daemon=True).start()

# Start the thread to animate twinkling stars
threading.Thread(target=animate_stars, args=(star_turtles,), daemon=True).start()

# Start the thread to update ISS position
threading.Thread(target=update_iss_position, args=(iss_turtle,), daemon=True).start()

root.mainloop()
