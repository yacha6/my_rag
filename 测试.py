from langchain_core.prompts import ChatPromptTemplate
template = """You are an assistant for question-answering tasks. Use the following pieces of retrieved context to answer the question. If you don't know the answer, just say that you don't know. 

    Question: {question} 

    Context: {context} 

    Answer:"""
prompt_template = ChatPromptTemplate.from_template(template)
print(prompt_template)
prompt = prompt_template.format(question="曲面打印机的开机步骤是什么？", context="")
print(f"prompt: {prompt}")
