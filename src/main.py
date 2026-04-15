"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from src.recommender import load_songs, recommend_songs


def main() -> None:
    songs = load_songs("data/songs.csv") 

    # Starter example profile — includes new acousticness and danceability targets
    user_prefs = {
        "genre":        "lofi",
        "mood":         "relaxed",
        "energy":       0.2,
        "acousticness": 0.8,
        "danceability": 0.55,
    }

    recommendations = recommend_songs(user_prefs, songs, k=5)

    width = 60
    divider = "-" * width

    print()
    print("=" * width)
    print(f"  Top {len(recommendations)} Music Recommendations")
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


if __name__ == "__main__":
    main()
