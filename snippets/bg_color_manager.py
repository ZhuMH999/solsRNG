import time

_sky_blue = (135, 206, 235)
_night_purple = (30, 0, 60)

def _lerp(a, b, t):
    return int(a + (b - a) * t)

def _interpolate_color(c1, c2, t):
    return (
        _lerp(c1[0], c2[0], t),
        _lerp(c1[1], c2[1], t),
        _lerp(c1[2], c2[2], t),
    )

def return_interpolated_color(next_switch_time, current_time):
    time_until = max(round(next_switch_time - time.time(), 2), 0)
    time_since = min(round(time.time() - (next_switch_time - 150), 2), 150)

    if 15 <= time_until <= 135:
        return _sky_blue if current_time == 12 else _night_purple

    if 135 <= time_since <= 150:
        t = (15 - time_until) / 30
    else:
        t = (15 + time_since) / 30

    # Interpolate depending on direction
    if (current_time == 12 and time_since >= 135) or (current_time == 13 and time_since <= 15):  # day → fading to night
        return _interpolate_color(_sky_blue, _night_purple, t)
    elif (current_time == 12 and time_since <= 15) or (current_time == 13 and time_since >= 135):  # night → fading to day
        return _interpolate_color(_night_purple, _sky_blue, t)
