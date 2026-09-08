import asyncio
import sys

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

from langchain_ollama import ChatOllama, OllamaEmbeddings
from langchain_chroma import Chroma


# ============================================================
# AI MODEL
# ============================================================

llm = ChatOllama(
    model="qwen2.5:3b",
    temperature=0
)


# ============================================================
# RAG KNOWLEDGE BASE
# ============================================================

embeddings = OllamaEmbeddings(
    model="nomic-embed-text"
)

vectorstore = Chroma(
    collection_name="it_helpdesk",
    embedding_function=embeddings,
    persist_directory="./chroma_db"
)


def search_it_knowledge(query: str) -> str:

    results = vectorstore.similarity_search(
        query,
        k=1
    )

    if not results:
        return "No relevant information found."

    return results[0].page_content


# ============================================================
# INTENT CLASSIFICATION
# ============================================================

async def classify_intent(question: str) -> str:

    prompt = f"""
You are the intent classifier for an AI IT Helpdesk Agent.

User request:

{question}


Classify the request into EXACTLY ONE of these categories:

TROUBLESHOOT
TICKET_HISTORY
SECURITY


Definitions:

TROUBLESHOOT:
The user has a normal IT problem that requires troubleshooting.

Examples:
- My internet is not working
- My printer is not working
- My computer is slow
- I forgot my password
- My software is not working


TICKET_HISTORY:
The user wants to see previous support tickets,
ticket history, existing tickets, or previously
reported issues.

Examples:
- Show my previous support tickets
- What tickets have I created?
- Show my ticket history
- What IT issues were reported?


SECURITY:
The user reports a security incident, compromised
computer, malware, suspicious activity, unauthorized
access, phishing, or another possible security threat.

Examples:
- My computer has been hacked
- I think my computer has malware
- There is a security incident
- Someone accessed my account
- I clicked a suspicious phishing link


Return ONLY one of:

TROUBLESHOOT
TICKET_HISTORY
SECURITY
"""

    response = await llm.ainvoke(prompt)

    intent = response.content.strip().upper()

    if "TICKET_HISTORY" in intent:
        return "TICKET_HISTORY"

    if "SECURITY" in intent:
        return "SECURITY"

    return "TROUBLESHOOT"


# ============================================================
# DIAGNOSTIC TOOL SELECTION
# ============================================================

async def select_diagnostic_tools(
    question: str,
    intent: str
) -> list:

    if intent == "TICKET_HISTORY":
        return []

    if intent == "SECURITY":
        return ["get_system_info"]

    prompt = f"""
You are an AI IT Helpdesk diagnostic tool selector.

User problem:

{question}


Available diagnostic tools:

1. check_internet

Use ONLY for:
- Internet problems
- Wi-Fi problems
- Network connectivity problems
- Websites not loading


2. get_system_info

Use when computer/system information could
help diagnose the problem.


Choose the useful diagnostic tools.

Return ONLY the tool names separated by commas.

Possible tools:

check_internet
get_system_info
no_tools


Examples:

Internet is not working
-> check_internet,get_system_info

Wi-Fi is disconnected
-> check_internet,get_system_info

Printer is not working
-> get_system_info

Computer is very slow
-> get_system_info

I forgot my password
-> no_tools
"""

    response = await llm.ainvoke(prompt)

    result = response.content.strip().lower()

    tools = []

    if "check_internet" in result:
        tools.append("check_internet")

    if "get_system_info" in result:
        tools.append("get_system_info")

    return tools


# ============================================================
# MAIN AGENT
# ============================================================

