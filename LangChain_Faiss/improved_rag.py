import os
import re
from typing import List, Dict, Any
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from langchain.docstore.document import Document
from langchain.retrievers import EnsembleRetriever
from langchain_community.retrievers import BM25Retriever
from langchain_community.vectorstores.utils import DistanceStrategy

# 使用新的 ollama 包
try:
    from langchain_ollama import OllamaEmbeddings, ChatOllama
except ImportError:
    from langchain_community.embeddings import OllamaEmbeddings
    from langchain_community.chat_models import ChatOllama

from dotenv import load_dotenv
load_dotenv()


class ImprovedRAG:
    def __init__(self, use_openai=False):
        self.use_openai = use_openai
        
        # 初始化 embeddings 和 LLM
        if use_openai:
            self.embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
            self.llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
        else:
            self.embeddings = OllamaEmbeddings(model="llama3.2:latest")
            self.llm = ChatOllama(model="llama3.2:latest")
        
        # 改進的文本分割器
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=300,
            chunk_overlap=50,
            separators=["\n\n", "\n", "。", "，", " ", ""]
        )
        
        self.vector_db = None
        self.bm25_retriever = None
        self.ensemble_retriever = None
        
    def enhance_text_variants(self, texts: List[str]) -> List[str]:
        """增強文本變體生成，包含更多語言模式"""
        variants = []
        
        for text in texts:
            text = text.strip("。，；,.;!?！?")
            variants.append(text)  # 原句
            
            # 處理 "是" 句型
            if "是" in text:
                parts = text.split("是", 1)
                if len(parts) == 2:
                    left, right = parts[0].strip(), parts[1].strip()
                    
                    # 倒裝句
                    variants.append(f"{right}是{left}。")
                    
                    # 問句變體
                    if left and right:
                        variants.extend([
                            f"{left}是誰？",
                            f"{left}是什麼？",
                            f"誰是{right}？",
                            f"什麼是{left}？",
                            f"{right}的身份是什麼？",
                            f"{left}的職位是什麼？"
                        ])
            
            # 處理職位/身份句型
            position_patterns = ["經理", "PM", "總監", "主管", "負責人", "工程師"]
            for pattern in position_patterns:
                if pattern in text:
                    # 提取人名和職位
                    match = re.search(rf"(\w+).*?{pattern}", text)
                    if match:
                        name = match.group(1)
                        variants.extend([
                            f"{name}的職位是什麼？",
                            f"誰是{pattern}？",
                            f"{pattern}是誰？"
                        ])
            
            # 處理技術/工具句型
            tech_keywords = ["框架", "資料庫", "工具", "技術", "平台"]
            for keyword in tech_keywords:
                if keyword in text:
                    variants.extend([
                        f"什麼是{keyword}？",
                        f"如何使用{keyword}？",
                        f"{keyword}的用途是什麼？"
                    ])
        
        return list(set(variants))  # 去重
    
    def preprocess_query(self, query: str) -> str:
        """預處理查詢，提升搜索準確性"""
        # 去除多餘空格和標點
        query = re.sub(r'\s+', ' ', query.strip())
        
        # 同義詞替換
        synonyms = {
            "總經理": ["總經理", "總裁", "CEO", "執行長"],
            "PM": ["PM", "專案經理", "項目經理", "產品經理"],
            "是誰": ["是誰", "是什麼人", "的身份"],
            "做什麼": ["做什麼", "負責什麼", "的工作"],
        }
        
        for key, values in synonyms.items():
            for value in values:
                if value in query:
                    query = query.replace(value, key)
                    break
        
        return query
    
    def setup_documents(self, texts: List[str]):
        """建立文檔集合，包含多重檢索策略"""
        # 生成增強文本變體
        enhanced_texts = self.enhance_text_variants(texts)
        
        # 創建文檔
        docs = [
            Document(
                page_content=text, 
                metadata={
                    "index": i, 
                    "length": len(text),
                    "type": "enhanced" if i >= len(texts) else "original"
                }
            )
            for i, text in enumerate(enhanced_texts)
        ]
        
        # 建立向量資料庫 (使用餘弦相似度)
        self.vector_db = FAISS.from_documents(
            docs, 
            self.embeddings,
            distance_strategy=DistanceStrategy.COSINE
        )
        
        # 建立 BM25 檢索器 (關鍵詞匹配)
        self.bm25_retriever = BM25Retriever.from_documents(docs)
        self.bm25_retriever.k = 3
        
        # 建立向量檢索器
        vector_retriever = self.vector_db.as_retriever(
            search_type="similarity_score_threshold",
            search_kwargs={
                "k": 5,
                "score_threshold": 0.1  # 降低閾值以獲得更多結果
            }
        )
        
        # 組合檢索器 (混合語義和關鍵詞搜索)
        self.ensemble_retriever = EnsembleRetriever(
            retrievers=[vector_retriever, self.bm25_retriever],
            weights=[0.7, 0.3]  # 70% 語義搜索，30% 關鍵詞搜索
        )
    
    def create_advanced_chain(self):
        """創建進階問答鏈"""
        system_prompt = """
你是一個專業的AI助手。請根據以下檢索到的上下文資訊來回答問題。

回答規則：
1. 每句話開頭以 "Will:" 
2. 只能根據提供的上下文 (context) 來回答
3. 如果上下文中沒有相關資訊，回答「我不知道」
4. 回答要簡潔明確，最多使用三句話
5. 如果問的是人物身份或職位，直接回答該身份
6. 如果上下文中有多個相關資訊，選擇最相關的回答

上下文資訊：
{context}
"""

        prompt = ChatPromptTemplate.from_messages([
            ("system", system_prompt),
            ("human", "{input}"),
        ])
        
        # 建立問答鏈
        question_answer_chain = create_stuff_documents_chain(self.llm, prompt)
        qa_chain = create_retrieval_chain(self.ensemble_retriever, question_answer_chain)
        
        return qa_chain
    
    def query_with_rerank(self, query: str, top_k: int = 3) -> Dict[str, Any]:
        """使用重新排序的查詢方法"""
        # 預處理查詢
        processed_query = self.preprocess_query(query)
        
        # 使用ensemble retriever獲取候選文檔
        candidate_docs = self.ensemble_retriever.get_relevant_documents(processed_query)
        
        # 簡單的重新排序策略：基於查詢匹配度
        def score_document(doc, query):
            content = doc.page_content.lower()
            query_terms = query.lower().split()
            score = 0
            
            # 完全匹配得分更高
            if query.lower() in content:
                score += 10
            
            # 關鍵詞匹配
            for term in query_terms:
                if term in content:
                    score += 1
            
            # 原始文檔得分更高
            if doc.metadata.get("type") == "original":
                score += 2
                
            return score
        
        # 重新排序
        scored_docs = [(doc, score_document(doc, processed_query)) for doc in candidate_docs]
        scored_docs.sort(key=lambda x: x[1], reverse=True)
        
        # 取前 top_k 個
        reranked_docs = [doc for doc, score in scored_docs[:top_k]]
        
        return {
            "documents": reranked_docs,
            "processed_query": processed_query,
            "original_query": query
        }
    
    def answer_question(self, query: str) -> Dict[str, Any]:
        """回答問題的主要方法"""
        # 創建問答鏈
        qa_chain = self.create_advanced_chain()
        
        # 預處理查詢
        processed_query = self.preprocess_query(query)
        
        # 執行問答
        result = qa_chain.invoke({"input": processed_query})
        
        # 獲取重新排序的文檔用於調試
        rerank_result = self.query_with_rerank(query)
        
        return {
            "question": query,
            "processed_question": processed_query,
            "answer": result["answer"],
            "source_documents": result.get("context", []),
            "reranked_documents": rerank_result["documents"]
        }
    
    def save_index(self, path="faiss_index_improved"):
        """保存向量索引"""
        if self.vector_db:
            self.vector_db.save_local(path)
    
    def load_index(self, path="faiss_index_improved"):
        """載入向量索引"""
        try:
            self.vector_db = FAISS.load_local(
                path, 
                self.embeddings, 
                allow_dangerous_deserialization=True
            )
            return True
        except:
            return False


