import os
from google.adk.agents import LlmAgent
from google.adk.tools.mcp_tool.mcp_toolset import McpToolset
from google.adk.tools.mcp_tool.mcp_session_manager import StdioConnectionParams
from mcp import StdioServerParameters
from dotenv import load_dotenv

import asyncio
import pprint


# Load environment variables from .env

env_path = os.path.join(os.path.dirname(__file__), ".env")
load_dotenv(dotenv_path=env_path)

# Create the Salesforce MCP toolset
salesforce_toolset = McpToolset(
    connection_params=StdioConnectionParams(
        server_params=StdioServerParameters(
            command="npx",
            args=[
                "-y",
                "@tsmztech/mcp-server-salesforce",
            ],
            env={
                "SALESFORCE_CONNECTION_TYPE": os.getenv("SALESFORCE_CONNECTION_TYPE"),
                "SALESFORCE_USERNAME": os.getenv("SALESFORCE_USERNAME"),
                "SALESFORCE_PASSWORD": os.getenv("SALESFORCE_PASSWORD"),
                "SALESFORCE_TOKEN": os.getenv("SALESFORCE_TOKEN"),
                "SALESFORCE_INSTANCE_URL": os.getenv("SALESFORCE_INSTANCE_URL"),
            },
        )
    ),
    # Optional: filter to expose only some MCP methods
    tool_filter=[
    "salesforce_dml_records",        # for insert/update/delete
    "salesforce_query_records",      # for SELECT queries
    "salesforce_aggregate_query",    # for reports/aggregations
    "salesforce_describe_object",    # for schema details
    "salesforce_search_objects"      # to look up available objects
    ]
)

# Create the root Salesforce agent
root_agent = LlmAgent(
    model="gemini-2.0-flash",
    name="salesforce_agent",
    description="Agent specialized in Salesforce data and operations.",
    instruction="Assist users with Salesforce queries, CRUD operations, and reporting tasks.",
    tools=[salesforce_toolset],  # Attach MCP toolset here
)


