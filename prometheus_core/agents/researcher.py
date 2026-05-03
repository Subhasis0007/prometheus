from src.utils.logger import logger

def researcher_agent(state, model, tokenizer):
    prompt = f"""You are the Researcher agent. Use memory and tools to gather information.
Task: {state['messages'][-1].content}"""
    response = generate(model, tokenizer, prompt=prompt, max_tokens=600)
    logger.info(f"Researcher: {response[:100]}...")
    return {"messages": state["messages"] + [AIMessage(content=response)]}