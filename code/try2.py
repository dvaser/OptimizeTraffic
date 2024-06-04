import itertools

def euclidean_distance(point1, point2):
    return ((point1[0] - point2[0])**2 + (point1[1] - point2[1])**2)**0.5

def calculate_tolerances(points):
    tolerances = []
    for pair in itertools.combinations(points, 2):
        point1, point2 = pair
        print(point1, point2)
        distance = euclidean_distance(point1, point2)
        print(distance)
        tolerances.append(distance)
    return tolerances

# Verilen noktalar
points = [
    (310.20183999999995, 317.66898000000003),
    (384.26176000000004, 433.94703),
    (485.16842, 437.40704000000005),
    (535.18832, 294.01071),
    (283.22880000000004, 431.05976)
]

# Toleransları hesapla
toleranslar = calculate_tolerances(points)
