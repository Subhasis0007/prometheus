from crewai import Agent, Task, Crew

def create_crew_example():
    researcher = Agent(
        role='Researcher',
        goal='Research the topic',
        backstory='You are a skilled researcher'
    )
    
    task = Task(
        description='Research about AI agents in 2026',
        agent=researcher
    )
    
    crew = Crew(agents=[researcher], tasks=[task])
    return crew.kickoff()
