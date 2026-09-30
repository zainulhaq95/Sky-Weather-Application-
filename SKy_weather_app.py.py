import tkinter as tk
import requests
import math
import random

API_KEY = "0e3cfce85b87987382d3be806b871f6a"

root = tk.Tk()
root.title("Sky Weather")
root.geometry("1800x1000")

canvas = tk.Canvas(root, highlightthickness=0)
canvas.pack(fill="both", expand=True)

WIDTH, HEIGHT = 1800, 1000

# ---------- SKY GRADIENT ----------
gradient_colors = ["#4facfe", "#6ec6ff", "#9dd9ff", "#cfefff"]
for i, color in enumerate(gradient_colors):
    canvas.create_rectangle(
        0, i * (HEIGHT // 4),
        WIDTH, (i + 1) * (HEIGHT // 4),
        fill=color, outline=""
    )

# ---------- SUN ----------
sun_x, sun_y = WIDTH - 220, 180
sun = canvas.create_oval(
    sun_x - 70, sun_y - 70,
    sun_x + 70, sun_y + 70,
    fill="#FFD54F", outline=""
)
sun_rays = []
angle = 0

def animate_sun():
    global angle
    for r in sun_rays:
        canvas.delete(r)
    sun_rays.clear()

    for i in range(16):
        a = angle + i * 22.5
        x1 = sun_x + 80 * math.cos(math.radians(a))
        y1 = sun_y + 80 * math.sin(math.radians(a))
        x2 = sun_x + 120 * math.cos(math.radians(a))
        y2 = sun_y + 120 * math.sin(math.radians(a))
        sun_rays.append(
            canvas.create_line(x1, y1, x2, y2, fill="#FFB300", width=4)
        )
    angle += 2
    root.after(60, animate_sun)

# ---------- CLOUDS ----------
clouds = []
for i in range(6):
    size = random.randint(90, 150)
    y = random.randint(200, 500)
    speed = random.uniform(0.5, 1.5)
    cloud = canvas.create_text(
        random.randint(-300, WIDTH),
        y,
        text="☁️",
        font=("Arial", size)
    )
    clouds.append((cloud, speed))

def animate_clouds():
    for cloud, speed in clouds:
        x, y = canvas.coords(cloud)
        x += speed
        if x > WIDTH + 200:
            x = -300
        canvas.coords(cloud, x, y)
    root.after(40, animate_clouds)

# ---------- BIRDS ----------
birds = []
for _ in range(4):
    bird = canvas.create_text(
        random.randint(0, WIDTH),
        random.randint(150, 350),
        text="🕊️",
        font=("Arial", 36)
    )
    birds.append(bird)

def animate_birds():
    for b in birds:
        canvas.move(b, 2.5, -0.3)
        if canvas.coords(b)[0] > WIDTH + 50:
            canvas.coords(b, -50, random.randint(150, 350))
    root.after(50, animate_birds)

# ---------- FLOATING LIGHT ----------
particles = []
for _ in range(40):
    x = random.randint(0, WIDTH)
    y = random.randint(HEIGHT // 2, HEIGHT)
    p = canvas.create_oval(x, y, x + 4, y + 4, fill="white", outline="")
    particles.append(p)

def animate_particles():
    for p in particles:
        canvas.move(p, 0, -0.7)
        if canvas.coords(p)[1] < 0:
            canvas.coords(
                p,
                random.randint(0, WIDTH),
                HEIGHT,
                random.randint(0, WIDTH) + 4,
                HEIGHT + 4
            )
    root.after(50, animate_particles)

# ---------- GLASS CARD ----------
canvas.create_rectangle(
    WIDTH//2 - 420, HEIGHT//2 - 220,
    WIDTH//2 + 420, HEIGHT//2 + 260,
    fill="#000000", stipple="gray25", outline=""
)

canvas.create_rectangle(
    WIDTH//2 - 400, HEIGHT//2 - 240,
    WIDTH//2 + 400, HEIGHT//2 + 240,
    fill="white", outline=""
)

result_text = canvas.create_text(
    WIDTH//2, HEIGHT//2 + 30,
    text="",
    font=("Verdana", 20, "bold"),
    fill="black",
    width=700,
    justify="center"
)

# ---------- INPUT ----------
city_entry = tk.Entry(root, font=("Verdana", 20), justify="center")
canvas.create_window(WIDTH//2, 90, window=city_entry, width=420)

btn = tk.Button(
    root,
    text="GET WEATHER",
    font=("Verdana", 18, "bold"),
    bg="#42a5f5",
    fg="black",
    padx=30,
    pady=8,
    command=lambda: get_weather()
)
canvas.create_window(WIDTH//2, 155, window=btn)

# ---------- WEATHER ----------
def format_weather(data, title):
    condition = data["weather"][0]["description"]
    temp_f = data["main"]["temp"]
    temp_c = (temp_f - 32) * 5 / 9
    return f"{title}\n{condition.capitalize()}\n{temp_f:.1f}°F | {temp_c:.1f}°C"

def get_weather():
    city = city_entry.get()
    try:
        today = requests.get(
            "https://api.openweathermap.org/data/2.5/weather",
            params={"q": city, "APPID": API_KEY, "units": "imperial"}
        ).json()

        if today.get("cod") != 200:
            canvas.itemconfig(result_text, text="City not found")
            return

        forecast = requests.get(
            "https://api.openweathermap.org/data/2.5/forecast",
            params={
                "lat": today["coord"]["lat"],
                "lon": today["coord"]["lon"],
                "APPID": API_KEY,
                "units": "imperial"
            }
        ).json()

        tomorrow = forecast["list"][8]

        canvas.itemconfig(
            result_text,
            text=format_weather(today, "TODAY")
            + "\n\n"
            + format_weather(tomorrow, "TOMORROW")
        )

    except:
        canvas.itemconfig(result_text, text="Error fetching weather")

animate_sun()
animate_clouds()
animate_particles()
animate_birds()

root.mainloop()
