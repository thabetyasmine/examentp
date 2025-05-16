import os
from dotenv import load_dotenv
from langchain.chat_models import ChatGroq
from langchain.prompts import PromptTemplate
from langchain.schema import HumanMessage

load_dotenv()
groq_api_key = os.getenv("GROQ_API_KEY")

chat = ChatGroq(api_key=groq_api_key, model_name="mixtral-8x7b-32768")

# Prompt Langchain
prompt_template = PromptTemplate(
    input_variables=["title", "year", "director", "actor_list"],
    template="Generate a short, engaging summary for the movie '{title}' ({year}), directed by {director} and starring {actor_list}."
)

def generate_movie_summary(title: str, year: int, director: str, actor_names: list[str]) -> str:
    prompt = prompt_template.format(
        title=title,
        year=year,
        director=director,
        actor_list=", ".join(actor_names)
    )
    message = [HumanMessage(content=prompt)]
    response = chat(message)
    return response.content
