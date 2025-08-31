import os
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.chat_models import ChatOllama
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import OllamaEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from langchain.docstore.document import Document

from dotenv import load_dotenv
load_dotenv()


def generate_questions(texts):
    qa_pairs = []
    for s in texts:
        if "是" in s:
            parts = s.split("是", 1)
            subject = parts[0].strip()
            predicate = parts[1].strip(" 。， ")

            q1 = f"誰是{predicate}？"
            q2 = f"{subject}是什麼？"
            q3 = f"{subject}是?"   # ✅ 新增一個簡短問法

            qa_pairs.extend([q1, q2, q3])
    return qa_pairs


def build_docs_with_questions(texts):
    """將原始句子與問句一起轉成 Document"""
    docs = []

    for i, s in enumerate(texts):
        # 原始句子
        docs.append(Document(page_content=s, metadata={"type": "statement", "index": i}))

    # 產生問句
    questions = generate_questions(texts)
    for j, q in enumerate(questions):
        docs.append(Document(page_content=q, metadata={"type": "question", "q_index": j}))

    return docs

# 環境變數
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
print("OPENAI_API_KEY:", OPENAI_API_KEY)

# 1. 準備文本資料
texts = [
    "LangChain 是一個強大的框架，用來建構 LLM 應用。",
    "FAISS 是由 Facebook AI 提供的向量檢索資料庫。",
    "你可以將文件轉換成 Embeddings，然後用 FAISS 做相似度搜尋。",
    "Kevin Sin 是NSG的大PM",
    "Danny Huang 是NSG的大PM",
]


# docs = [
#     Document(page_content=t, metadata={"index": i})
#     for i, t in enumerate(texts)
# ]
docs = build_docs_with_questions(texts)
# 2. 建立 Embeddings 與 FAISS 向量資料庫
# embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
embeddings = OllamaEmbeddings(model="llama3.2:latest")
db = FAISS.from_documents(docs, embeddings)

# 3. 建立檢索器
retriever = db.as_retriever(search_type="similarity", search_kwargs={"k": 2})

# 4. 結合 LLM 問答
# llm = ChatOpenAI(
#     model="gpt-4o-mini",  # 也可以用 "gpt-4o" 或 "gpt-3.5-turbo"
#     temperature=0
# )

llm = ChatOllama(model="llama3.2:latest")

system_prompt = (
    "每句話回答前先表達自己的名字是Will並以Will: "
    "你是一個助手，用來回答問題。"
    "請使用以下檢索到的上下文來回答問題。"
    "如果你不知道答案，就說你不知道。"
    "最多使用三句話，保持答案簡潔。"
    "如果檢索結果有相關資訊，請務必用檢索到的內容回答。"
    "如果檢索結果顯示某人身份或職稱，就直接回答該身份。"
    "\n\n"
    "{context}"
)

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system_prompt),
        ("human", "{input}"),
    ]
)

# 建立 QA chain
question_answer_chain = create_stuff_documents_chain(llm, prompt)
qa_chain = create_retrieval_chain(retriever, question_answer_chain)

# 5. 問問題
query = input("請輸入你的問題: ")
result = qa_chain.invoke({"input": query})
db.save_local("faiss_index")
print("問題:", query)
print("回答:", result["answer"])
