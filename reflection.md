# Stress-Test Reflection — Pair Comparisons

Three profiles were run against the same 10-song catalog. The scores below are
calculated from the current experimental weights in `recommender.py`:
base score = (2 × energy similarity + danceability similarity) / 3,
genre bonus = +0.75, exact mood bonus = +1.0, cap = 10.0.

---

## Pair 1 — High-Energy Pop vs. Deep Intense Rock

**Profiles at a glance**

| | High-Energy Pop | Deep Intense Rock |
|---|---|---|
| Energy target | 0.90 | 1.00 |
| Danceability target | 0.85 | 0.70 |
| Favorite genre | pop | rock |
| Favorite mood | happy | aggressive |

**Top 5 results**

| Rank | High-Energy Pop | Score | Deep Intense Rock | Score |
|---|---|---|---|---|
| 1 | Sunrise City | 10.0 | Storm Runner | 10.0 |
| 2 | Gym Hero | 10.0 | Gym Hero | 8.93 |
| 3 | Rooftop Lights | 9.97 | Sunrise City | 8.50 |
| 4 | Storm Runner | 9.30 | Night Drive Loop | 8.23 |
| 5 | Night Drive Loop | 8.60 | Rooftop Lights | 8.00 |

**What changed and why**

The most striking result is that the same five songs appear in both lists —
only the order shifted. Both profiles target high energy and high danceability,
so the numeric base scores are nearly identical across the catalog. The only
thing that reshuffled the rankings was which song happened to match the genre.

Storm Runner (rock, energy 0.91) climbed from #4 to #1 for the rock listener
because its genre bonus (+0.75) pushed its total to the 10.0 cap. Sunrise City
fell from #1 to #3 for the same reason in reverse: the pop listener received
both a genre bonus and a mood bonus on Sunrise City, stacking the score to the
cap, but the rock listener received neither bonus on it, leaving it at 8.50 on
numerics alone.

Gym Hero stayed in the top two for both profiles because its energy (0.93) and
danceability (0.88) are so close to both targets that no bonus is needed to
keep it competitive. This is the clearest sign that numeric proximity dominates
when the song is an extremely close match on the features that are measured.

**Takeaway:** When two profiles share the same numeric targets, the genre bonus
acts as a tiebreaker — not a fundamentally different recommendation, just a
reorder of the same shortlist.

---

## Pair 2 — Deep Intense Rock vs. Adversarial / Sad Jazz

**Profiles at a glance**

| | Deep Intense Rock | Adversarial / Sad Jazz |
|---|---|---|
| Energy target | 1.00 | 1.00 |
| Danceability target | 0.70 | 0.50 |
| Favorite genre | rock | jazz |
| Favorite mood | aggressive | sad |

**Top 5 results**

| Rank | Deep Intense Rock | Score | Adversarial / Sad Jazz | Score |
|---|---|---|---|---|
| 1 | Storm Runner | 10.0 | Storm Runner | 8.87 |
| 2 | Gym Hero | 8.93 | Gym Hero | 8.27 |
| 3 | Sunrise City | 8.50 | Sunrise City | 7.83 |
| 4 | Night Drive Loop | 8.23 | Night Drive Loop | 7.57 |
| 5 | Rooftop Lights | 8.00 | Rooftop Lights | 7.33 |

**What changed and why**

Both profiles target the same energy level (1.0), but the jazz listener targets
lower danceability (0.50 vs. 0.70). That shift quietly changes the numeric
base for every song, pulling scores down by roughly 0.5 to 1.0 points across
the board. The ranking order is identical — the same five songs in the same
positions — but the jazz profile's ceiling is 8.87 instead of 10.0.

The deeper problem is what is missing rather than what changed. The rock
listener earned a genre bonus on Storm Runner (+0.75), which is why it hit the
cap. The jazz listener cannot earn a genre bonus at all in the top five because
the only jazz song, Coffee Shop Stories, has an energy of 0.37 — far from the
target of 1.0 — and that numeric gap (a base of 5.67) is too large for the
+0.75 genre bonus to overcome. Coffee Shop Stories ends up at position #6,
scoring 6.42, while five non-jazz songs outscore it on energy and danceability
alone.

The mood situation is even bleaker: "aggressive" and "sad" both have zero songs
in the catalog, so neither profile can ever earn a mood bonus regardless of how
everything else lines up.

**Takeaway:** Matching energy is so heavily weighted that a genre fan whose
preferred genre has low-energy songs cannot compete. The jazz listener gets a
playlist that looks almost identical to the rock listener's — just slightly
lower scores — despite wanting a completely different listening experience.

---

## Pair 3 — High-Energy Pop vs. Adversarial / Sad Jazz

**Profiles at a glance**

| | High-Energy Pop | Adversarial / Sad Jazz |
|---|---|---|
| Energy target | 0.90 | 1.00 |
| Danceability target | 0.85 | 0.50 |
| Favorite genre | pop | jazz |
| Favorite mood | happy | sad |

**Top 5 results**

| Rank | High-Energy Pop | Score | Adversarial / Sad Jazz | Score |
|---|---|---|---|---|
| 1 | Sunrise City | 10.0 | Storm Runner | 8.87 |
| 2 | Gym Hero | 10.0 | Gym Hero | 8.27 |
| 3 | Rooftop Lights | 9.97 | Sunrise City | 7.83 |
| 4 | Storm Runner | 9.30 | Night Drive Loop | 7.57 |
| 5 | Night Drive Loop | 8.60 | Rooftop Lights | 7.33 |

**What changed and why**

This pair shows the widest gap in both score ceiling and recommendation quality.
The pop listener earned bonuses on three of the top five songs: a genre bonus on
Sunrise City and Gym Hero (both pop), and a mood bonus on Sunrise City and
Rooftop Lights (both happy). Those stacked bonuses pushed two songs to the
perfect 10.0 cap and a third to 9.97. The jazz listener earned zero bonuses
across the entire top five — not one genre match, not one mood match.

Both profiles still received Storm Runner, Gym Hero, and Sunrise City in their
top five. These are rock, pop, and pop songs respectively. A user who described
themselves as a sad jazz fan received a playlist dominated by high-intensity
rock and pop because that is what scores highest on numeric features when no
bonuses are accessible. The system is not malfunctioning — it is doing exactly
what the math says — but the result is a list that has almost nothing to do with
what the user asked for.

The contrast also shows how the scoring gap between profiles widens as the
catalog gets smaller. A pop fan benefits from two genre candidates and two mood
candidates in ten songs; a jazz fan has one genre candidate (and it is an
energy mismatch) and zero mood candidates. The richer a genre is represented
in the catalog, the more opportunities a fan of that genre has to earn bonuses,
making the recommender quietly more useful for mainstream tastes than niche ones.

**Takeaway:** The pop listener's result felt intuitive — recognizable songs for
a recognizable taste. The jazz listener's result felt arbitrary — a high-energy
playlist delivered to someone who wanted something quiet and melancholy. The
difference came entirely from catalog composition, not from anything the
recommender logic did wrong.

---

## Overall Pattern

Across all three pairs, one conclusion repeats: **the catalog is the bottleneck,
not the weights.** Songs with high energy and high danceability dominate every
shortlist because those features are shared by the majority of the catalog's
high-scoring tracks, and none of the weight adjustments in the sensitivity
experiment changed that fundamental ordering. A real recommender would need a
larger, more balanced catalog before weight tuning would make a meaningful
difference.
