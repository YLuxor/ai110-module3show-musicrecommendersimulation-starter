# Music Recommender — Algorithm Flowchart

Visual overview of the scoring pipeline: how `songs.csv` and a `UserProfile`
flow through the weighted-feature + bonus recipe to produce the Top 5
recommendations.

```mermaid
flowchart TD
    subgraph IN["① INPUT"]
        A[/"songs.csv — 10 songs"/]
        B[/"UserProfile\nfavorite_genre · favorite_mood\ntarget_energy · target_acousticness · target_danceability"/]
    end

    subgraph PROC["② PROCESS — Evaluate Each Song"]
        LOOP(["For each song in catalog"])

        subgraph NUM["Numeric Feature Score  〔0 – 10 pts〕"]
            N1["energy        × 0.15"]
            N2["acousticness  × 0.25"]
            N3["valence       × 0.25"]
            N4["danceability  × 0.35"]
            WSUM(["Weighted Sum"])
            N1 & N2 & N3 & N4 --> WSUM
        end

        GQ{"Genre Match?\nuser_genre == song_genre"}
        MQ{"Mood Match?\nuser_mood vs song_mood"}
        TOT["Total = min( numeric + bonuses, 10.0 )"]
        MORE{"More songs\nremaining?"}

        LOOP --> N1 & N2 & N3 & N4
        WSUM --> GQ
        GQ -- "Yes → +1.5 pts" --> MQ
        GQ -- "No  → +0.0 pts" --> MQ
        MQ -- "Exact    → +1.0 pt"  --> TOT
        MQ -- "Adjacent → +0.5 pt"  --> TOT
        MQ -- "None     → +0.0 pts" --> TOT
        TOT --> MORE
        MORE -- "Yes" --> LOOP
    end

    subgraph OUT["③ OUTPUT"]
        SORT["Sort all songs by Score descending"]
        TOP["Select Top 5 songs"]
        DISP["Display Recommendations\nTitle · Artist · Score · Explanation"]
        SORT --> TOP --> DISP
    end

    A --> LOOP
    B --> LOOP
    MORE -- "No — all songs scored" --> SORT

    style IN   fill:#dbeafe,stroke:#3b82f6,color:#1e3a5f
    style PROC fill:#fef3c7,stroke:#f59e0b,color:#78350f
    style NUM  fill:#fde68a,stroke:#d97706,color:#78350f
    style OUT  fill:#dcfce7,stroke:#22c55e,color:#14532d
```

## Algorithm Recipe Summary

| Layer | Signal | Points |
|---|---|---|
| Numeric features | Weighted similarity across energy, acousticness, valence, danceability | 0 – 10 |
| Genre bonus | Exact match: `user_genre == song_genre` | +1.5 |
| Mood bonus (exact) | `user_mood == song_mood` | +1.0 |
| Mood bonus (adjacent) | Similar mood per adjacency map | +0.5 |
| **Cap** | `min(total, 10.0)` | **max 10** |
