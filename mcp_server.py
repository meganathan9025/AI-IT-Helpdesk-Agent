from mcp.server.mcpserver import MCPServer

import socket
import platform
import uuid
import json
from pathlib import Path
from datetime import datetime


server = MCPServer("IT Helpdesk Tools")


# ==========================================
# TICKET STORAGE
# ==========================================

TICKET_FILE = Path("tickets.json")


def load_tickets():

    if not TICKET_FILE.exists():
        return []

    try:
        with open(
            TICKET_FILE,
            "r",
            encoding="utf-8"
        ) as file:

            return json.load(file)

    except (json.JSONDecodeError, OSError):
        return []


def save_tickets(tickets):

    with open(
        TICKET_FILE,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            tickets,
            file,
            indent=4
        )


# ==========================================
# TOOL 1: CHECK INTERNET
# ==========================================

@server.tool()
def check_internet() -> str:
    """Check whether the computer has an internet connection."""

    try:

        socket.create_connection(
            ("8.8.8.8", 53),
            timeout=3
        )

        return "Internet connection is working."

    except OSError:

        return "Internet connection is not working."


# ==========================================
# TOOL 2: SYSTEM INFORMATION
# ==========================================

@server.tool()
def get_system_info() -> str:
    """Get basic information about the computer."""

    return (
        f"Operating System: {platform.system()}\n"
        f"OS Version: {platform.version()}\n"
        f"Machine: {platform.machine()}\n"
        f"Processor: {platform.processor()}"
    )


# ==========================================
# TOOL 3: CREATE SUPPORT TICKET
# ==========================================

@server.tool()
def create_support_ticket(
    issue: str,
    priority: str = "Medium"
) -> str:
    """Create and persist an IT support ticket."""

    ticket_id = (
        "IT-"
        + str(uuid.uuid4())[:8].upper()
    )

    ticket = {
        "ticket_id": ticket_id,
        "issue": issue,
        "priority": priority,
        "status": "Open",
        "created_at": datetime.now().isoformat(
            timespec="seconds"
        )
    }

    tickets = load_tickets()

    tickets.append(ticket)

    save_tickets(tickets)

    return (
        "Support ticket created successfully.\n"
        f"Ticket ID: {ticket_id}\n"
        f"Issue: {issue}\n"
        f"Priority: {priority}\n"
        "Status: Open\n"
        f"Created At: {ticket['created_at']}"
    )


# ==========================================
# TOOL 4: GET SUPPORT TICKETS
# ==========================================

@server.tool()
def get_support_tickets() -> str:
    """Retrieve all stored IT support tickets."""

    tickets = load_tickets()

    if not tickets:
        return "No support tickets found."

    output = []

    for ticket in tickets:

        output.append(
            f"Ticket ID: {ticket['ticket_id']}\n"
            f"Issue: {ticket['issue']}\n"
            f"Priority: {ticket['priority']}\n"
            f"Status: {ticket['status']}\n"
            f"Created At: {ticket['created_at']}"
        )

    return "\n\n------------------------------\n\n".join(
        output
    )


# ==========================================
# START MCP SERVER
# ==========================================

if __name__ == "__main__":

    server.run(
        transport="stdio"
    )