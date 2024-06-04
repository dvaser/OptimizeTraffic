import numpy as np


def cluster_and_average_positions(tensor_list, tolerance=1.5, threshold=0.6):
    all_positions = []
    position_indices = []
    
    for i, tensor in enumerate(tensor_list):
        for pos in tensor:
            all_positions.append(pos)
            position_indices.append(i)
    
    clusters = []
    cluster_indices = []
    
    for position, index in zip(all_positions, position_indices):
        added_to_cluster = False
        for cluster, indices in zip(clusters, cluster_indices):
            if all(np.linalg.norm(np.array(position[:2]) - np.array(p[:2])) <= tolerance for p in cluster):
                cluster.append(position)
                indices.append(index)
                added_to_cluster = True
                break
        if not added_to_cluster:
            clusters.append([position])
            cluster_indices.append([index])
    
    averaged_positions = []
    total_detections = len(tensor_list)
    
    for cluster, indices in zip(clusters, cluster_indices):
        unique_indices = set(indices)
        detection_ratio = len(unique_indices) / total_detections
        if detection_ratio >= threshold:
            averaged_positions.append(np.mean(cluster, axis=0).tolist())
    
    return averaged_positions

""" x-+2 , y+2, w, h 
    1 amb
    4 car
"""
tensor_listesi = [
    [[276.0064, 275.9860, 67.8746, 83.7976],
     [343.9008, 373.9061, 80.5873, 120.9159],
     [446.9678, 377.7187, 75.6280, 119.8892],
     [473.5276, 186.3598, 122.9483, 216.4189],
     [237.8894, 372.7906, 91.2600, 118.7218]],

    [[343.8509, 373.7438, 80.5663, 120.6278],
     [276.3301, 275.8190, 67.6848, 83.5477],
     [237.7415, 372.4804, 90.2802, 117.8807],
     [447.1500, 377.3181, 75.4026, 119.9342],
     [474.0717, 186.4323, 123.0658, 215.0797]],

    [[344.0958, 373.2687, 80.5530, 120.5484],
     [276.3773, 275.8329, 67.9901, 83.7909],
     [447.4504, 377.3491, 75.7582, 120.3806],
     [237.8002, 371.9057, 90.3795, 117.1572],
     [473.7798, 186.1714, 122.8169, 215.6604],
     [371.5843, 249.6223, 71.3289, 143.5029]],

    [[344.1304, 373.3636, 80.2862, 121.2791],
     [276.2400, 275.6642, 67.7968, 83.7601],
     [447.5094, 377.2227, 75.7848, 120.0023],
     [237.9262, 371.7857, 90.3297, 117.8553],
     [473.7606, 186.2264, 122.4276, 215.4084],
     [552.3195, 354.0804, 80.2451, 110.5771]],

    [[344.1765, 373.0709, 80.3160, 121.3929],
     [276.3173, 275.6220, 68.1299, 83.9453],
     [473.7011, 185.3079, 122.9430, 216.5441],
     [447.5656, 377.2530, 75.8242, 120.1409],
     [238.1079, 371.7465, 91.1082, 117.5648],
     [552.9117, 353.7159, 81.0466, 110.5076],
     [552.7144, 353.4789, 80.4604, 110.3679],
     [373.6734, 280.5805, 64.8948, 83.3787]]
]

ortalama_konumlar = cluster_and_average_positions(tensor_listesi)

# for i in ortalama_konumlar:
#     print(i)

# Adım 4: Orta nokta hesaplama
def orta_nokta_hesapla(x, y, w, h):
    orta_x = x + (w / 2)
    orta_y = y + (h / 2)
    return orta_x, orta_y

orta_noktalar = []
for konum in ortalama_konumlar:
    x, y, w, h = konum
    orta_x, orta_y = orta_nokta_hesapla(x, y, w, h)
    orta_noktalar.append((orta_x, orta_y))

# for i in orta_noktalar:
#     print(i)

# Adım 5: Aynı hizada olan araçları bulma
def ayni_hizadami(orta_nokta1, orta_nokta2, tolerans):
    return abs(orta_nokta1[1] - orta_nokta2[1]) <= tolerans

tolerans = 30
aynı_hizadaki_gruplar = []
for i, nokta1 in enumerate(orta_noktalar):
    grup = []
    for nokta2 in orta_noktalar[i+1:]:
        if ayni_hizadami(nokta1, nokta2, tolerans):
            grup.append(nokta2)
    if grup:
        grup.append(nokta1)
        aynı_hizadaki_gruplar.append(grup)

if aynı_hizadaki_gruplar:
    en_buyuk_grup = max(aynı_hizadaki_gruplar, key=len)
    aynı_hizadaki_arac_sayisi = len(en_buyuk_grup)
else:
    aynı_hizadaki_arac_sayisi = 0

# Adım 6: Sıra sayısı belirleme
orta_noktalar.sort(key=lambda orta_nokta: orta_nokta[1])

sira_sayisi = 1
for i in range(1, len(orta_noktalar)):
    if orta_noktalar[i][1] - orta_noktalar[i - 1][1] > tolerans:
        sira_sayisi += 1

print(f"Yaklaşık aynı hizada {aynı_hizadaki_arac_sayisi} araç var.")
print(f"Araçlar {sira_sayisi} sıra halinde.")







