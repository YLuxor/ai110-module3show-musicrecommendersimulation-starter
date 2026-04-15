# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

**BeatSync 1.0**

A content-based music recommender that matches songs to a listener's energy level, genre preference, and mood.

---

## 2. Intended Use  

**What it does:** BeatSync suggests the top 5 songs from a small catalog based on a user's taste profile. It looks at genre, mood, energy, and danceability to find the closest matches.

**Who it is for:** This is a classroom simulation. It is designed for exploring how recommender systems work, not for real users or a real product.

**What it assumes:** It assumes the user's taste can be described with a single genre, a single mood, and a target energy level. It does not handle complex tastes like "I like jazz on weekdays but pop on weekends."

**What it should NOT be used for:**
- Making recommendations for real streaming platforms
- Users with moods or genres not represented in the catalog (those profiles will get poor results)
- Any setting where fairness across genres actually matters

---

## 3. How the Model Works  

Every song gets a score out of 10. Here is how the score is built:

1. **Numeric similarity (0–10 pts):** The system checks how close the song's energy and danceability are to what the user wants. A perfect match scores 10. A big difference scores close to 0. Energy is weighted twice as heavily as danceability.

2. **Genre bonus (+0.75 pts):** If the song's genre exactly matches the user's favorite genre, it gets a small bonus added on top.

3. **Mood bonus (+1.0 or +0.5 pts):** If the song's mood exactly matches, it earns a full bonus point. If the mood is "close but not exact" (for example, the user likes "relaxed" and the song is "chill"), it earns a half point.

4. **Cap:** The total is capped at 10.0. A song can never score higher than that no matter how many bonuses stack up.

The system ranks all 10 songs by their final score and returns the top 5.

The main change from the starter version: energy is weighted 2:1 over danceability instead of 1:1. This makes energy the dominant numeric signal.

---

## 4. Data  

**Catalog size:** 10 songs, stored in `data/songs.csv`.

**Features stored per song:** id, title, artist, genre, mood, energy, tempo (BPM), valence, danceability, acousticness.

**Features actually used in scoring:** energy, danceability, genre, mood. Tempo, valence, and acousticness are stored but not used.

**Genre breakdown:** lofi (3 songs), pop (2), and one each of rock, jazz, ambient, synthwave, and indie pop.

**Mood breakdown:** chill (3 songs), happy (2), intense (2), and one each of relaxed, moody, and focused.

**What is missing:** No songs with "sad," "aggressive," "romantic," "calm," or "energetic" moods — even though those moods appear in the scoring rules. A user who picks any of those moods will never earn a mood bonus. There are no hip-hop, R&B, classical, or country songs at all.

No songs were added or removed from the original catalog.

---

## 5. Strengths  

**High-energy pop and rock fans get reasonable results.** The catalog has enough pop and rock songs with high energy that those users consistently see songs close to what they asked for.

**The scoring is fully transparent.** Every recommendation comes with a printed explanation: which features matched and how many points each one added. There are no hidden signals.

**The mood adjacency map adds some flexibility.** If a user's mood has no exact match, the system can still award partial credit for a similar mood (for example, "relaxed" and "chill" are treated as close). This prevents the score from dropping to zero just because the wording is slightly different.

**Fast and simple.** The system scores 10 songs in milliseconds and requires no training data or machine learning. The logic is easy to read and explain.

---

## 6. Limitations and Bias 

The catalog contains only 10 songs, and 30% of them are lofi — meaning a lofi user has three opportunities to earn the genre bonus (+1.5 pts) while a jazz or rock user has only one, creating an unequal playing field baked directly into the data. Five moods that appear in the scoring adjacency map — including "sad," "aggressive," and "romantic" — have zero matching songs in the catalog, so any user whose preference falls into those moods will never earn a mood bonus regardless of how well the rest of their profile matches. This produces a filter bubble: the system quietly steers niche-taste users toward high-energy songs that score well on numeric features alone, not because they are a good match, but because nothing better exists in the catalog. The sensitivity experiment confirmed this — halving the genre bonus barely affected lofi recommendations (three songs still compete for it) but made jazz nearly invisible, dropping Coffee Shop Stories out of the top five entirely. A real recommender would need a much larger and more balanced catalog, plus a penalty or diversity mechanism to prevent the same cluster of high-energy songs from dominating every profile that lacks an exact genre or mood match.

---

## 7. Evaluation  

Three user profiles were tested: High-Energy Pop (a happy, danceable pop listener), Deep Intense Rock (an aggressive, maximum-energy rock fan), and an Adversarial/Edge Case (a jazz listener whose preferred moods — sad and aggressive — do not exist in the catalog).

