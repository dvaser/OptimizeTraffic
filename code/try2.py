import matplotlib.pyplot as plt

# Verilen noktalar
points = [
    (310.20183999999995, 317.66898000000003),
    (384.26176000000004, 433.94703),
    (485.16842, 437.40704000000005),
    (535.18832, 294.01071),
    (283.22880000000004, 431.05976)
]

# Noktaları çizme
x, y = zip(*points)
plt.scatter(x, y, color='blue')

# Her noktayı etiketleme
for i, (x_val, y_val) in enumerate(points):
    plt.text(x_val, y_val, f'({x_val:.2f}, {y_val:.2f})', fontsize=9, ha='right')

# Grafik başlığı ve eksen etiketleri
plt.title('Points Plot')
plt.xlabel('X Coordinate')
plt.ylabel('Y Coordinate')

# Eksenleri göster
plt.grid(True)
plt.axhline(y=0, color='k')
plt.axvline(x=0, color='k')

# Görselleştirme
plt.show()