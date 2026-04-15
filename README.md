# 🎵 Music Recommender Simulation

## Project Summary

In this project you will build and explain a small music recommender system.

Your goal is to:

- Represent songs and a user "taste profile" as data
- Design a scoring rule that turns that data into recommendations
- Evaluate what your system gets right and wrong
- Reflect on how this mirrors real world AI recommenders

Replace this paragraph with your own summary of what your version does.
ANS: A content-based music recommender that translates musical attributes into a searchable data format. My version uses a weighted scoring algorithm to compare a catalog of songs against a specific user "taste profile" dictionary. By assigning point values to genre matches, mood alignment, and energy proximity, the system mathematically identifies the best matches within the library. This simulation explores the balance between strict data matching and flexible "vibes," mirroring how real-world AI platforms like Spotify prioritize specific features to personalize user feeds.

---

## How The System Works

Explain your design in plain language.

Some prompts to answer:

- What features does each `Song` use in your system
  - For example: genre, mood, energy, tempo
- What information does your `UserProfile` store
- How does your `Recommender` compute a score for each song
- How do you choose which songs to recommend

You can include a simple diagram or bullet list if helpful.
ANS: My music recommender uses a weighted point-scoring system to rank songs based on a user's taste profile. The system evaluates every track in a 20-song catalog by comparing its attributes to a target profile, awarding 1.5 points for an exact genre match, 1.0 point for a mood match, and up to 10.0 points based on the similarity of numeric features like energy and danceability. This approach ensures that while general "vibes" (mood and energy) are considered, the system remains slightly biased toward a user's long-term genre preferences to maintain consistency. The final output is a sorted list where the user is presented with the top 5 highest-scoring recommendations that align most closely with their defined preferences.

---

## Getting Started

### Setup

1. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv .venv
   source .venv/bin/activate      # Mac or Linux
   .venv\Scripts\activate         # Windows

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Run the app:

```bash
python -m src.main
```

### Running Tests

Run the starter tests with:

```bash
pytest
```

You can add more tests in `tests/test_recommender.py`.

---

## Sample Output

![Top 5 Music Recommendations in the terminal](docs/terminal-output.png)

---

## Experiments You Tried

Use this section to document the experiments you ran. For example:

- What happened when you changed the weight on genre from 2.0 to 0.5
- What happened when you added tempo or valence to the score
- How did your system behave for different types of users

---

## Limitations and Risks

Summarize some limitations of your recommender.

Examples:

- It only works on a tiny catalog
- It does not understand lyrics or language
- It might over favor one genre or mood

You will go deeper on this in your model card.

---

## Reflection

Read and complete `model_card.md`:

[**Model Card**](model_card.md)

Recommenders turn data into predictions by comparing numbers. My system gives each song a score based on how close its energy and danceability are to what a user wants, then adds bonus points for genre and mood matches. That is it. There is no understanding of lyrics, context, or emotion — just arithmetic. But when you format the output cleanly and print a reason for each recommendation, it feels surprisingly personal. The explanation does most of the work; the math just produces the ranking.

Bias shows up quietly. My catalog has three lofi songs and one jazz song, which means a lofi fan has three chances to earn the genre bonus while a jazz fan has one. A user who prefers "sad" music gets zero mood bonuses because no songs in the catalog have that mood. The system never warns about this — it just returns five songs and prints scores, which makes the problem invisible unless you specifically test edge cases. That taught me that unfairness in AI systems is often a data problem, not a logic problem, and it can be hard to spot without deliberately trying to break the system.


---

## 7. `model_card_template.md`

Combines reflection and model card framing from the Module 3 guidance. :contentReference[oaicite:2]{index=2}  

```markdown
# 🎧 Model Card - Music Recommender Simulation

## 1. Model Name

Give your recommender a name, for example:

> VibeFinder 1.0

---

## 2. Intended Use

- What is this system trying to do
- Who is it for

Example:

> This model suggests 3 to 5 songs from a small catalog based on a user's preferred genre, mood, and energy level. It is for classroom exploration only, not for real users.

---

## 3. How It Works (Short Explanation)

Describe your scoring logic in plain language.

- What features of each song does it consider
- What information about the user does it use
- How does it turn those into a number

Try to avoid code in this section, treat it like an explanation to a non programmer.

---

## 4. Data

Describe your dataset.

- How many songs are in `data/songs.csv`
- Did you add or remove any songs
- What kinds of genres or moods are represented
- Whose taste does this data mostly reflect

---

## 5. Strengths

Where does your recommender work well

You can think about:
- Situations where the top results "felt right"
- Particular user profiles it served well
- Simplicity or transparency benefits

---

## 6. Limitations and Bias

Where does your recommender struggle

Some prompts:
- Does it ignore some genres or moods
- Does it treat all users as if they have the same taste shape
- Is it biased toward high energy or one genre by default
- How could this be unfair if used in a real product

---

## 7. Evaluation

How did you check your system

Examples:
- You tried multiple user profiles and wrote down whether the results matched your expectations
- You compared your simulation to what a real app like Spotify or YouTube tends to recommend
- You wrote tests for your scoring logic

You do not need a numeric metric, but if you used one, explain what it measures.

---

## 8. Future Work

If you had more time, how would you improve this recommender

Examples:

- Add support for multiple users and "group vibe" recommendations
- Balance diversity of songs instead of always picking the closest match
- Use more features, like tempo ranges or lyric themes

---

## 9. Personal Reflection

A few sentences about what you learned:

- What surprised you about how your system behaved
- How did building this change how you think about real music recommenders
- Where do you think human judgment still matters, even if the model seems "smart"

