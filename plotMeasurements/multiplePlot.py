import json
import matplotlib.pyplot as plt

# JSON fájl beolvasása
file_path = "max_PWM_measurements_short_distance/measures/m19_max_PWM_22.json"

data = []
with open(file_path, "r") as f:
    for line in f:
        data.append(json.loads(line.strip()))

# Koordináták kigyűjtése
timestamps = [float(entry["timestamp"]) for entry in data]
Po_x, Po_y = zip(*[entry["Po"] for entry in data])
Pb_x, Pb_y = zip(*[entry["Pb"] for entry in data])

# Közös határok kiszámítása
x_min = min(min(Po_x), min(Pb_x)) - 1
x_max = max(max(Po_x), max(Pb_x)) + 1
y_min = min(min(Po_y), min(Pb_y)) - 1
y_max = max(max(Po_y), max(Pb_y)) + 1

# 1. ábra - Po pontok
plt.figure(figsize=(6, 6))
plt.plot(Po_x, Po_y, 'bx-', label="Po pontok")
plt.xlabel("X koordináta")
plt.ylabel("Y koordináta")
plt.title("Po pontok ábrázolása")
plt.grid()
plt.legend()
plt.xlim(x_min, x_max)
plt.ylim(y_min, y_max)
plt.savefig("plot_m19_1_Po.png", dpi=300, bbox_inches="tight")
plt.close()

# 2. ábra - Pb pontok
plt.figure(figsize=(6, 6))
plt.plot(Pb_x, Pb_y, 'rx-', label="Pb pontok")
plt.xlabel("X koordináta")
plt.ylabel("Y koordináta")
plt.title("Pb pontok ábrázolása")
plt.grid()
plt.legend()
plt.xlim(x_min, x_max)
plt.ylim(y_min, y_max)
plt.savefig("plot_m19_2_Pb.png", dpi=300, bbox_inches="tight")
plt.close()


# 3. ábra - Xo idő függvényében
plt.figure(figsize=(8, 4))
plt.plot(timestamps, Po_x, 'b.-', label="Xo")
plt.xlabel("Idő [s]")
plt.ylabel("Xo koordináta")
plt.title("Xo idő függvényében")
plt.grid()
plt.legend()
plt.savefig("plot_m19_3_Xo_vs_time.png", dpi=300, bbox_inches="tight")
plt.close()

# 4. ábra - Yo idő függvényében
plt.figure(figsize=(8, 4))
plt.plot(timestamps, Po_y, 'g.-', label="Yo")
plt.xlabel("Idő [s]")
plt.ylabel("Yo koordináta")
plt.title("Yo idő függvényében")
plt.grid()
plt.legend()
plt.savefig("plot_m19_4_Yo_vs_time.png", dpi=300, bbox_inches="tight")
plt.close()

# 5. ábra - Xb idő függvényében
plt.figure(figsize=(8, 4))
plt.plot(timestamps, Pb_x, 'r.-', label="Xb")
plt.xlabel("Idő [s]")
plt.ylabel("Xb koordináta")
plt.title("Xb idő függvényében")
plt.grid()
plt.legend()
plt.savefig("plot_m19_5_Xb_vs_time.png", dpi=300, bbox_inches="tight")
plt.close()

# 6. ábra - Yb idő függvényében
plt.figure(figsize=(8, 4))
plt.plot(timestamps, Pb_y, 'm.-', label="Yb")
plt.xlabel("Idő [s]")
plt.ylabel("Yb koordináta")
plt.title("Yb idő függvényében")
plt.grid()
plt.legend()
plt.savefig("plot_m19_6_Yb_vs_time.png", dpi=300, bbox_inches="tight")
plt.close()
