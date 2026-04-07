from geopy.distance import geodesic

def optimize_route(group):
    if len(group) <= 1:
        return group

    route = []
    remaining = group.copy()

    # Start from first passenger
    current = remaining.pop(0)
    route.append(current)

    while remaining:
        # Find nearest passenger
        next_p = min(
            remaining,
            key=lambda x: geodesic(
                (current['lat'], current['lon']),
                (x['lat'], x['lon'])
            ).km
        )

        route.append(next_p)
        remaining.remove(next_p)
        current = next_p

    return route