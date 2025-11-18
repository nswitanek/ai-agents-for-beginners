# # 🎨 Agentic Design Patterns with GitHub Models (Python)

# ## 📋 Learning Objectives

# This file demonstrates essential design patterns for building intelligent agents using the Microsoft Agent Framework with GitHub Models integration. You'll learn proven patterns and architectural approaches that make agents more robust, maintainable, and effective.

# **Core Design Patterns Covered:**
# - 🏗️ **Agent Factory Pattern**: Standardized agent creation and configuration
# - 🔧 **Tool Registry Pattern**: Organized approach to managing agent capabilities
# - 🧵 **Conversation Management**: Effective patterns for multi-turn interactions
# - 🔄 **Response Processing**: Best practices for handling agent outputs

# ## 🎯 Key Architectural Concepts

# ### Design Principles
# - **Separation of Concerns**: Clear boundaries between agent logic, tools, and configuration
# - **Composability**: Building complex agents from reusable components
# - **Extensibility**: Patterns that allow easy addition of new capabilities
# - **Testability**: Design for easy unit testing and validation

# ### Azure OpenAI Models Integration
# - **Model Selection**: Choosing appropriate models for different use cases

# ## 🔧 Technical Architecture

# ### Core Components
# - **Microsoft Agent Framework**: Python implementation with Azure OpenAI Models support
# - **Azure OpenAI Service**: Access to state-of-the-art language models
# - **OpenAI Client Pattern**: Standardized API interaction patterns
# - **Environment Configuration**: Secure and flexible configuration management

# ### Design Pattern Benefits
# - **Maintainability**: Clear code organization and structure
# - **Scalability**: Patterns that grow with your application needs
# - **Reliability**: Proven approaches that handle edge cases
# - **Performance**: Efficient resource utilization and API usage


# ## 📚 Design Pattern Categories

# ### 1. **Creational Patterns**
# - Agent factory and builder patterns
# - Configuration management patterns
# - Dependency injection for agent services

# ### 2. **Behavioral Patterns**
# - Tool execution and orchestration
# - Conversation flow management  
# - Response processing and formatting

# ### 3. **Integration Patterns**
# - Azure OpenAI Service integration
# - Error handling and retry logic
# - Resource management and cleanup

# ## 🚀 Best Practices Demonstrated

# - **Clean Architecture**: Layered design with clear responsibilities
# - **Error Handling**: Comprehensive exception management
# - **Configuration**: Environment-based setup for different environments
# - **Testing**: Patterns that enable effective unit and integration testing
# - **Documentation**: Self-documenting code with clear intent

# 📦 Import Core Libraries for Agent Design Patterns
import os                     # Environment variable access for configuration management
from random import randint    # Random selection utilities for tool functionality
import asyncio               # Asynchronous programming support

from dotenv import load_dotenv  # Secure environment configuration loading


# 🤖 Import Microsoft Agent Framework Components  
# ChatAgent: Core agent orchestration class following factory pattern
# AzureOpenAIChatClient: Azure OpenAI Models integration following adapter pattern
from agent_framework import ChatAgent
from agent_framework.azure import AzureOpenAIChatClient

# 🔧 Configuration Loading Pattern
# Implement configuration management pattern for secure credential handling
# This follows the external configuration principle for cloud-native applications
load_dotenv()

# 🛠️ Tool Function Design Pattern
# Implements the Strategy Pattern for pluggable agent capabilities
# This demonstrates clean separation of business logic from agent orchestration
def get_random_destination() -> str:
    """Get a random vacation destination using Repository Pattern.
    
    This function exemplifies several design patterns:
    - Strategy Pattern: Interchangeable algorithm for destination selection
    - Repository Pattern: Encapsulates data access logic
    - Factory Method: Creates destination objects on demand
    
    Returns:
        str: A randomly selected destination following consistent format
    """
    # Data Repository Pattern: Centralized destination data management
    destinations = [
        "Barcelona, Spain",      # Mediterranean cultural hub
        "Paris, France",         # European artistic center
        "Berlin, Germany",       # Historical European capital
        "Tokyo, Japan",          # Asian technology metropolis
        "Sydney, Australia",     # Oceanic coastal city
        "New York, USA",         # American urban center
        "Cairo, Egypt",          # African historical capital
        "Cape Town, South Africa", # African scenic destination
        "Rio de Janeiro, Brazil",  # South American beach city
        "Bali, Indonesia"          # Southeast Asian island paradise
    ]
    
    # Factory Method Pattern: Create destination selection on demand
    return destinations[randint(0, len(destinations) - 1)]


async def main():

    # 🌐 Azure OpenAI Client Integration Pattern
    azure_openai_chat_client = AzureOpenAIChatClient(
            api_key=os.environ.get("AZURE_OPENAI_API_KEY"), 
            endpoint=os.environ.get("AZURE_OPENAI_ENDPOINT"),
            deployment_name=os.environ.get("AZURE_OPENAI_CHAT_DEPLOYMENT_NAME"),
            api_version=os.environ.get("AZURE_OPENAI_API_VERSION")
        )

    AGENT_NAME ="TravelAgent"

    AGENT_INSTRUCTIONS = """You are a helpful AI Agent that can help plan vacations for customers.

    Important: When users specify a destination, always plan for that location. Only suggest random destinations when the user hasn't specified a preference.

    When the conversation begins, introduce yourself with this message:
    "Hello! I'm your TravelAgent assistant. I can help plan vacations and suggest interesting destinations for you. Here are some things you can ask me:
    1. Plan a day trip to a specific location
    2. Suggest a random vacation destination
    3. Find destinations with specific features (beaches, mountains, historical sites, etc.)
    4. Plan an alternative trip if you don't like my first suggestion

    What kind of trip would you like me to help you plan today?"

    Always prioritize user preferences. If they mention a specific destination like "Bali" or "Paris," focus your planning on that location rather than suggesting alternatives.
    """

    # 🛠️ Tool Registry Pattern
    AGENT_TOOLS = [get_random_destination]

    # 🤖 Agent Factory Pattern
    agent = ChatAgent(
        name = AGENT_NAME,
        chat_client=azure_openai_chat_client,
        instructions=AGENT_INSTRUCTIONS,
        tools=AGENT_TOOLS
    )

    # print that agent is created with instructions and tools
    print("🤖 Agent created with the following instructions:")
    print(AGENT_INSTRUCTIONS)
    print("🛠️ Tools available to the agent:")
    print([tool.__name__ for tool in AGENT_TOOLS])
    print("\n")

    # 🧵 Conversation Management Pattern
    thread = agent.get_new_thread()

    # 🚀 Run the Agent
    # Send a message to the agent and get a response
    # The agent will use its tools (get_random_destination) if needed
    user_message = "Plan me a day trip"
    print(f"👤 User: {user_message}")

    response1 = await agent.run(user_message, thread=thread)

    print("\n")
    # 📋 View Raw Response Object
    # This shows the complete response structure including metadata
    # Useful for debugging and understanding the response format
    # print("\n📝 Raw Response Object:")
    # print(response1) 


    # 📖 Extract and Display the Travel Plan
    # Get the last message from the conversation (agent's response)s
    last_message = response1.messages[-1]
    # Extract the text content from the message
    text_content = last_message.contents[0].text
    # Display the formatted travel plan
    print("🏖️ Travel plan:")
    print(text_content)


if __name__ == "__main__":
    asyncio.run(main())

