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
import re
import regex
from dotenv import load_dotenv
load_dotenv()


def generate_variants(texts: list) -> list:
    variants = set()
    PUNCT = r"。；；,.;!?！？、"
    def clean_sentence(text: str) -> str:
        return re.sub(fr"^[\s{PUNCT}]+|[\s{PUNCT}]+$", "", text)

    for text in texts:
        # 去掉前後中英文標點
        sentence = clean_sentence(text)

        if not sentence:
            continue

        # 原句
        variants.add(sentence)

        # 如果包含「是」，嘗試生成變體
        if "是" in sentence:
            parts = sentence.split("是", 1)
            if len(parts) == 2:
                left, right = parts[0].strip(), parts[1].strip()

                if left and right:
                    # 倒裝句
                    variants.add(f"{right}是{left}。")

                    # 問句（誰是 right）
                    variants.add(f"誰是{right}？是{left}。")

                    # 問句（left 是誰）
                    variants.add(f"{left}是誰？是{right}。")

                    # 問句（right 是什麼）
                    variants.add(f"{right}是什麼？是{left}。")

    return list(variants)


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
"""
但 llama3.2 是聊天/生成模型，不是向量嵌入模型。用它做 embedding 
會很差（或直接不對），FAISS 當然就抓不到「Kevin Sin」那句。👇給你兩個可用方案與最小修正。
"""
# embeddings = OllamaEmbeddings(model="llama3.2:latest")
# embeddings = OpenAIEmbeddings(model="text-embedding-3-small")  # 或 text-embedding-3-large
# ollama pull nomic-embed-text
from langchain_community.embeddings import OllamaEmbeddings
embeddings = OllamaEmbeddings(model="nomic-embed-text")  # 或 "mxbai-embed-large" 


"""
1) 用「餵 Cosine」的方式建索引

FAISS 在 LangChain 預設是 L2 距離；而句向量常用 Cosine 相似度。做法是把向量 先做 L2 正規化 再用 L2 搜尋（等效於 Cosine）。
👉 只要在 from_documents 加 normalize_L2=True：
"""
db = FAISS.from_documents(docs, embeddings, normalize_L2=True)

# 3. 建立檢索器
"""
2) k 調大、MMR 更穩
"""
# retriever = db.as_retriever(search_type="similarity", search_kwargs={"k": 4})
retriever = db.as_retriever(
    search_type="mmr",                # 改成 mmr
    search_kwargs={"k": 8, "fetch_k": 20, "lambda_mult": 0.5}
)
print("=== DEBUG Retrieved ===")
for r in retriever.get_relevant_documents("誰是 Kevin Sin"):
    print(r.metadata, r.page_content)
print("=======================")

# 4. 結合 LLM 問答
# llm = ChatOpenAI(
#     model="gpt-4o-mini",  # 也可以用 "gpt-4o" 或 "gpt-3.5-turbo"
#     temperature=0
# )

llm = ChatOllama(model="llama3.2:latest")

system_prompt = """
回答必須以「Will: 」開頭，且最多三句話。
如果 context 中找到某人對應的身份或職稱，就直接輸出該身份或職稱，如果在資料庫發現就不要用自己的知識補充。
如果 context 中沒有答案，就回答「我不知道」。
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


