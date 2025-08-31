"""
簡化的RAG改進測試
"""
from improved_rag import ImprovedRAG


def quick_test():
    """快速測試改進的RAG系統"""
    print("🚀 RAG改進系統快速測試")
    print("="*50)
    
    # 創建系統
    rag = ImprovedRAG(use_openai=False)
    
    # 測試數據
    texts = [
        "Kevin Sin是NSG的大PM。",
        "Danny Huang是NSG的總經理。",
        "NSG是一個技術團隊，負責開發AI相關產品。",
        "LangChain 是一個強大的框架，用來建構 LLM 應用。",
        "FAISS 是由 Facebook AI 提供的向量檢索資料庫。"
    ]
    
    print("📚 正在建立知識庫...")
    rag.setup_documents(texts)
    
    # 測試查詢
    test_queries = [
        "Kevin Sin是誰？",
        "誰是NSG的總經理？", 
        "NSG做什麼？",
        "什麼是LangChain？"
    ]
    
    print("\n🔍 開始測試查詢...")
    print("-"*50)
    
    for i, query in enumerate(test_queries, 1):
        print(f"\n測試 {i}: {query}")
        
        # 檢查文本變體生成
        variants = rag.enhance_text_variants([query])
        print(f"生成變體數量: {len(variants)}")
        
        # 檢查查詢預處理
        processed = rag.preprocess_query(query)
        print(f"處理後查詢: {processed}")
        
        # 執行搜索
        search_result = rag.query_with_rerank(query, top_k=2)
        print(f"檢索到文檔: {len(search_result['documents'])}")
        
        for j, doc in enumerate(search_result['documents'], 1):
            print(f"  {j}. {doc.page_content}")
        
        # 獲得答案
        result = rag.answer_question(query)
        print(f"📝 答案: {result['answer']}")
        print("-"*50)
    
    print("\n✅ 測試完成！")
    
    # 保存索引
    rag.save_index("test_index")
    print("💾 索引已保存到 test_index/")


if __name__ == "__main__":
    quick_test()