**High-Energy Pop vs. Deep Intense Rock — what changed and what did not.**
The most surprising result was that the exact same five songs appeared in both top-five lists. Storm Runner, Gym Hero, Sunrise City, Night Drive Loop, and Rooftop Lights dominated both profiles; only their order shifted. Storm Runner jumped from #4 (Pop) to #1 (Rock) purely because its rock genre bonus pushed its total score to the 10.0 cap. Everything else kept roughly the same ranking because both profiles share high energy and high danceability targets — the numbers looked almost identical to the recommender even though one user imagines herself dancing at a concert and the other imagines himself lifting weights. This confirmed that the system measures *how much* energy a song has, but cannot detect *why* someone wants that energy.

**Why Gym Hero keeps appearing for a "Happy" profile.**
Gym Hero (energy 0.93, danceability 0.88) is the closest numerical match for a pop fan who wants high energy and high danceability — the system scores it 9.7 out of 10 on numbers alone before any bonus is applied. Its mood is "intense," not "happy," so it earns no mood bonus — but by that point the base score is already high enough to land it in the top two. Imagine looking for a fun, upbeat song to play at a birthday party and the playlist keeps inserting a heavy workout track: both have loud, fast, driving beats, but the *feeling* is completely different. The recommender has no way to know the difference because it only reads the numbers, not the emotional intention behind them. A song either has high energy or it does not; why the listener wants that energy is invisible to the model.

**What surprised me.**
The Adversarial profile revealed a hard ceiling on the system's helpfulness. A jazz listener who prefers "sad" music has zero mood-match candidates in the entire catalog, so the recommendations are determined entirely by numeric similarity — and the highest-energy, most-danceable songs (Storm Runner, Gym Hero) floated to the top even though they are arguably the worst emotional match imaginable for someone who wants calm, melancholy jazz. Running the sensitivity experiment (halving the genre bonus) made this worse: the jazz genre bonus on Coffee Shop Stories dropped just enough to push it out of the top five entirely, leaving an all-rock-and-pop list for a jazz fan. That result made the catalog imbalance problem concrete and measurable rather than just theoretical.

---

## 8. Future Work  

**1. Expand and balance the catalog.**
Ten songs is not enough. A real version would need at least 100 songs spread evenly across genres and moods. Right now the catalog bottleneck matters more than any weight setting — there is nothing to recommend for sad, aggressive, or romantic listeners no matter how the math is tuned.

**2. Add a diversity rule.**
The same five high-energy songs dominate almost every profile. A simple fix would be a penalty that prevents the same artist or genre from taking more than two spots in the top five. This would push niche-genre songs higher even when they lose on raw score.

**3. Use tempo and valence in the score.**
Both features are stored in the CSV but completely ignored right now. Tempo (BPM) is a good proxy for energy style — a 60 BPM lofi track and a 152 BPM metal track can both score "high energy" by the current measure, but they feel nothing alike. Adding tempo as a feature would separate those two cases.

---

## 9. Personal Reflection  

**Biggest learning moment**

The biggest moment came when I ran the adversarial jazz profile. The system returned five high-energy rock and pop songs to a user who said they wanted calm, sad jazz. The algorithm was not broken — it was doing exactly what the math said. That showed me that data quality matters more than algorithm design. I spent time tuning weights and bonuses, but no weight change could fix a catalog that had zero "sad" songs and only one jazz track.

**How AI tools helped — and when I had to double-check**

AI tools helped me understand why specific songs ranked the way they did. When Storm Runner ranked first for the adversarial profile, I asked for an exact mathematical explanation and got the step-by-step arithmetic. That was faster than working through it manually. But I did need to double-check a few things. The scoring path in `score_song` (used by `main.py`) and the one in `_score_song` (used by the tests) use different formulas — and an AI explanation once mixed them up, giving me numbers that did not match what actually printed in the terminal. The lesson: always verify AI-generated explanations against what the code actually runs, not what it looks like it should run.

**What surprised me about simple algorithms feeling like real recommendations**

I expected the output to look like a toy. Instead, the formatted terminal output — ranked titles, scores, and printed reasons like "matches your favorite genre" or "energy is close to your target" — felt genuinely convincing. A few weighted numbers and two bonus conditions created something that reads like a real product. That surprised me. The explanation text does a lot of work: once you print *why* a song was recommended, it stops feeling arbitrary even if the underlying math is simple. Real recommender apps probably rely on the same trick — the explanation makes the result feel personal even when the algorithm is not that different from what I built here.

**What I would try next**

If I kept working on this, the first thing I would fix is the catalog. A hundred songs spread evenly across genres and moods would make the genre and mood bonuses fair for everyone, not just pop and lofi listeners. After that, I would add tempo to the scoring — it is already stored in the CSV but completely ignored right now. A 60 BPM ambient track and a 152 BPM metal track can both score the same on energy, but they feel nothing alike. Bringing tempo in would let the system separate those two cases.
