import os, re, json
import warnings
from crewai import Agent, Task, Crew, LLM
from crewai_tools import SerperDevTool, WebsiteSearchTool
from dotenv import load_dotenv
load_dotenv()

warnings.filterwarnings("ignore")

# Load API keys
gemini_api_key = os.getenv("GEMINI_API_KEY")
serper_api_key = os.getenv("SERPER_API_KEY")

# Set up LLM
gemini_llm = LLM(
    model='gemini/gemini-2.0-flash',
    api_key=gemini_api_key,
    temperature=0.0
)

# Tools
search_tool = SerperDevTool()
web_rag_tool = WebsiteSearchTool(
    api_key=serper_api_key,
    search_engine="google",
    verbose=True
)
# Agents
lead_researcher = Agent(
    role="B2B Lead Research Specialist",
    goal="Identify potential company leads based on industry and location.",
    backstory="An expert in B2B company research with sharp attention to market fit.",
    tools=[search_tool, web_rag_tool],
    llm=gemini_llm,
    verbose=True
)

linkedin_finder = Agent(
    role='LinkedIn Profile Curator',
    goal=(
        "Given a list of company names, find ONLY valid and functional LinkedIn URLs "
        "corresponding to the official *company* pages. "
        "Ignore results that point to personal profiles (linkedin.com/in/...), broken links, or return None."
    ),
    backstory=(
        "You're a diligent researcher who maps company names to their verified LinkedIn company pages. "
        "You must ensure that each link is to a valid company profile."
    ),
    tools=[search_tool, web_rag_tool],
    verbose=True,
    llm=gemini_llm
)

# Tasks
lead_research_task = Task(
    description="Find {num_companies} companies in the {industry} industry located in {location}.",
    expected_output="A Python list of company names relevant to the industry and location.",
    agent=lead_researcher
)

linkedin_task = Task(
    description="For the list of companies from the previous task, find their official LinkedIn pages. "
                "Return a JSON with company names as keys and LinkedIn URLs as values.",
    expected_output="A raw JSON list with each company's name associated to its LinkedIn URL.",
    agent=linkedin_finder
)

# Crew
crew = Crew(
    agents=[lead_researcher, linkedin_finder],
    tasks=[lead_research_task, linkedin_task],
    verbose=True,
    llm=gemini_llm
)

# Kickoff
results = crew.kickoff(inputs={
    'industry': 'Pharmaceuticals',
    'location': 'Hyderabad',
    'num_companies': 5
})

def clean_json(raw_block):
    """ Cleans a raw JSON block by removing the code block markers and extra whitespace."""
    clean_json_str = re.sub(r"^```json\s*|\s*```$", "", raw_block.strip(), flags=re.DOTALL)
    data = json.loads(clean_json_str)
    return data

print(clean_json(str(results)))