async def main():

    # --------------------------------------------------------
    # CONNECT TO MCP SERVER
    # --------------------------------------------------------

    server_params = StdioServerParameters(
        command=sys.executable,
        args=["mcp_server.py"]
    )

    print("\nConnecting to MCP server...")

    async with stdio_client(server_params) as (read, write):

        async with ClientSession(read, write) as session:

            await session.initialize()

            print("MCP session initialized.")


            # ------------------------------------------------
            # LIST MCP TOOLS
            # ------------------------------------------------

            tools = await session.list_tools()

            print("\nAVAILABLE MCP TOOLS")
            print("===================")

            for tool in tools.tools:
                print(f"- {tool.name}")


            # ------------------------------------------------
            # USER INPUT
            # ------------------------------------------------

            question = input(
                "\nDescribe your IT problem: "
            )


            print("\n==============================")
            print("       USER PROBLEM")
            print("==============================")

            print(question)


            # =================================================
            # STEP 1 — INTENT CLASSIFICATION
            # =================================================

            print("\n==============================")
            print("STEP 1: CLASSIFYING USER INTENT")
            print("==============================")


            intent = await classify_intent(question)


            print("\nDetected Intent:")
            print(intent)


            # =================================================
            # TICKET HISTORY
            # =================================================

            if intent == "TICKET_HISTORY":

                print("\n==============================")
                print("STEP 2: RETRIEVING SUPPORT TICKETS")
                print("==============================")


                result = await session.call_tool(
                    "get_support_tickets",
                    {}
                )


                support_tickets = result.content[0].text


                print("\nMCP Ticket History:")
                print("------------------------------")

                print(support_tickets)


                # ------------------------------------------------
                # AI TICKET SUMMARY
                # ------------------------------------------------

                print("\n==============================")
                print("AI TICKET SUMMARY")
                print("==============================")


                ticket_prompt = f"""
You are an AI IT Helpdesk Agent.

The user asked:

{question}


Previous support tickets:

{support_tickets}


Summarize the ticket information clearly.

For each ticket mention:

- Ticket ID
- Issue
- Priority
- Status
- Created time

Do not invent information.
"""


                response = await llm.ainvoke(
                    ticket_prompt
                )


                print(response.content)

                return


            # =================================================
            # SECURITY INCIDENT
            # =================================================

            if intent == "SECURITY":

                print("\n==============================")
                print("SECURITY INCIDENT DETECTED")
                print("==============================")


                print(
                    "Security incident detected."
                )

                print(
                    "Immediate escalation is required."
                )


                # ------------------------------------------------
                # GET SYSTEM INFO
                # ------------------------------------------------

                print("\n==============================")
                print("STEP 2: GETTING SYSTEM INFO")
                print("==============================")


                result = await session.call_tool(
                    "get_system_info",
                    {}
                )


                system_info = result.content[0].text


                print("\nMCP Result:")
                print(system_info)


                # ------------------------------------------------
                # CREATE HIGH PRIORITY TICKET
                # ------------------------------------------------

                print("\n==============================")
                print("STEP 3: CREATING SECURITY TICKET")
                print("==============================")


                ticket_result = await session.call_tool(
                    "create_support_ticket",
                    {
                        "issue": question,
                        "priority": "High"
                    }
                )


                ticket_info = ticket_result.content[0].text


                print("\nMCP Ticket Result:")
                print(ticket_info)


                print("\n==============================")
                print("SECURITY INCIDENT ESCALATED")
                print("==============================")


                print(
                    "The security incident has been "
                    "escalated to IT support."
                )


                return


            # =================================================
            # NORMAL TROUBLESHOOTING
            # =================================================

            print("\n==============================")
            print("STEP 2: SEARCHING KNOWLEDGE BASE")
            print("==============================")


            knowledge = search_it_knowledge(
                question
            )


            print("\nRelevant Knowledge:")
            print("------------------------------")

            print(knowledge)


            # =================================================
            # SELECT DIAGNOSTIC TOOLS
            # =================================================

            print("\n==============================")
            print("STEP 3: SELECTING MCP TOOLS")
            print("==============================")


            selected_tools = await select_diagnostic_tools(
                question,
                intent
            )


            if selected_tools:

                print("\nAI selected:")

                for tool in selected_tools:
                    print(f"- {tool}")

            else:

                print("\nAI selected:")
                print("- No diagnostic MCP tools required")


            # =================================================
            # DEFAULT TOOL RESULTS
            # =================================================

            internet_status = "Not checked."

            system_info = "Not collected."


            # =================================================
            # CHECK INTERNET
            # =================================================

            if "check_internet" in selected_tools:

                print("\n==============================")
                print("STEP 4: CHECKING INTERNET")
                print("==============================")


                result = await session.call_tool(
                    "check_internet",
                    {}
                )


                internet_status = result.content[0].text


                print("MCP Result:")
                print(internet_status)


            # =================================================
            # SYSTEM INFORMATION
            # =================================================

            if "get_system_info" in selected_tools:

                print("\n==============================")
                print("STEP 5: GETTING SYSTEM INFO")
                print("==============================")


                result = await session.call_tool(
                    "get_system_info",
                    {}
                )


                system_info = result.content[0].text


                print("MCP Result:")
                print(system_info)


            # =================================================
            # AI ANALYSIS
            # =================================================

            print("\n==============================")
            print("STEP 6: AI ANALYSIS")
            print("==============================")


            prompt = f"""
You are an AI IT Helpdesk Agent.

User problem:

{question}


========================================
IT KNOWLEDGE BASE
========================================

{knowledge}


========================================
INTERNET CHECK
========================================

{internet_status}


========================================
SYSTEM INFORMATION
========================================

{system_info}


========================================
INSTRUCTIONS
========================================

1. Use the knowledge base to troubleshoot
   the user's problem.

2. Use actual MCP results when available.

3. Do not invent information.

4. Give practical troubleshooting steps.

5. If the issue cannot be solved, recommend
   contacting IT support.


Respond using exactly:

Diagnosis:
Explain the problem.

Troubleshooting Steps:
Give numbered steps.

System Information:
Summarize the actual system information
if collected.

If not collected, say:
"System information was not collected."

Escalation:
Explain when IT support should be contacted.
"""


            response = await llm.ainvoke(
                prompt
            )


            ai_response = response.content


            print("\nAI RESPONSE:")
            print("------------------------------")

            print(ai_response)


            # =================================================
            # ESCALATION CHECK
            # =================================================

            print("\n==============================")
            print("STEP 7: ESCALATION CHECK")
            print("==============================")


            escalation_prompt = f"""
You are an IT Helpdesk escalation classifier.

User problem:

{question}


Knowledge base:

{knowledge}


Diagnostic information:

Internet:
{internet_status}

System:
{system_info}


Create a support ticket ONLY if:

- The issue cannot reasonably be solved using
  the available troubleshooting information,

OR

- The user explicitly requires IT support.


Return ONLY:

CREATE_TICKET

or

NO_TICKET
"""


            escalation_response = await llm.ainvoke(
                escalation_prompt
            )


            decision = (
                escalation_response.content
                .strip()
                .upper()
            )


            print("AI Decision:")
            print(decision)


            # =================================================
            # CREATE SUPPORT TICKET
            # =================================================

            if "CREATE_TICKET" in decision:

                print("\n==============================")
                print("STEP 8: CREATING SUPPORT TICKET")
                print("==============================")


                ticket_result = await session.call_tool(
                    "create_support_ticket",
                    {
                        "issue": question,
                        "priority": "High"
                    }
                )


                ticket_info = ticket_result.content[0].text


                print("\nMCP Ticket Result:")
                print(ticket_info)


                print("\n==============================")
                print("       TICKET CREATED")
                print("==============================")


                print(ticket_info)


            else:

                print("\n==============================")
                print("       NO TICKET REQUIRED")
                print("==============================")


                print(
                    "The issue can currently be handled "
                    "using the available troubleshooting steps."
                )


# ============================================================
# PROGRAM ENTRY
# ============================================================

if __name__ == "__main__":

    asyncio.run(main())