def main():
    # 測試數據
    texts = [
        "LangChain 是一個強大的框架，用來建構 LLM 應用。",
        "FAISS 是由 Facebook AI 提供的向量檢索資料庫。",
        "你可以將文件轉換成 Embeddings，然後用 FAISS 做相似度搜尋。",
        "Kevin Sin是NSG的大PM。",
        "Danny Huang是NSG的總經理。",
        "NSG是一個技術團隊，負責開發AI相關產品。",
        "RAG系統結合了檢索和生成技術，提供更準確的答案。",
    ]
    
    # 創建改進的RAG系統
    rag = ImprovedRAG(use_openai=False)  # 使用Ollama
    
    # 設置文檔
    print("正在建立改進的RAG系統...")
    rag.setup_documents(texts)
    
    # 保存索引
    rag.save_index()
    print("索引已保存!")
    
    # 交互式問答
    print("\n改進的RAG系統已準備就緒！輸入 'quit' 結束。")
    print("="*50)
    
    while True:
        query = input("\n請輸入你的問題: ")
        if query.lower() in ['quit', 'exit', 'q']:
            break
            
        result = rag.answer_question(query)
        
        print(f"\n問題: {result['question']}")
        print(f"處理後的問題: {result['processed_question']}")
        print(f"回答: {result['answer']}")
        
        # 顯示來源文檔
        print(f"\n檢索到的文檔數量: {len(result['source_documents'])}")
        for i, doc in enumerate(result['source_documents'][:3]):
            print(f"  文檔 {i+1}: {doc.page_content}")


if __name__ == "__main__":
    main()
