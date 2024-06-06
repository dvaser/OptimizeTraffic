import numpy as np

# Nokta koordinatları (x, y)
points = [(439.43, 327.79), (434.51, 263.85), (539.54, 240.35), (639.33, 123.93)]

def isThere_same_lane(midpoint_1, midpoint_2, tolerance=30):
    return abs(midpoint_1 - midpoint_2) <= tolerance

def group_points_by_y(points, tolerance=30):
    groups = []
    for point in points:
        added = False
        for group in groups:
            if isThere_same_lane(midpoint_1=point[1], midpoint_2=group[0][1], tolerance=tolerance):
                group.append(point)
                added = True
                break
        if not added:
            groups.append([point])
    return len(groups), groups


sequences_count, grouped_points = group_points_by_y(points, tolerance=30)

print("Number of sequences:", sequences_count)
print("Grouped points by Y:", grouped_points)
