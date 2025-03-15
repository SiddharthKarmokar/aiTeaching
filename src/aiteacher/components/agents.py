import pandas as pd
from collections import Counter
from phi.agent import Agent
from phi.tools.duckduckgo import DuckDuckGo
from phi.knowledge.pdf import PDFUrlKnowledgeBase
from phi.vectordb.pgvector import PgVector, SearchType

# 🔹 Database Config
DB_URL = "postgresql+psycopg://ai:ai@localhost:5532/ai"
TABLE_NAME = "concept_misunderstandings"

# 🔹 Initialize VectorDB
vector_db = PgVector(table_name=TABLE_NAME, db_url=DB_URL, search_type=SearchType.hybrid)

# 🔹 Initialize Agents
search_agent = Agent(tools=[DuckDuckGo()], show_tool_calls=True)
rag_agent = Agent(knowledge=vector_db, show_tool_calls=True)

# 🔹 Function to Process CodeLlama Mistakes
def extract_recurring_mistakes(csv_path):
    df = pd.read_csv(csv_path)
    issues = [issue for analysis in df["analysis"] for issue in analysis.split("\n")]
    issue_counts = Counter(issues)
    return [issue for issue, _ in issue_counts.most_common(5)]

# 🔹 Function to Enrich with RAG
def fetch_from_rag(query):
    response = rag_agent.response(query, markdown=True)
    return response if response else "No relevant data found in the vector database."

# 🔹 Function to Fetch Learning Resources
def search_with_duckduckgo(query):
    return search_agent.response(f"How to fix {query} in programming?", markdown=True)

# 🔹 Main Function
def get_learning_resources(csv_path):
    mistakes = extract_recurring_mistakes(csv_path)
    resources = {}

    for mistake in mistakes:
        print(f"🔍 Processing: {mistake}")
        rag_result = fetch_from_rag(mistake)
        search_result = search_with_duckduckgo(mistake)

        resources[mistake] = {
            "📖 RAG Results": rag_result,
            "🌍 Web Search": search_result,
        }

    return resources

# 🔹 Run the Pipeline
if __name__ == "__main__":
    results = get_learning_resources("conceptual_misunderstandings.csv")

    # 🔹 Output Results
    for mistake, data in results.items():
        print(f"\n## 🔍 Issue: {mistake}\n")
        print(f"### 📖 RAG-Based Solution:\n{data['📖 RAG Results']}\n")
        print(f"### 🌍 DuckDuckGo Resources:\n{data['🌍 Web Search']}\n")
