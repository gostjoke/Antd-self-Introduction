"""
RAG 系統改進演示腳本
展示新舊版本的搜索對比
"""
from improved_rag import ImprovedRAG
from LangChainTool import *
import time
from tabulate import tabulate


def compare_rag_systems():
    """比較新舊RAG系統的性能"""
    print("🚀 RAG系統改進對比演示")
    print("="*60)
    
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
    
    # 測試查詢
    test_queries = [
        "Kevin Sin是誰？",
        "誰是NSG的總經理？",
        "什麼是LangChain？",
        "NSG團隊做什麼？",
        "如何使用FAISS？"
    ]
    
    print("🔧 初始化改進的RAG系統...")
    improved_rag = ImprovedRAG(use_openai=False)
    improved_rag.setup_documents(texts)
    
    print("📊 開始對比測試...\n")
    
    results = []
    
    for query in test_queries:
        print(f"🔍 測試查詢: '{query}'")
        print("-" * 50)
        
        # 改進版RAG
        start_time = time.time()
        improved_result = improved_rag.answer_question(query)
        improved_time = time.time() - start_time
        
        print(f"🆕 改進版回答: {improved_result['answer']}")
        print(f"⏱️ 響應時間: {improved_time:.2f}秒")
        print(f"📄 檢索到文檔數: {len(improved_result['source_documents'])}")
        
        # 搜索質量分析
        search_result = improved_rag.query_with_rerank(query, top_k=3)
        print(f"🔍 原始查詢: {search_result['original_query']}")
        print(f"🔄 處理後查詢: {search_result['processed_query']}")
        print(f"📋 重新排序的文檔:")
        for i, doc in enumerate(search_result['documents'][:2], 1):
            print(f"   {i}. {doc.page_content}")
        
        results.append({
            "query": query,
            "improved_answer": improved_result['answer'][:100] + "..." if len(improved_result['answer']) > 100 else improved_result['answer'],
            "response_time": f"{improved_time:.2f}s",
            "doc_count": len(improved_result['source_documents'])
        })
        
        print("\n" + "="*60 + "\n")
    
    # 總結表格
    print("📈 測試結果總結")
    print("="*60)
    
    table_data = []
    for result in results:
        table_data.append([
            result["query"],
            result["improved_answer"],
            result["response_time"],
            result["doc_count"]
        ])
    
    headers = ["查詢", "改進版回答", "響應時間", "檢索文檔數"]
    print(tabulate(table_data, headers=headers, tablefmt="grid", maxcolwidths=[20, 50, 10, 8]))


def demonstrate_advanced_features():
    """演示高級功能"""
    print("\n🌟 高級功能演示")
    print("="*60)
    
    rag = ImprovedRAG(use_openai=False)
    
    # 設置數據
    texts = [
        "Kevin Sin是NSG的大PM。",
        "Danny Huang是NSG的總經理。",
        "NSG是一個技術團隊。"
    ]
    
    rag.setup_documents(texts)
    
    # 功能1: 文本變體生成
    print("🔤 功能1: 文本變體生成")
    original_texts = ["Kevin Sin是NSG的大PM。"]
    variants = rag.enhance_text_variants(original_texts)
    print("原始文本:", original_texts[0])
    print("生成的變體:")
    for i, variant in enumerate(variants[1:6], 1):  # 顯示前5個變體
        print(f"  {i}. {variant}")
    
    # 功能2: 查詢預處理
    print(f"\n🔄 功能2: 查詢預處理")
    test_queries = [
        "Kevin Sin是什麼人？",
        "誰是NSG的總裁？",
        "Danny Huang負責什麼？"
    ]
    
    for query in test_queries:
        processed = rag.preprocess_query(query)
        print(f"原始: {query}")
        print(f"處理: {processed}")
        print()
    
    # 功能3: 混合檢索
    print("🔍 功能3: 混合檢索演示")
    query = "誰是PM？"
    search_result = rag.query_with_rerank(query, top_k=3)
    
    print(f"查詢: {query}")
    print(f"檢索到的文檔:")
    for i, doc in enumerate(search_result['documents'], 1):
        print(f"  {i}. {doc.page_content}")
        print(f"     元數據: {doc.metadata}")


def performance_benchmark():
    """性能基準測試"""
    print("\n⚡ 性能基準測試")
    print("="*60)
    
    rag = ImprovedRAG(use_openai=False)
    
    # 設置較大的數據集
    texts = [
        "LangChain 是一個強大的框架，用來建構 LLM 應用。",
        "FAISS 是由 Facebook AI 提供的向量檢索資料庫。",
        "你可以將文件轉換成 Embeddings，然後用 FAISS 做相似度搜尋。",
        "Kevin Sin是NSG的大PM。",
        "Danny Huang是NSG的總經理。",
        "NSG是一個技術團隊，負責開發AI相關產品。",
        "RAG系統結合了檢索和生成技術，提供更準確的答案。",
        "Python是一種流行的程式語言，廣泛用於AI開發。",
        "機器學習是人工智慧的一個分支。",
        "自然語言處理幫助電腦理解人類語言。",
    ] * 10  # 擴大數據集
    
    print(f"📚 數據集大小: {len(texts)} 個文檔")
    
    setup_start = time.time()
    rag.setup_documents(texts)
    setup_time = time.time() - setup_start
    
    print(f"🏗️ 索引建立時間: {setup_time:.2f}秒")
    
    # 測試查詢性能
    queries = [
        "Kevin Sin是誰？",
        "什麼是機器學習？",
        "NSG做什麼？",
        "如何使用Python？",
        "FAISS的功能？"
    ]
    
    total_time = 0
    for query in queries:
        start = time.time()
        result = rag.answer_question(query)
        end = time.time()
        query_time = end - start
        total_time += query_time
        
        print(f"🔍 '{query}' - {query_time:.2f}秒")
    
    avg_time = total_time / len(queries)
    print(f"📊 平均查詢時間: {avg_time:.2f}秒")
    print(f"🎯 查詢吞吐量: {1/avg_time:.1f} 查詢/秒")


def main():
    """主演示函數"""
    print("🎉 歡迎使用改進的RAG系統演示！")
    print("本演示將展示以下改進功能:")
    print("1. 增強的文本變體生成")
    print("2. 智能查詢預處理")
    print("3. 混合檢索策略 (語義+關鍵詞)")
    print("4. 文檔重新排序")
    print("5. 改進的提示工程")
    print()
    
    try:
        # 主要對比演示
        compare_rag_systems()
        
        # 高級功能演示
        demonstrate_advanced_features()
        
        # 性能測試
        performance_benchmark()
        
        print("\n✅ 演示完成！")
        print("\n📝 主要改進總結:")
        print("• 📈 提升搜索準確性：通過文本變體和同義詞處理")
        print("• 🔍 混合檢索策略：結合語義搜索和關鍵詞匹配")
        print("• 🎯 智能重新排序：基於查詢相關性重新排序結果")
        print("• 🚀 更好的用戶體驗：預處理查詢，優化提示")
        print("• 📊 豐富的評估工具：詳細的性能指標和測試框架")
        
    except Exception as e:
        print(f"❌ 演示過程中發生錯誤: {e}")
        print("請確保已安裝所有依賴和配置Ollama")


if __name__ == "__main__":
    main()
