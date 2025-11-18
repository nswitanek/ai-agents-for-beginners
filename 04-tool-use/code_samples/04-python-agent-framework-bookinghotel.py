# # 🛠️ Advanced Tool Use with GitHub Models (Python)

# ## 📋 Learning Objectives

# This notebook demonstrates advanced tool integration patterns using the Microsoft Agent Framework with GitHub Models. You'll learn how to create, manage, and orchestrate multiple tools to build sophisticated agent capabilities.

# **Patterns:**
# - 🔧 **Multi-Tool Architecture**: Building agents with multiple specialized tools
# - 🎯 **Tool Selection Logic**: How agents choose the right tool for each task
# - 📊 **Data Processing Tools**: Creating tools that handle different data types
# - 🔗 **Tool Composition**: Combining tools for complex workflows

# ## 🎯 Key Tool Patterns

# ### Tool Design Principles
# - **Single Responsibility**: Each tool has a clear, focused purpose
# - **Type Safety**: Strong typing for reliable tool execution
# - **Error Handling**: Graceful failure and recovery patterns
# - **Composability**: Tools that work well together

# ### Advanced Tool Features
# - **Context Awareness**: Tools that understand conversation context
# - **Data Validation**: Input sanitization and output validation
# - **Performance Optimization**: efficient tool execution patterns
# - **Extensibility**: Easy addition of new tool capabilities

# ## 🔧 Technical Architecture

# ### Core Components
# - **Microsoft Agent Framework**: Python implementation with advanced tool support
# - **Azure OpenAI Models Integration**: High-performance language model access
# - **Tool Registry System**: Organized management of agent capabilities
# - **Error Recovery Patterns**: Robust handling of tool execution failures

# ### Tool Integration Flow
# User Request → Agent Analysis → Tool Selection → Tool Execution → Response Synthesis

# ## 🛠️ Tool Categories 

# ### 1. **Data Generation Tools**
# - Random destination generator
# - Weather information provider  
# - Travel cost calculator
# - Activity recommendation engine

# ### 2. **Processing Tools**
# - Text formatting and validation
# - Data transformation utilities
# - Content analysis functions
# - Response enhancement tools

# ### 3. **Integration Tools**
# - External API connectors
# - File system operations
# - Database query interfaces
# - Web scraping utilities

# ## 🎨 Design Patterns

# ### Tool Factory Pattern
# - Centralized tool creation and configuration
# - Consistent tool interface design
# - Easy tool registration and discovery

# ### Command Pattern
# - Encapsulated tool execution logic
# - Undo/redo functionality for complex operations
# - Audit logging for tool usage

# ### Observer Pattern
# - Tool execution monitoring
# - Performance metrics collection
# - Error reporting and alerting

# ## 🚀 Best Practices

# - **Tool Documentation**: Clear descriptions for agent understanding
# - **Input Validation**: Robust parameter checking and sanitization
# - **Output Formatting**: Consistent, parseable tool responses
# - **Error Messages**: Helpful error information for debugging
# - **Performance**: Optimized tool execution for responsiveness


# Import core dependencies for Agent Framework and tool integration
# This sets up the essential libraries for building intelligent agents with tool capabilities

import asyncio
import os
import json
import requests

from dotenv import load_dotenv  # For loading environment variables securely
from random import randint

# These are the core components for building tool-enabled agents
from agent_framework import ChatAgent           # Main agent class
from agent_framework import ai_function # Decorator for defining AI functions (tools)
from agent_framework.azure import AzureOpenAIChatClient  # Azure OpenAI-compatible client

# Pydantic for strong typing and data validation in tool definitions
from typing import Annotated
from pydantic import Field


# Load environment variables from .env file for secure configuration
load_dotenv()


# Define Booking Tools
@ai_function(max_invocations=3)
def booking_hotel(
    query: Annotated[str, "The name of the city"], 
    check_in_date: Annotated[str, "Hotel Check-in Time"], 
    check_out_date: Annotated[str, "Hotel Check-out Time"],
) -> Annotated[str, "Return the result of booking hotel information"]:
    """
    Function to book a hotel.
    Parameters:
    - query: The name of the city
    - check_in_date: Hotel Check-in Time
    - check_out_date: Hotel Check-out Time
    Returns:
    - The result of booking hotel information
    """

    # Define the parameters for the hotel booking request
    params = {
        "engine": "google_hotels",
        "q": query,
        "check_in_date": check_in_date,
        "check_out_date": check_out_date,
        "adults": "1",
        "currency": "USD",
        "gl": "us",
        "hl": "en",
        "api_key": os.environ.get("SERP_API_KEY")
    }

    serp_base_url = os.environ.get("SERP_API_BASE_URL") or "https://serpapi.com/search"
    
    response = requests.get(serp_base_url, params=params)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the response content as JSON
        response = response.json()
        # Return the properties from the response
        return response["properties"]
    else:
        # Return None if the request failed
        return "request failed"


