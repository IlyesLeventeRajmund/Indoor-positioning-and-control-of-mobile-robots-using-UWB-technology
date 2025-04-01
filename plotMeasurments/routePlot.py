import json
import matplotlib.pyplot as plt

# JSON fájl beolvasása
file_path = "thrid_measurement_line_log.json" 

data = []
with open(file_path, "r") as f:
    for line in f:
        data.append(json.loads(line.strip()))

# Koordináták kigyűjtése
Po_x, Po_y = zip(*[entry["Po"] for entry in data])
Pb_x, Pb_y = zip(*[entry["Pb"] for entry in data])


print(f"Pb_x min: {min(Pb_x)}, Pb_x max: {max(Pb_x)}")
print(f"Pb_y min: {min(Pb_y)}, Pb_y max: {max(Pb_y)}")

# Diagram rajzolása
plt.figure(figsize=(8, 6))
plt.plot(Pb_x, Pb_y, label="Pb útvonal", color="red", alpha=0.5)
plt.plot(Po_x, Po_y, label="Po útvonal", color="blue", alpha=0.5)
plt.xlabel("X koordináta")
plt.ylabel("Y koordináta")
plt.legend()
plt.title("Két útvonal ábrázolása")
plt.grid()
plt.xlim(min(min(Po_x), min(Pb_x)) - 1, max(max(Po_x), max(Pb_x)) + 1)
plt.ylim(min(min(Po_y), min(Pb_y)) - 1, max(max(Po_y), max(Pb_y)) + 1)
plt.show()
plt.savefig("output.png")
