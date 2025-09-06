from flask import Flask, jsonify, request, render_template_string
from improved_rag import ImprovedRAG
import json
from datetime import datetime

app = Flask(__name__)

# 全局RAG實例
rag_instance = None

def initialize_rag():
    """初始化RAG系統"""
    global rag_instance
    
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
        "自然語言處理幫助電腦理解人類語言。"
    ]
    
    rag_instance = ImprovedRAG(use_openai=False)
    
    # 嘗試載入已存在的索引，如果失敗則重新建立
    if not rag_instance.load_index():
        print("建立新的RAG索引...")
        rag_instance.setup_documents(texts)
        rag_instance.save_index()
        print("RAG索引建立完成！")
    else:
        print("載入已存在的RAG索引！")


# 原有的API
@app.route("/hello", methods=["GET"])
def hello():
    return jsonify({"message": "Hello, Improved Flask RAG API!"})

@app.route("/echo", methods=["POST"])
def echo():
    data = request.get_json()
    return jsonify({"you_sent": data})

# 新的RAG API
@app.route("/rag/ask", methods=["POST"])
def rag_ask():
    """RAG問答API"""
    try:
        data = request.get_json()
        if not data or 'question' not in data:
            return jsonify({
                "error": "請提供 'question' 參數",
                "example": {"question": "Kevin Sin是誰？"}
            }), 400
        
        question = data['question'].strip()
        if not question:
            return jsonify({"error": "問題不能為空"}), 400
        
        # 使用RAG系統回答問題
        result = rag_instance.answer_question(question)
        
        return jsonify({
            "success": True,
            "timestamp": datetime.now().isoformat(),
            "question": result['question'],
            "processed_question": result['processed_question'],
            "answer": result['answer'],
            "source_count": len(result['source_documents']),
            "sources": [doc.page_content for doc in result['source_documents'][:3]]
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": f"處理問題時發生錯誤: {str(e)}"
        }), 500

@app.route("/rag/search", methods=["POST"])
def rag_search():
    """向量搜索API"""
    try:
        data = request.get_json()
        if not data or 'query' not in data:
            return jsonify({
                "error": "請提供 'query' 參數",
                "example": {"query": "PM"}
            }), 400
        
        query = data['query'].strip()
        top_k = data.get('top_k', 5)
        
        # 使用重新排序的搜索
        result = rag_instance.query_with_rerank(query, top_k)
        
        documents = []
        for doc in result['documents']:
            documents.append({
                "content": doc.page_content,
                "metadata": doc.metadata,
                "length": len(doc.page_content)
            })
        
        return jsonify({
            "success": True,
            "timestamp": datetime.now().isoformat(),
            "query": result['original_query'],
            "processed_query": result['processed_query'],
            "document_count": len(documents),
            "documents": documents
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": f"搜索時發生錯誤: {str(e)}"
        }), 500

@app.route("/rag/status", methods=["GET"])
def rag_status():
    """RAG系統狀態API"""
    try:
        if rag_instance is None:
            return jsonify({
                "status": "not_initialized",
                "message": "RAG系統尚未初始化"
            })
        
        # 獲取向量資料庫資訊
        vector_count = rag_instance.vector_db.index.ntotal if rag_instance.vector_db else 0
        
        return jsonify({
            "status": "ready",
            "message": "RAG系統已準備就緒",
            "vector_count": vector_count,
            "embedding_model": "llama3.2:latest" if not rag_instance.use_openai else "text-embedding-3-small",
            "llm_model": "llama3.2:latest" if not rag_instance.use_openai else "gpt-4o-mini"
        })
        
    except Exception as e:
        return jsonify({
            "status": "error",
            "error": f"獲取狀態時發生錯誤: {str(e)}"
        })

@app.route("/rag/add_document", methods=["POST"])
def add_document():
    """添加新文檔到RAG系統"""
    try:
        data = request.get_json()
        if not data or 'content' not in data:
            return jsonify({
                "error": "請提供 'content' 參數",
                "example": {"content": "新的知識內容"}
            }), 400
        
        content = data['content'].strip()
        if not content:
            return jsonify({"error": "文檔內容不能為空"}), 400
        
        # 將新文檔添加到現有的向量資料庫
        from langchain.docstore.document import Document
        new_doc = Document(
            page_content=content,
            metadata={
                "index": rag_instance.vector_db.index.ntotal,
                "type": "user_added",
                "timestamp": datetime.now().isoformat()
            }
        )
        
        # 添加到向量資料庫
        rag_instance.vector_db.add_documents([new_doc])
        
        # 保存更新的索引
        rag_instance.save_index()
        
        return jsonify({
            "success": True,
            "message": "文檔已成功添加到RAG系統",
            "document_count": rag_instance.vector_db.index.ntotal
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": f"添加文檔時發生錯誤: {str(e)}"
        }), 500

@app.route("/", methods=["GET"])
def home():
    """主頁面，提供API文檔"""
    html_template = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Improved RAG API</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 40px; }
            .endpoint { background: #f5f5f5; padding: 15px; margin: 10px 0; border-radius: 5px; }
            .method { background: #007bff; color: white; padding: 5px 10px; border-radius: 3px; }
            code { background: #e9ecef; padding: 2px 5px; border-radius: 3px; }
        </style>
    </head>
    <body>
        <h1>Improved RAG API 文檔</h1>
        
        <div class="endpoint">
            <h3><span class="method">POST</span> /rag/ask</h3>
            <p>使用RAG系統回答問題</p>
            <code>{"question": "Kevin Sin是誰？"}</code>
        </div>
        
        <div class="endpoint">
            <h3><span class="method">POST</span> /rag/search</h3>
            <p>向量相似度搜索</p>
            <code>{"query": "PM", "top_k": 5}</code>
        </div>
        
        <div class="endpoint">
            <h3><span class="method">GET</span> /rag/status</h3>
            <p>獲取RAG系統狀態</p>
        </div>
        
        <div class="endpoint">
            <h3><span class="method">POST</span> /rag/add_document</h3>
            <p>添加新文檔到知識庫</p>
            <code>{"content": "新的知識內容"}</code>
        </div>
        
        <h2>測試範例</h2>
        <p>您可以使用以下curl命令測試API：</p>
        <pre>
curl -X POST http://localhost:5000/rag/ask \
  -H "Content-Type: application/json" \
  -d '{"question": "Danny Huang是誰？"}'
        </pre>
    </body>
    </html>
    """
    return render_template_string(html_template)

if __name__ == "__main__":
    # 手動初始化RAG（用於直接運行此文件）
    initialize_rag()
    app.run(debug=True, host='0.0.0.0', port=5000)
