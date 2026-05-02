from src.utils.logger import logger

def tool_creator_agent(state, model, tokenizer):
    prompt = f"""You are the ToolCreator agent. If the user asked to create a tool, generate the full @tool code."""
    response = generate(model, tokenizer, prompt=prompt, max_tokens=1000)
    logger.info(f"ToolCreator: {response[:100]}...")
    return {"messages": state["messages"] + [AIMessage(content=response)]}