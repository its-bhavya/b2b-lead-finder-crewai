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
    model='gemini/gemini-1.5-flash',
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

def clean_json(raw_block: str) -> dict:
    clean_str = re.sub(r"^```json\s*|\s*```$", "", raw_block.strip(), flags=re.DOTALL)
    return json.loads(clean_str)

# Main function for external call
def get_leads(industry: str, location: str, num_companies: int) -> dict:
    # Agents
    lead_researcher = Agent(
        role="B2B Lead Research Specialist",
        goal="Identify potential company leads based on industry and location.",
        backstory="An expert in B2B company research.",
        tools=[search_tool, web_rag_tool],
        llm=gemini_llm,
        verbose=True
    )

    linkedin_finder = Agent(
        role="LinkedIn Profile Curator",
        goal=(
            f"Given a list of company names, find ONLY valid and functional LinkedIn URLs "
            f"corresponding to official *company* pages. "
            f"Ensure that the LinkedIn profile clearly lists the company as based in or having operations in '{location}'. "
            "Ignore links that are broken, redirect to personal profiles (linkedin.com/in/), or point to companies in a different city."
        ),
        backstory=(
            f"You are a detail-oriented LinkedIn researcher who verifies not only the existence of company pages "
            f"but also confirms that they operate in '{location}'. "
            "If a company page doesn't exist or doesn't mention the specified city, skip it."
        ),
        tools=[search_tool, web_rag_tool],
        llm=gemini_llm,
        verbose=True
    )

    # Tasks
    lead_research_task = Task(
        description=f"Find {num_companies} companies in the {industry} industry located in {location}.",
        expected_output="A Python list of company names relevant to the industry and location.",
        agent=lead_researcher
    )

    linkedin_task = Task(
        description="For the list of companies, find their official LinkedIn pages. "
                    "Return a JSON with company names as keys and LinkedIn URLs as values.",
        expected_output="A raw JSON list with each company's name associated to its LinkedIn URL." \
        "Do not include companies with missing or irrelevant pages.",
        agent=linkedin_finder
    )

    crew = Crew(
        agents=[lead_researcher, linkedin_finder],
        tasks=[lead_research_task, linkedin_task],
        llm=gemini_llm,
        verbose=True,
        memory=True
    )

    results = crew.kickoff(inputs={
        'industry': industry,
        'location': location,
        'num_companies': num_companies
    })

    return clean_json(str(results))