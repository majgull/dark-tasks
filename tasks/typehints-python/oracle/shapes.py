"""Plane geometry helpers."""

import math


def area_circle(r: float) -> float:
    return math.pi * r * r


def area_rect(w: float, h: float) -> float:
    return w * h


def perimeter_rect(w: float, h: float) -> float:
    return 2 * (w + h)


def scale(points: list[tuple[float, float]], factor: float) -> list[tuple[float, float]]:
    return [(x * factor, y * factor) for x, y in points]


def describe(name: str, area: float) -> str:
    return f"{name}: {area:.2f}"
