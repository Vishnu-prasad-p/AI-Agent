from langgraph.checkpoint.sqlite import SqliteSaver
from src.agents.base import Agent, AgentsOrchestrator
from src.prompts import *
from src.tools.calendar import *
from src.tools.email import *
from src.tools.notion import *
from src.tools.slack import *
from src.tools.research import *
from src.utils import get_current_date_time

class PersonalAssistant:from langgraph.checkpoint.sqlite import SqliteSaver
from src.agents.base import Agent, AgentsOrchestrator
from src.prompts import *
from src.tools.calendar import *
from src.tools.email import *
from src.tools.notion import *
from src.tools.slack import *
from src.tools.research import *
from src.utils import get_current_date_time

class PersonalAssistant:
    def __init__(self, db_connection):
        # Create sqlite checkpointer for managing manager memory
        self.checkpointer = SqliteSaver(db_connection)
        
        # Initialize individual agents
        self.email_agent = Agent(
            name="email_agent",
            description="Email agent can manage GMAIL inbox including read and send emails",
            model="openai/gpt-4o-mini",
            system_prompt=EMAIL_AGENT_PROMPT.format(date_time=get_current_date_time()),
            tools=[read_emails, send_email, find_contact_email],
            sub_agents=[],
            temperature=0.1
        )

        self.calendar_agent = Agent(
            name="calendar_agent",
            description="Calendar agent can manage Google Calendar including get events and create events",
            model="openai/gpt-4o-mini",
            system_prompt=CALENDAR_AGENT_PROMPT.format(date_time=get_current_date_time()),
            tools=[get_calendar_events, add_event_to_calendar, find_contact_email],
            sub_agents=[],
            temperature=0.1
        )

        self.researcher_agent = Agent(
            name="researcher_agent",
            description="Researcher agent can search the web, scrape websites or LinkedIn profiles",
            model="openai/gpt-4o-mini",
            system_prompt=RESEARCHER_AGENT_PROMPT.format(date_time=get_current_date_time()),
            tools=[search_web, scrape_website_to_markdown, search_linkedin_tool],
            sub_agents=[],
            temperature=0.1
        )

        # Initialize the manager agent
        self.manager_agent = Agent(
            name="manager_agent",
            description="Manager agent",
            model="openai/gpt-4o",
            system_prompt=ASSISTANT_MANAGER_PROMPT.format(date_time=get_current_date_time()),
            tools=[],
            sub_agents=[
                self.email_agent,
                self.calendar_agent,
                self.researcher_agent
            ],
            temperature=0.1,
            memory=self.checkpointer # only manager has memory feature
        )

        # Initialize the orchestrator
        self.assistant_orchestrator = AgentsOrchestrator(
            main_agent=self.manager_agent,
            agents=[
                self.manager_agent,
                self.email_agent,
                self.calendar_agent,
                self.researcher_agent
            ]
        )

    def __getattr__(self, name):
        return getattr(self.assistant_orchestrator, name)

    def __str__(self):
        return f"PersonalAssistant(db_connection={self.checkpointer.db_connection})"

    def __repr__(self):
        return f"PersonalAssistant(db_connection={self.checkpointer.db_connection})"
    def __init__(self, db_connection):
        # Create sqlite checkpointer for managing manager memory
        self.checkpointer = SqliteSaver(db_connection)
        
        # Initialize individual agents
        self.email_agent = Agent(
            name="email_agent",
            description="Email agent can manage GMAIL inbox including read and send emails",
            model="openai/gpt-4o-mini",
            system_prompt=EMAIL_AGENT_PROMPT.format(date_time=get_current_date_time()),
            tools=[read_emails, send_email, find_contact_email],
            sub_agents=[],
            temperature=0.1
        )

        self.calendar_agent = Agent(
            name="calendar_agent",
            description="Calendar agent can manage Google Calendar including get events and create events",
            model="openai/gpt-4o-mini",
            system_prompt=CALENDAR_AGENT_PROMPT.format(date_time=get_current_date_time()),
            tools=[get_calendar_events, add_event_to_calendar, find_contact_email],
            sub_agents=[],
            temperature=0.1
        )

        self.researcher_agent = Agent(
            name="researcher_agent",
            description="Researcher agent can search the web, scrape websites or LinkedIn profiles",
            model="openai/gpt-4o-mini",
            system_prompt=RESEARCHER_AGENT_PROMPT.format(date_time=get_current_date_time()),
            tools=[search_web, scrape_website_to_markdown, search_linkedin_tool],
            sub_agents=[],
            temperature=0.1
        )

        # Initialize the manager agent
        self.manager_agent = Agent(
            name="manager_agent",
            description="Manager agent",
            model="openai/gpt-4o",
            system_prompt=ASSISTANT_MANAGER_PROMPT.format(date_time=get_current_date_time()),
            tools=[],
            sub_agents=[
                self.email_agent,
                self.calendar_agent,
                self.researcher_agent
            ],
            temperature=0.1,
            memory=self.checkpointer # only manager has memory feature
        )

        # Initialize the orchestrator
        self.assistant_orchestrator = AgentsOrchestrator(
            main_agent=self.manager_agent,
            agents=[
                self.manager_agent,
                self.email_agent,
                self.calendar_agent,
                self.researcher_agent
            ]
        )

    def __getattr__(self, name):
        return getattr(self.assistant_orchestrator, name)
