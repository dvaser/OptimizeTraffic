roads = {
            "road1":{
                "vehicle1":42,
                "vehicle2":35,
                "vehicle5":22
            },
            "road2":{
                "vehicle3":62,
                "vehicle4":55
            }
        }

for road in roads:
    for v in roads[road]:
        print(roads[road][v])