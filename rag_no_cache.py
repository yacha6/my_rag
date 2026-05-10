import streamlit as st
import os.path

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import TextLoader
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.runnables import RunnableParallel,RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
import os
from dotenv import load_dotenv

from langchain_community.embeddings import DashScopeEmbeddings

load_dotenv()

embeddings = DashScopeEmbeddings(
    model=os.getenv("DASHSCOPE_EMBEDDING_MODEL", "text-embedding-v2"),
    dashscope_api_key=os.getenv("DASHSCOPE_API_KEY"))
llm = ChatOpenAI(
    base_url=os.getenv("DASHSCOPE_BASE_URL"),
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    model=os.getenv("DASHSCOPE_LLM_MODEL", "qwen3-vl-235b-a22b-thinking"),
    temperature=0.7,
    streaming=True)

def text_chunk(file_path):
    # 加载指定路径的文本文件
    loader = TextLoader(file_path, encoding='utf-8')
    docs = loader.load()
    print(docs[0].metadata)

    # 把文本分割成 500 字一组的切片
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50  # 设置文本重叠
    )
    chunks = text_splitter.split_documents(docs)
    return chunks


def chunk2vector(docs, embeddings):
    # new_client = chromadb.EphemeralClient()
    vector = FAISS.from_documents(
        documents=docs,  # 设置保存的文档
        embedding=embeddings  # 设置 embedding model
        )
    return vector




def llm_chain(vector):
    template = """You are an assistant for question-answering tasks. Use the following pieces of retrieved context to answer the question. If you don't know the answer, just say that you don't know.

    Question: {question}

    Context: {context}

    Answer:"""
    prompt = ChatPromptTemplate.from_template(template)
    retriever = vector.as_retriever()
    chain = (
            RunnableParallel({"context": retriever, "question": RunnablePassthrough()})
            | prompt
            | llm
            | StrOutputParser()
    )
    return chain


def llm_an(file_path, question):
    # 避免question输入为空导致报错
    if not question:
        return "请输入问题。"
    docs = text_chunk(file_path)
    vetcor = chunk2vector(docs, embeddings)
    chain = llm_chain(vetcor)

    # 使用 st.write_stream 实现流式输出
    return st.write_stream(chain.stream(question))

def interactive(file_path):
    st.title("RAG")
    # st.sidebar.header("")

    with st.expander("RAG知识库", expanded=True):
        # 创建一个问题
        question_title = "您的问题是？"

        # 创建问答框，并获取用户输入
        usr_question = st.text_input(question_title)

        # 获取答案
        if usr_question:
            st.subheader("回答：")
            llm_an(file_path, usr_question)
        else:
            st.info("请输入您的问题。")


if __name__ == "__main__":
    # 设置文件地址
    file_path = '/Users/myc/Desktop/rag项目/曲面打印机说明书.txt'
    # 展示
    interactive(file_path)
