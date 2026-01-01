from pydantic import BaseModel, Field
from typing_extensions import Literal, List

GenreType = Literal[
    "Action", "Adventure", "Animation", "Comedy", "Crime", 
    "Documentary", "Drama", "Fantasy", "Horror", "Musical", 
    "Mystery", "Romance", "Science Fiction", "Thriller", "Western", "War"
]

class UserState(BaseModel):
    current_emotion: str = Field(description="The user's current mood (e.g., Melancholy, Joyful)")
    goal: Literal["Uplift", "Catharsis", "Maintain", "Distract"] = Field(description="The desired emotional outcome")
    energy_required: Literal["Low", "Medium", "High"] = Field(description="Physical/emotional stamina")
    brain_load: Literal["Light", "Moderate", "Heavy"] = Field(description="Cognitive effort")
    preferred_genres: List[GenreType] = Field(
        default_factory=list, 
        description="Genres the user explicitly asked for or implied"
    )
    excluded_genres: List[GenreType] = Field(
        default_factory=list,
        description="Genres to be suppressed or filtered out of the user's content recommendations."
    )

class UserVibe(BaseModel):
    vibe: str = Field(description="Vibe of the movie the user is looking for")