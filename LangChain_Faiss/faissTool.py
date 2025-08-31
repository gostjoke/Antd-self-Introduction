import faiss

# 讀取索引
index = faiss.read_index("faiss_index/index.faiss")

# 查看索引維度、向量數量
print("維度:", index.d)
print("向量數量:", index.ntotal)

# 因為 FAISS 索引本身只有向量，文件內容是存在旁邊的 index.pkl 裡。
# 所以要看原始文件，要用 LangChain 的 load_local：

from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from langchain_community.embeddings import OllamaEmbeddings

import os 
from dotenv import load_dotenv
load_dotenv()

# 環境變數
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
# embeddings = OpenAIEmbeddings(model="text-embedding-3-small", api_key=OPENAI_API_KEY)

embeddings = OllamaEmbeddings(model="llama3.2:latest")


db = FAISS.load_local("faiss_index", embeddings, allow_dangerous_deserialization=True)

# 看所有存的文件
print(db.docstore._dict)   # 一個 dict，key 是 id，value 是 Document


# 如果只想查一筆：

for k, v in db.docstore._dict.items():
    print("🆔 ID:", k)
    print("📄 內容:", v.page_content)
    print("📎 Metadata:", v.metadata)
    print("-" * 40)