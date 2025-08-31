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


def generate_variants(texts: list) -> list:
    variants = []
    for i in texts:
        i = i.strip("。，；,.;!?！?")  # 清理標點
        variants.append(i)  # 原句

        if "是" in i:
            parts = i.split("是", 1)
            if len(parts) == 2:
                left, right = parts[0].strip(), parts[1].strip()

                # 倒裝句
                variants.append(f"{right}是{left}。")

                # 問句：誰/什麼
                if len(left) > 0 and len(right) > 0:
                    variants.append(f"{left}是誰？是{right}。")
                    variants.append(f"{right}是什麼？是{left}。")
                    variants.append(f"{right}是誰？是{left}。")
                    variants.append(f"誰是{right}？是{left}。")
    return variants


# 環境變數
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
print("OPENAI_API_KEY:", OPENAI_API_KEY)

# 1. 準備文本資料
texts = [
    "LangChain 是一個強大的框架，用來建構 LLM 應用。",
    "FAISS 是由 Facebook AI 提供的向量檢索資料庫。",
    "你可以將文件轉換成 Embeddings，然後用 FAISS 做相似度搜尋。",
    "Kevin Sin是NSG的大PM。",
    "Danny Huang是NSG的總經理。",
]

texts = generate_variants(texts)


docs = [
    Document(page_content=t, metadata={"index": i})
    for i, t in enumerate(texts)
]

# 2. 建立 Embeddings 與 FAISS 向量資料庫
# embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
embeddings = OllamaEmbeddings(model="llama3.2:latest")
db = FAISS.from_documents(docs, embeddings)

# 3. 建立檢索器
retriever = db.as_retriever(search_type="similarity", search_kwargs={"k": 4})

# 4. 結合 LLM 問答
# llm = ChatOpenAI(
#     model="gpt-4o-mini",  # 也可以用 "gpt-4o" 或 "gpt-3.5-turbo"
#     temperature=0
# )

llm = ChatOllama(model="llama3.2:latest")

system_prompt = """
每句話開頭以 Will:
你是一個助手，用來回答問題。
你只能根據檢索到的上下文 (context) 來回答。
禁止使用你自己的知識來補充。
如果 context 中沒有答案，就回答「我不知道」。
最多使用三句話，保持答案簡潔。
如果檢索結果顯示某人身份或職稱，就直接回答該身份。

{context}
"""

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
