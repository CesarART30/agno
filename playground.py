from agno.agent import Agent
from agno.models.groq import Groq
from agno.playground import Playground
from agno.storage.sqlite import SqliteStorage
from agno.tools.duckduckgo import DuckDuckGoTools
from agno.tools.yfinance import YFinanceTools
from fastapi.middleware.cors import CORSMiddleware

agent_storage: str = "tmp/agents.db"



groq_model = Groq(
    id="llama-3.3-70b-versatile",
    api_key="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"
)
# Configuración de los agentes
web_agent = Agent(
    name="cesar Agent",
    model=groq_model,
    tools=[DuckDuckGoTools()],
    instructions=["Always include sources"],
    storage=SqliteStorage(table_name="web_agent", db_file=agent_storage),
    add_datetime_to_instructions=True,
    add_history_to_messages=True,
    num_history_responses=5,
    markdown=True,
)

finance_agent = Agent(
    name="ANGENCIA Cesar",
    model=groq_model,
    tools=[YFinanceTools(stock_price=True, analyst_recommendations=True, company_info=True, company_news=True)],
    instructions=["Always use tables to display data"],
    storage=SqliteStorage(table_name="finance_agent", db_file=agent_storage),
    add_datetime_to_instructions=True,
    add_history_to_messages=True,
    num_history_responses=5,
    markdown=True,
)

playground_app = Playground(agents=[web_agent, finance_agent])
app = playground_app.get_app()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://frontend-152767013906.europe-west1.run.app"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)