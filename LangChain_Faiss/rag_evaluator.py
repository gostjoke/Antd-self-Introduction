import json
import time
from typing import List, Dict, Any
from improved_rag import ImprovedRAG
from tabulate import tabulate
import matplotlib.pyplot as plt
import seaborn as sns


class RAGEvaluator:
    def __init__(self):
        self.rag = ImprovedRAG(use_openai=False)
        self.test_results = []
        
    def setup_test_data(self):
        """設置測試數據"""
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
            "向量資料庫專門用於儲存和檢索高維向量數據。",
            "Embedding模型將文本轉換為數值向量表示。"
        ]
        
        self.rag.setup_documents(texts)
        
    def create_test_cases(self) -> List[Dict[str, Any]]:
        """創建測試案例"""
        return [
            {
                "query": "Kevin Sin是誰？",
                "expected_keywords": ["Kevin Sin", "PM", "NSG"],
                "category": "人物查詢"
            },
            {
                "query": "Danny Huang的職位？",
                "expected_keywords": ["Danny Huang", "總經理", "NSG"],
                "category": "職位查詢"
            },
            {
                "query": "誰是NSG的PM？",
                "expected_keywords": ["Kevin Sin", "PM"],
                "category": "反向查詢"
            },
            {
                "query": "什麼是LangChain？",
                "expected_keywords": ["LangChain", "框架", "LLM"],
                "category": "技術查詢"
            },
            {
                "query": "FAISS是什麼？",
                "expected_keywords": ["FAISS", "向量", "檢索", "資料庫"],
                "category": "技術查詢"
            },
            {
                "query": "如何使用向量搜尋？",
                "expected_keywords": ["Embeddings", "FAISS", "相似度"],
                "category": "技術指導"
            },
            {
                "query": "NSG團隊做什麼？",
                "expected_keywords": ["NSG", "技術團隊", "AI", "產品"],
                "category": "組織查詢"
            },
            {
                "query": "機器學習是什麼？",
                "expected_keywords": ["機器學習", "人工智慧", "分支"],
                "category": "概念查詢"
            }
        ]
    
    def evaluate_retrieval_quality(self, query: str, retrieved_docs: List, expected_keywords: List[str]) -> Dict[str, float]:
        """評估檢索質量"""
        if not retrieved_docs:
            return {"precision": 0.0, "recall": 0.0, "f1": 0.0}
        
        # 將所有檢索到的文本合併
        retrieved_text = " ".join([doc.page_content for doc in retrieved_docs]).lower()
        
        # 計算關鍵詞匹配
        matched_keywords = []
        for keyword in expected_keywords:
            if keyword.lower() in retrieved_text:
                matched_keywords.append(keyword)
        
        precision = len(matched_keywords) / len(expected_keywords) if expected_keywords else 0
        recall = len(matched_keywords) / len(expected_keywords) if expected_keywords else 0
        f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0
        
        return {
            "precision": precision,
            "recall": recall,
            "f1": f1,
            "matched_keywords": matched_keywords,
            "total_keywords": len(expected_keywords)
        }
    
    def evaluate_answer_quality(self, answer: str, expected_keywords: List[str]) -> Dict[str, float]:
        """評估答案質量"""
        answer_lower = answer.lower()
        
        matched_keywords = []
        for keyword in expected_keywords:
            if keyword.lower() in answer_lower:
                matched_keywords.append(keyword)
        
        keyword_coverage = len(matched_keywords) / len(expected_keywords) if expected_keywords else 0
        
        # 答案長度評分 (適中的長度得分更高)
        length_score = 1.0
        if len(answer) < 10:
            length_score = 0.3  # 太短
        elif len(answer) > 200:
            length_score = 0.7  # 太長
        
        # 檢查是否包含 "Will:" 前綴
        format_score = 1.0 if answer.startswith("Will:") else 0.5
        
        return {
            "keyword_coverage": keyword_coverage,
            "length_score": length_score,
            "format_score": format_score,
            "matched_keywords": matched_keywords
        }
    
    def run_single_test(self, test_case: Dict[str, Any]) -> Dict[str, Any]:
        """運行單個測試案例"""
        query = test_case["query"]
        expected_keywords = test_case["expected_keywords"]
        category = test_case["category"]
        
        start_time = time.time()
        
        # 執行RAG查詢
        result = self.rag.answer_question(query)
        
        end_time = time.time()
        response_time = end_time - start_time
        
        # 評估檢索質量
        retrieval_metrics = self.evaluate_retrieval_quality(
            query, result["source_documents"], expected_keywords
        )
        
        # 評估答案質量
        answer_metrics = self.evaluate_answer_quality(
            result["answer"], expected_keywords
        )
        
        return {
            "query": query,
            "category": category,
            "answer": result["answer"],
            "response_time": response_time,
            "retrieval_metrics": retrieval_metrics,
            "answer_metrics": answer_metrics,
            "source_count": len(result["source_documents"]),
            "expected_keywords": expected_keywords
        }
    
    def run_evaluation(self) -> Dict[str, Any]:
        """運行完整評估"""
        print("🚀 開始RAG系統評估...")
        
        # 設置測試數據
        self.setup_test_data()
        
        # 獲取測試案例
        test_cases = self.create_test_cases()
        
        # 運行所有測試
        self.test_results = []
        for i, test_case in enumerate(test_cases, 1):
            print(f"📝 運行測試 {i}/{len(test_cases)}: {test_case['query']}")
            result = self.run_single_test(test_case)
            self.test_results.append(result)
        
        # 計算總體統計
        overall_stats = self.calculate_overall_stats()
        
        return {
            "test_results": self.test_results,
            "overall_stats": overall_stats
        }
    
    def calculate_overall_stats(self) -> Dict[str, float]:
        """計算總體統計數據"""
        if not self.test_results:
            return {}
        
        # 檢索指標
        avg_precision = sum(r["retrieval_metrics"]["precision"] for r in self.test_results) / len(self.test_results)
        avg_recall = sum(r["retrieval_metrics"]["recall"] for r in self.test_results) / len(self.test_results)
        avg_f1 = sum(r["retrieval_metrics"]["f1"] for r in self.test_results) / len(self.test_results)
        
        # 答案指標
        avg_keyword_coverage = sum(r["answer_metrics"]["keyword_coverage"] for r in self.test_results) / len(self.test_results)
        avg_format_score = sum(r["answer_metrics"]["format_score"] for r in self.test_results) / len(self.test_results)
        
        # 性能指標
        avg_response_time = sum(r["response_time"] for r in self.test_results) / len(self.test_results)
        avg_source_count = sum(r["source_count"] for r in self.test_results) / len(self.test_results)
        
        return {
            "avg_precision": avg_precision,
            "avg_recall": avg_recall,
            "avg_f1": avg_f1,
            "avg_keyword_coverage": avg_keyword_coverage,
            "avg_format_score": avg_format_score,
            "avg_response_time": avg_response_time,
            "avg_source_count": avg_source_count,
            "total_tests": len(self.test_results)
        }
    
    def print_detailed_results(self):
        """打印詳細結果"""
        print("\n" + "="*80)
        print("📊 RAG系統評估詳細結果")
        print("="*80)
        
        for i, result in enumerate(self.test_results, 1):
            print(f"\n🔍 測試 {i}: {result['category']}")
            print(f"問題: {result['query']}")
            print(f"回答: {result['answer']}")
            print(f"響應時間: {result['response_time']:.2f}秒")
            
            # 檢索指標
            rm = result['retrieval_metrics']
            print(f"檢索指標 - Precision: {rm['precision']:.2f}, Recall: {rm['recall']:.2f}, F1: {rm['f1']:.2f}")
            
            # 答案指標
            am = result['answer_metrics']
            print(f"答案指標 - 關鍵詞覆蓋率: {am['keyword_coverage']:.2f}, 格式分數: {am['format_score']:.2f}")
            
            print(f"匹配關鍵詞: {am['matched_keywords']}")
            print("-" * 50)
    
    def print_summary(self, overall_stats: Dict[str, float]):
        """打印總結"""
        print("\n" + "="*80)
        print("📈 RAG系統評估總結")
        print("="*80)
        
        summary_data = [
            ["總測試數量", overall_stats['total_tests']],
            ["平均精確率", f"{overall_stats['avg_precision']:.2f}"],
            ["平均召回率", f"{overall_stats['avg_recall']:.2f}"],
            ["平均F1分數", f"{overall_stats['avg_f1']:.2f}"],
            ["平均關鍵詞覆蓋率", f"{overall_stats['avg_keyword_coverage']:.2f}"],
            ["平均格式分數", f"{overall_stats['avg_format_score']:.2f}"],
            ["平均響應時間", f"{overall_stats['avg_response_time']:.2f}秒"],
            ["平均來源文檔數", f"{overall_stats['avg_source_count']:.1f}"]
        ]
        
        print(tabulate(summary_data, headers=["指標", "值"], tablefmt="grid"))
        
        # 性能評級
        overall_score = (overall_stats['avg_f1'] + overall_stats['avg_keyword_coverage']) / 2
        if overall_score >= 0.8:
            grade = "優秀 🌟"
        elif overall_score >= 0.6:
            grade = "良好 👍"
        elif overall_score >= 0.4:
            grade = "普通 👌"
        else:
            grade = "需改進 ⚠️"
        
        print(f"\n🎯 整體評級: {grade} (分數: {overall_score:.2f})")
    
    def save_results(self, filename="rag_evaluation_results.json"):
        """保存評估結果"""
        evaluation_data = {
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "test_results": self.test_results,
            "overall_stats": self.calculate_overall_stats()
        }
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(evaluation_data, f, ensure_ascii=False, indent=2)
        
        print(f"📁 評估結果已保存到: {filename}")


def main():
    """主函數"""
    evaluator = RAGEvaluator()
    
    # 運行評估
    results = evaluator.run_evaluation()
    
    # 顯示結果
    evaluator.print_detailed_results()
    evaluator.print_summary(results["overall_stats"])
    
    # 保存結果
    evaluator.save_results()
    
    print("\n✅ 評估完成！")


if __name__ == "__main__":
    main()
