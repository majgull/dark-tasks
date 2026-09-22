"""Demo: a tiny report built from the helpers."""

from numutil import clamp, mean, percent
from textutil import slug, title_words, truncate

SCORES = [72, 88, 95, 61]


def main():
    print(slug("Dark Runner: Phase 2!"))
    print(title_words("the quick brown fox"))
    print(truncate("a rather long sentence", 10))
    print(clamp(150, 0, 100), clamp(-5, 0, 100), clamp(42, 0, 100))
    print(mean(SCORES))
    print(percent(sum(1 for s in SCORES if s >= 70), len(SCORES)))


if __name__ == "__main__":
    main()
