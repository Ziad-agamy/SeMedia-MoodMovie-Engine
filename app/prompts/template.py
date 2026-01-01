user_state_prompt = """
The user's message:
{user_input}

Given a user's message, infer the following fields:

- current_emotion:
  The user's present emotional state inferred from tone, wording, and intent.

- goal:
  The emotional outcome the user wants:
  - Uplift
  - Catharsis
  - Maintain
  - Distract

- energy_required:
  The level of emotional or physical engagement:
  - Low
  - Medium
  - High

- brain_load:
  The cognitive effort preferred:
  - Light
  - Moderate
  - Heavy

- preferred_genres:
  Genres explicitly mentioned or strongly implied.
  Use only allowed genres.

- excluded_genres:
  Genres mentioned by user to be suppressed or filtered out of the content recommendations.
  Don't add any genres in this section unless the user mentioned it (e.g., Don't suggest action and horror movies).
  User only allowed genres.

Return the result strictly in the required structured format.
{format_instructions}
"""

film_vibe_prompt = """
The goal is to expand a user query into a rich, emotionally descriptive movie-style synopsis
that captures mood, themes, pacing, and emotional tone.
This text will be used for semantic similarity search.

Constraints:
- Write exactly 3 sentences.
- Do NOT mention specific movie titles, actors, or directors.
- Use evocative, cinematic language (like a tagline or short plot summary).
- Focus on emotional atmosphere, themes, and viewing experience.
- Avoid spoilers or concrete plot details.

User State:
User emotion: {current_emotion}
Original user query: "{user_input}"

NOTE: Return the desription only, don't add any helper comments or text, just the desrcription.
"""