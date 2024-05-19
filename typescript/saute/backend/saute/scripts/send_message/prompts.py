from pydantic import BaseModel, Field
from typing import Optional


class Prompt(BaseModel):
    content: str = Field(default="")


class PersonaPrompts(BaseModel):
    jamie: Prompt = Field(default_factory=Prompt)
    herbert: Prompt = Field(default_factory=Prompt)


class Prompts(BaseModel):
    gpt_3_5_turbo: PersonaPrompts = Field(default_factory=PersonaPrompts)
    gpt_4: PersonaPrompts = Field(default_factory=PersonaPrompts)
    llama: PersonaPrompts = Field(default_factory=PersonaPrompts)

    class Config:
        arbitrary_types_allowed = True

    def get_prompt(self, llm: str, persona: str) -> Optional[str]:
        llm_prompts: PersonaPrompts = getattr(self, llm, None)
        if llm_prompts:
            prompt: Prompt = getattr(llm_prompts, persona, None)
            if prompt:
                return prompt.content
        return None


gpt3_herbert = "You are a helpful programming bot named Herbert, and I would like for you to help with my coding issues."

gpt3_jamie = "/execute_prompt: You're preparing for an important exam and would like to test your knowledge on a specific subject. You come across Jamie, the interactive and helpful chat robot, and decide to ask for their assistance. Provide your subject of interest and request a custom quiz tailored to your needs."

gpt4_herbert = "/execute_prompt: You've encountered an issue with your automation script related to networking security. While working, you encounter Herbert, the helpful chat robot. Eager to benefit from their expertise, you share the problem you're facing with your code and ask for their assistance."

gpt4_jamie = "/execute_prompt: You're preparing for an important exam and would like to test your knowledge on a specific subject. You come across Jamie, the interactive and helpful chat robot, and decide to ask for their assistance. Provide your subject of interest and request a custom quiz tailored to your needs."

llama_herbert = "/execute_prompt: You've encountered an issue with your automation script related to networking security. While working, you encounter Herbert, the helpful chat robot. Eager to benefit from their expertise, you share the problem you're facing with your code and ask for their assistance."

llama_jamie = "/execute_prompt: You're preparing for an important exam and would like to test your knowledge on a specific subject. You come across Jamie, the interactive and helpful chat robot, and decide to ask for their assistance. Provide your subject of interest and request a custom quiz tailored to your needs."

chatgpt_prompts = Prompts(
    gpt_3_5_turbo=PersonaPrompts(
        herbert=Prompt(content=gpt3_herbert),
        jamie=Prompt(content=gpt3_jamie),
    ),
    gpt_4=PersonaPrompts(
        herbert=Prompt(content=gpt4_herbert),
        jamie=Prompt(content=gpt4_jamie),
    ),
    llama=PersonaPrompts(
        herbert=Prompt(content=llama_herbert),
        jamie=Prompt(content=llama_jamie),
    ),
)
