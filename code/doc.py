# Verilen yolo_classes_counts listesi
yolo_classes_counts = [
    [5, 2, 2, 2],
    [5, 2],
    [5, 2, 2],
    [2, 2, 2],
    [2, 2],
    [2, 2,2],
    [2,5,2,2],
    [2,2,2]
]

# Ka� tane alt listede 5 oldu?unu hesapla
count_lists_with_5 = sum(1 for sublist in yolo_classes_counts if 5 in sublist)
total_lists = len(yolo_classes_counts)

# 5 olan alt listelerin toplam liste say?s?na oran?
ratio_of_lists_with_5 = count_lists_with_5 / total_lists

# Her alt listede 2 s?n?f?n?n ka� tane oldu?unun ortalamas?n? hesapla
total_2_counts = sum(sublist.count(2) for sublist in yolo_classes_counts)
average_2_per_list = total_2_counts / total_lists

# Sonu�lar? yazd?r
print(f"Ratio of lists with 5: {(ratio_of_lists_with_5+.5)}")
print(f"Average count of 2 per list: {int(average_2_per_list+.5)}")

