"""Plane geometry helpers."""

import math


def area_circle(r):
    return math.pi * r * r


def area_rect(w, h):
    return w * h


def perimeter_rect(w, h):
    return 2 * (w + h)


def scale(points, factor):
    return [(x * factor, y * factor) for x, y in points]


def describe(name, area):
    return f"{name}: {area:.2f}"
