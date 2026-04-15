"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from src.recommender import load_songs, recommend_songs


TEST_PROFILES = [
    {
        "label":        "High-Energy Pop",
        "genre":        "pop",
        "mood":         "happy",
        "energy":       0.9,
        "acousticness": 0.1,
        "danceability": 0.85,
    },
    {
        "label":        "Deep Intense Rock",
        "genre":        "rock",
        "mood":         "aggressive",
        "energy":       1.0,
        "acousticness": 0.05,
        "danceability": 0.7,
    },
    {
        "label":        "Adversarial / Edge Case",
        "genre":        "jazz",
        "mood":         "sad",
        "energy":       1.0,
        "acousticness": 0.5,
        "danceability": 0.5,
    },
]


def print_recommendations(label: str, recommendations: list) -> None:
    """Print a formatted results block for one user profile."""
    width = 60
    divider = "-" * width

    print()
    print("=" * width)
    print(f"  Profile: {label}")
    print(f"  Top {len(recommendations)} Recommendations")
    print("=" * width)

    for rank, (song, score, reasons) in enumerate(recommendations, start=1):
        print()
        title_line = f"  #{rank}  {song['title']}"
        score_str  = f"Score: {score:.1f} / 10"
        padding    = width - len(title_line) - len(score_str)
        print(f"{title_line}{' ' * max(padding, 1)}{score_str}")
        print(f"       {song['artist']}  |  {song['genre']}  |  {song['mood']}")
        for reason in reasons:
            print(f"       * {reason}")
        print(f"  {divider}")

    print()


def main() -> None:
    songs = load_songs("data/songs.csv")

    for profile in TEST_PROFILES:
        label = profile["label"]
        user_prefs = {k: v for k, v in profile.items() if k != "label"}
        recommendations = recommend_songs(user_prefs, songs, k=5)
        print_recommendations(label, recommendations)


if __name__ == "__main__":
    main()
