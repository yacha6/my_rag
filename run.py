import streamlit as st
from rag import llm_an

def interactive(file_path):
    st.title("RAG")
    # st.sidebar.header("")

    with st.expander("RAG知识库"):
        question_title = "您的问题是？"

        usr_question = st.text_input(question_title)

        if usr_question:
            usr_ans = llm_an(file_path, usr_question)
            st.write(f' {usr_ans}')
        else:
            st.write("请输入您的问题。")


if __name__ == "__main__":
    file_path = r'/Users/myc/Desktop/rag项目/曲面打印机说明书.txt'
    interactive(file_path)
