from typing import List, Dict, Tuple
from dataclasses import dataclass, field
import csv

# ---------------------------------------------------------------------------
# Mood adjacency map — moods considered "close enough" to earn a partial bonus
# ---------------------------------------------------------------------------
MOOD_ADJACENCY: Dict[str, set] = {
    "relaxed":   {"chill", "calm"},
    "chill":     {"relaxed", "calm", "focused"},
    "calm":      {"relaxed", "chill"},
    "focused":   {"chill", "moody"},
    "happy":     {"romantic"},
    "romantic":  {"happy"},
    "intense":   {"energetic"},
    "energetic": {"intense"},
    "moody":     {"focused", "intense"},
}

# ---------------------------------------------------------------------------
# Scoring constants
# ---------------------------------------------------------------------------
WEIGHTS = {
    "energy":       0.15,
    "acousticness": 0.25,
    "valence":      0.25,
    "danceability": 0.35,
}

GENRE_BONUS        = 1.5   # exact genre match
MOOD_MATCH_BONUS   = 1.0   # exact mood match
MOOD_ADJACENT_BONUS = 0.5  # similar/adjacent mood


# ---------------------------------------------------------------------------
# Data classes
# ---------------------------------------------------------------------------
@dataclass
class Song:
    """Represents a song and its audio attributes."""
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float


@dataclass
class UserProfile:
    """Represents a user's taste preferences."""
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool
    target_acousticness: float = 0.5   # neutral default keeps old tests working
    target_danceability: float = 0.5   # neutral default keeps old tests working


# ---------------------------------------------------------------------------
# Scoring helpers
# ---------------------------------------------------------------------------
def _feature_score(user_val: float, song_val: float) -> float:
    """Score one numeric feature 0–10. Perfect match → 10, worst → 0."""
    return (1 - abs(user_val - song_val)) * 10


def _mood_bonus(user_mood: str, song_mood: str) -> float:
    """Return 1.0 for exact match, 0.5 for adjacent mood, 0.0 otherwise."""
    if user_mood == song_mood:
        return MOOD_MATCH_BONUS
    if song_mood in MOOD_ADJACENCY.get(user_mood, set()):
        return MOOD_ADJACENT_BONUS
    return 0.0


def _score_song(user: UserProfile, song: Song) -> float:
    """Compute a 0–10 match score for one song against a user profile."""
    numeric = (
        WEIGHTS["energy"]       * _feature_score(user.target_energy,       song.energy)
        + WEIGHTS["acousticness"] * _feature_score(user.target_acousticness, song.acousticness)
        + WEIGHTS["valence"]      * _feature_score(0.6,                      song.valence)
        + WEIGHTS["danceability"] * _feature_score(user.target_danceability, song.danceability)
    )
    genre_b = GENRE_BONUS if user.favorite_genre.lower() == song.genre.lower() else 0.0
    mood_b  = _mood_bonus(user.favorite_mood.lower(), song.mood.lower())
    return min(numeric + genre_b + mood_b, 10.0)


def _explain_song(user_genre: str, user_mood: str, user_energy: float, song: Song) -> str:
    """Build a human-readable explanation for why a song was recommended."""
    reasons = []
    if user_genre.lower() == song.genre.lower():
        reasons.append(f"matches your favorite genre ({song.genre})")
    mood_b = _mood_bonus(user_mood.lower(), song.mood.lower())
    if mood_b == MOOD_MATCH_BONUS:
        reasons.append(f"matches your preferred mood ({song.mood})")
    elif mood_b == MOOD_ADJACENT_BONUS:
        reasons.append(f"mood '{song.mood}' is similar to your preference '{user_mood}'")
    if abs(user_energy - song.energy) <= 0.15:
        reasons.append(f"energy ({song.energy}) is close to your target ({user_energy})")
    if reasons:
        return "Recommended because it " + ", and ".join(reasons)
    return "Scored well across energy, acousticness, and danceability"


# ---------------------------------------------------------------------------
# OOP interface (used by tests)
# ---------------------------------------------------------------------------
class Recommender:
    """OOP wrapper around the scoring and ranking logic."""

    def __init__(self, songs: List[Song]):
        """Store the catalog of songs this recommender will score."""
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        """Return the top k songs ranked by score for the given user profile."""
        scored = sorted(self.songs, key=lambda s: _score_song(user, s), reverse=True)
        return scored[:k]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        """Return a human-readable string explaining why a song was recommended."""
        return _explain_song(
            user.favorite_genre, user.favorite_mood, user.target_energy, song
        )


# ---------------------------------------------------------------------------
# Functional interface (used by main.py)
# ---------------------------------------------------------------------------
def load_songs(csv_path: str) -> List[Dict]:
    """
    Loads songs from a CSV file.
    Required by src/main.py
    """
    # TODO: Implement CSV loading logic
    print(f"Loading songs from {csv_path}...")
    return []

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """
    Functional implementation of the recommendation logic.
    Required by src/main.py
    """
    # 1. Score every song
    scored: List[Tuple[Dict, float, List[str]]] = []
    for song in songs:
        total, reasons = score_song(user_prefs, song)
        scored.append((song, total, reasons))

    # 2. Sort by score descending — sorted() leaves the original list untouched
    ranked = sorted(scored, key=lambda item: item[1], reverse=True)

    # 3. Return the top k
    return ranked[:k]
