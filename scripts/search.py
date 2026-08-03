from app.services.chroma_service import ChromaService
from app.services.prompt_service import PromptService
from app.services.llm_service import LLMService

question = input("Question : ")

chroma = ChromaService()

results = chroma.search(question)

documents = results["documents"][0]

context = "\n\n".join(documents)

prompt = PromptService.build(
    context=context,
    question=question
)

answer = LLMService.ask(prompt)

print("=" * 60)
print(answer)
print("=" * 60)