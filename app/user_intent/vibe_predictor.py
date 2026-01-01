from langchain_core.prompts import ChatPromptTemplate, FewShotChatMessagePromptTemplate
from langchain_core.output_parsers import PydanticOutputParser, StrOutputParser

from app.prompts.system_prompt import user_state_role, film_vibe_role
from app.prompts.few_shot import film_vibe_shot
from app.prompts.template import user_state_prompt, film_vibe_prompt 
from app.user_intent.schemas import UserState, UserVibe

def predict_user_state(llm, user_input: str) -> UserState:
    parser = PydanticOutputParser(pydantic_object=UserState)

    prompt = ChatPromptTemplate.from_messages([
        ('system', user_state_role),
        ('human', user_state_prompt)
    ]).partial(format_instructions=parser.get_format_instructions())

    chain = prompt | llm | parser
    return chain.invoke({"user_input": user_input})

def predict_film_vibe(llm, user_input: str) -> UserVibe:
    vibe = predict_user_state(llm, user_input)
    vibe = vibe.current_emotion

    parser = StrOutputParser()

    example_prompt = ChatPromptTemplate.from_messages([
        ('human', '{input}'),
        ('ai', '{output}')
    ])
    few_shot_prompt = FewShotChatMessagePromptTemplate(
        example_prompt=example_prompt,
        examples=film_vibe_shot
    )
    prompt = ChatPromptTemplate.from_messages([
        ('system', film_vibe_role),
        few_shot_prompt,
        ('human', film_vibe_prompt)

    ])
    chain = prompt | llm | parser
    result_text = chain.invoke({"current_emotion": vibe, "user_input": user_input})
    
    return UserVibe(vibe=result_text)

if __name__ == '__main__':
    from langchain_ollama import ChatOllama
    from app.config import DEFAULT_LLM_MODEL

    llm = ChatOllama(model=DEFAULT_LLM_MODEL)
    user_input = "Today I am in the mood. It's the christmas and I want to celebrate the new year with the family"

    vibe = predict_film_vibe(llm, user_input)
    state = predict_user_state(llm, user_input)

    print(state.model_dump_json(indent=2))
    print("\n")
    print(vibe.model_dump_json(indent=2))