@ai_function(max_invocations=3)
def booking_flight(
    origin: Annotated[str, "The name of Departure"], 
    destination: Annotated[str, "The name of Destination"], 
    outbound_date: Annotated[str, "The date of outbound flight"], 
    return_date: Annotated[str, "The date of return flight"],
) -> Annotated[str, "Return the result of booking flight information"]:
    """
    Function to book a flight.
    Parameters:
    - origin: The name of Departure
    - destination: The name of Destination
    - outbound_date: The date of outbound flight
    - return_date: The date of return flight
    - airline: The preferred airline carrier
    - hotel_brand: The preferred hotel brand
    Returns:
    - The result of booking flight information
    """
    
    # Define the parameters for the outbound flight request
    go_params = {
        "engine": "google_flights",
        "departure_id": origin,
        "arrival_id": destination,
        "outbound_date": outbound_date,
        "return_date": return_date,
        "currency": "USD",
        "hl": "en",
        "api_key": os.environ.get("SERP_API_KEY")
    }

    print(go_params)

    # Send the GET request for the outbound flight
    serp_base_url = os.environ.get("SERP_API_BASE_URL") or "https://serpapi.com/search"

    go_response = requests.get(serp_base_url, params=go_params)

    # Initialize the result string
    result = ''

    # Check if the outbound flight request was successful
    if go_response.status_code == 200:
        # Parse the response content as JSON
        response = go_response.json()
        # Append the outbound flight information to the result
        result += "# outbound \n " + str(response)
    else:
        # Print an error message if the request failed
        print('error with outbound request')

    # Define the parameters for the return flight request
    back_params = {
        "engine": "google_flights",
        "departure_id": destination,
        "arrival_id": origin,
        "outbound_date": outbound_date,
        "return_date": return_date,
        "currency": "USD",
        "hl": "en",
        "api_key": os.environ.get("SERP_API_KEY")
    }

    # Send the GET request for the return flight
    serp_base_url = os.environ.get("SERP_API_BASE_URL") or "https://serpapi.com/search"
    back_response = requests.get(serp_base_url, params=back_params)

    # Check if the return flight request was successful
    if back_response.status_code == 200:
        # Parse the response content as JSON
        response = back_response.json()
        # Append the return flight information to the result
        result += "\n # return \n" + str(response)
    else:
        # Print an error message if the request failed
        print('error with return request')

    # Print the result
    print(result)

    # Return the result
    return result

async def main():

    # 🌐 Azure OpenAI Client Integration Pattern
    azure_openai_chat_client = AzureOpenAIChatClient(
            api_key=os.environ.get("AZURE_OPENAI_API_KEY"), 
            endpoint=os.environ.get("AZURE_OPENAI_ENDPOINT"),
            deployment_name=os.environ.get("AZURE_OPENAI_CHAT_DEPLOYMENT_NAME"),
            api_version=os.environ.get("AZURE_OPENAI_API_VERSION")
        )

    AGENT_NAME ="BookingAgent"

    AGENT_INSTRUCTIONS = """
    You are a booking agent, help me to book flights or hotels.

    Thought: Understand the user's intention and confirm whether to use the reservation system to complete the task.

    Action:
    - If booking a flight, convert the departure name and destination name into airport codes.
    - If booking a hotel or flight, use the corresponding API to call. Ensure that the necessary parameters are available. If any parameters are missing, use default values or assumptions to proceed.
    - If it is not a hotel or flight booking, respond with the final answer only.
    - Output the results using a markdown table:
    - For flight bookings, separate the outbound and return contents and list them in the order of Departure_airport Name | Airline | Flight Number | Departure Time | Arrival_airport Name | Arrival Time | Duration | Airplane | Travel Class | Price (USD) | Legroom | Extensions | Carbon Emissions (kg).
    - For hotel bookings, list them in the order of Properties Name | Properties description | check_in_time | check_out_time | prices | nearby_places | hotel_class | gps_coordinates.
    """

    # 🛠️ Tool Registry Pattern
    AGENT_TOOLS = [booking_hotel, booking_flight]

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
    print([tool.func.__name__ for tool in AGENT_TOOLS])
    print([getattr(tool, '__name__', str(tool)) for tool in AGENT_TOOLS])
    print("\n")

    # 🧵 Conversation Management Pattern
    thread = agent.get_new_thread()

    # 🚀 Run the Agent
    # This is your prompt for the activity or task you want to complete 
    # Define user inputs for the agent to process we have provided some example prompts to test and validate 
    user_inputs = [
        # "Can you tell me the round-trip air ticket from  London to New York JFK aiport, the departure time is February 17, 2025, and the return time is February 23, 2025"
        # "Book a hotel in New York from Feb 20,2026 to Feb 24,2026"
        """Help me book flight tickets and hotel for the following trip 
        New York JFK Feb 20th 2026 to London Heathrow LHR returning Feb 27th 2026 
        flying economy with British Airways only. 
        I want a stay in a Hilton hotel in London 
        please provide costs for the flight and hotel"""
        # "I have a business trip from London LHR to New York JFK on Feb 20th 2026 to Feb 27th 2026, can you help me to book a hotel and flight tickets"
    ]

    user_message = user_inputs[0]
    print(f"👤 User: {user_message}")

    response1 = await agent.run(user_message, thread=thread)

    print("\n")
    # 📋 View Raw Response Object
    # This shows the complete response structure including metadata
    # Useful for debugging and understanding the response format
    # print("\n📝 Raw Response Object:")
    # print(response1) 


    # 📖 Extract and Display the booking details
    # Use the response's text property which handles different content types
    print("🏖️ Booking details:")
    print(response1.text)


if __name__ == "__main__":
    asyncio.run(main())