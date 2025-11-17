
# 📦 Import Required Libraries
# Standard library imports for system operations and random number generation
# asyncio for running the main function asynchronously
import os
from random import randint
import asyncio


# Third-party library for loading environment variables from .env file
from dotenv import load_dotenv

# 🤖 Import Microsoft Agent Framework Components
# ChatAgent: The main agent class for conversational AI
from agent_framework import ChatAgent
# OpenAIChatClient: Client for connecting to OpenAI-compatible APIs (including GitHub Models)
from agent_framework.openai import OpenAIChatClient
# AzureOpenAIChatClient: Client for connecting to Azure OpenAI Service
from agent_framework.azure import AzureOpenAIChatClient

# 🔧 Load Environment Variables
# This loads configuration from a .env file in the project root
# Required variables if using GitHub Models: GITHUB_ENDPOINT, GITHUB_TOKEN, GITHUB_MODEL_ID
# Required variables if using Azure OpenAI Service: AZURE_OPENAI_API_KEY, AZURE_OPENAI_ENDPOINT, AZURE_OPENAI_CHAT_DEPLOYMENT_NAME, AZURE_OPENAI_API_VERSION
load_dotenv()

# 🎲 Tool Function: Random Destination Generator
# This function will be available to the agent as a tool
# The agent can call this function to get random vacation destinations
def get_random_destination() -> str:
    """Get a random vacation destination.
    
    Returns:
        str: A randomly selected destination from our predefined list
    """
    # List of popular vacation destinations around the world
    destinations = [
        "Barcelona, Spain",
        "Paris, France", 
        "Berlin, Germany",
        "Tokyo, Japan",
        "Sydney, Australia",
        "New York, USA",
        "Cairo, Egypt",
        "Cape Town, South Africa",
        "Rio de Janeiro, Brazil",
        "Bali, Indonesia"
    ]
    # Return a random destination from the list
    return destinations[randint(0, len(destinations) - 1)]



async def main():
    # 🔗 Create OpenAI Chat Client for GitHub Models
    # This client connects to GitHub Models API (OpenAI-compatible endpoint)
    # Environment variables required:
    # - GITHUB_ENDPOINT: API endpoint URL (usually https://models.inference.ai.azure.com)
    # - GITHUB_TOKEN: Your GitHub personal access token
    # - GITHUB_MODEL_ID: Model to use (e.g., gpt-4o-mini, gpt-4o)
    # openai_chat_client = OpenAIChatClient(
    #     base_url=os.environ.get("GITHUB_ENDPOINT"),
    #     api_key=os.environ.get("GITHUB_TOKEN"), 
    #     model_id=os.environ.get("GITHUB_MODEL_ID")
    # )

    # 🔗 Create Azure OpenAI Chat Client 
    # This client connects to Azure OpenAI Service
    # Environment variables required:
    # - AZURE_OPENAI_API_KEY: Your Azure OpenAI API key
    # - AZURE_OPENAI_ENDPOINT: Your Azure OpenAI endpoint URL
    # - AZURE_OPENAI_CHAT_DEPLOYMENT_NAME: Deployment name of the chat model
    # - AZURE_OPENAI_API_VERSION: API version to use (e.g., 2024-10-21)
    azure_openai_chat_client = AzureOpenAIChatClient(
        api_key=os.environ.get("AZURE_OPENAI_API_KEY"), 
        endpoint=os.environ.get("AZURE_OPENAI_ENDPOINT"),
        deployment_name=os.environ.get("AZURE_OPENAI_CHAT_DEPLOYMENT_NAME"),
        api_version=os.environ.get("AZURE_OPENAI_API_VERSION")
    )

    # 🤖 Create the Travel Planning Agent
    # This creates a conversational AI agent with specific capabilities:
    # - chat_client: The AI model client for generating responses
    # - instructions: System prompt that defines the agent's personality and role
    # - tools: List of functions the agent can call to perform actions
    agent_instructions = (
        "You are a travel planning assistant. "
        "Your job is to help users plan their trips by suggesting destinations, activities, and itineraries. "
        "Use the available tools to get random vacation destinations when needed."
        "If a user doesn't specify a destination, use the random destination tool to suggest one."
    )
    agent_tools = [get_random_destination]

    agent = ChatAgent(
        # chat_client=openai_chat_client,
        chat_client=azure_openai_chat_client,
        instructions=agent_instructions,
        tools=agent_tools  # Our random destination tool function
    )

    # print that agent is created with instructions and tools
    print("🤖 Agent created with the following instructions:")
    print(agent_instructions)
    print("🛠️ Tools available to the agent:")
    print([tool.__name__ for tool in agent_tools])
    print("\n")


    # 🚀 Run the Agent
    # Send a message to the agent and get a response
    # The agent will use its tools (get_random_destination) if needed
    user_message = "Plan me a day trip"
    print(f"👤 User: {user_message}")

    response = await agent.run(user_message)

    print("\n")
    # 📋 View Raw Response Object
    # This shows the complete response structure including metadata
    # Useful for debugging and understanding the response format
    # print("\n📝 Raw Response Object:")
    # print(response) 


    # 📖 Extract and Display the Travel Plan
    # Get the last message from the conversation (agent's response)s
    last_message = response.messages[-1]
    # Extract the text content from the message
    text_content = last_message.contents[0].text
    # Display the formatted travel plan
    print("🏖️ Travel plan:")
    print(text_content)


if __name__ == "__main__":
    asyncio.run(main())