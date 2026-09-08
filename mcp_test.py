import asyncio
import sys

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


# ==========================================
# MCP SERVER CONFIGURATION
# ==========================================

server_params = StdioServerParameters(
    command=sys.executable,
    args=["mcp_server.py"]
)


# ==========================================
# MAIN TEST
# ==========================================

async def main():

    print("Starting MCP server...")

    async with stdio_client(server_params) as (read, write):

        print("Connected to MCP server.")

        async with ClientSession(read, write) as session:

            print("Initializing MCP session...")

            await session.initialize()

            print("MCP session initialized.")


            # ==========================================
            # LIST AVAILABLE TOOLS
            # ==========================================

            tools = await session.list_tools()

            print("\nAVAILABLE MCP TOOLS:")
            print("====================")

            for tool in tools.tools:
                print(f"- {tool.name}")


            # ==========================================
            # TEST 1: CHECK INTERNET
            # ==========================================

            print("\n\nTEST 1: check_internet()")
            print("======================")

            result = await session.call_tool(
                "check_internet",
                {}
            )

            print(result.content)


            # ==========================================
            # TEST 2: SYSTEM INFORMATION
            # ==========================================

            print("\n\nTEST 2: get_system_info()")
            print("=========================")

            result = await session.call_tool(
                "get_system_info",
                {}
            )

            print(result.content)


            # ==========================================
            # TEST 3: CREATE SUPPORT TICKET
            # ==========================================

            print("\n\nTEST 3: create_support_ticket()")
            print("===============================")

            result = await session.call_tool(
                "create_support_ticket",
                {
                    "issue": "Internet is not working",
                    "priority": "High"
                }
            )

            print(result.content)


            # ==========================================
            # TEST 4: GET SUPPORT TICKETS
            # ==========================================

            print("\n\nTEST 4: get_support_tickets()")
            print("============================")

            result = await session.call_tool(
                "get_support_tickets",
                {}
            )

            print(result.content)


# ==========================================
# RUN PROGRAM
# ==========================================

if __name__ == "__main__":
    asyncio.run(main())