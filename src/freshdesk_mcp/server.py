import httpx
from mcp.server.fastmcp import FastMCP
import logging
import os
import base64
from typing import Optional, Dict, Union, Any, List
from enum import IntEnum, Enum
import re
from pydantic import BaseModel, Field

# Set up logging
logging.basicConfig(level=logging.INFO)

# Initialize FastMCP server
mcp = FastMCP("freshdesk-mcp")

FRESHDESK_API_KEY = os.getenv("FRESHDESK_API_KEY")
FRESHDESK_DOMAIN = os.getenv("FRESHDESK_DOMAIN")


def parse_link_header(link_header: str) -> Dict[str, Optional[int]]:
    """Parse the Link header to extract pagination information.

    Args:
        link_header: The Link header string from the response

    Returns:
        Dictionary containing next and prev page numbers
    """
    pagination = {
        "next": None,
        "prev": None
    }

    if not link_header:
        return pagination

    # Split multiple links if present
    links = link_header.split(',')

    for link in links:
        # Extract URL and rel
        match = re.search(r'<(.+?)>;\s*rel="(.+?)"', link)
        if match:
            url, rel = match.groups()
            # Extract page number from URL
            page_match = re.search(r'page=(\d+)', url)
            if page_match:
                page_num = int(page_match.group(1))
                pagination[rel] = page_num

    return pagination

# enums of ticket properties
class TicketSource(IntEnum):
    EMAIL = 1
    PORTAL = 2
    PHONE = 3
    CHAT = 7
    FEEDBACK_WIDGET = 9
    OUTBOUND_EMAIL = 10

class TicketStatus(IntEnum):
    OPEN = 2
    PENDING = 3
    RESOLVED = 4
    CLOSED = 5

class TicketPriority(IntEnum):
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    URGENT = 4
class AgentTicketScope(IntEnum):
    GLOBAL_ACCESS = 1
    GROUP_ACCESS = 2
    RESTRICTED_ACCESS = 3

class UnassignedForOptions(str, Enum):
    THIRTY_MIN = "30m"
    ONE_HOUR = "1h"
    TWO_HOURS = "2h"
    FOUR_HOURS = "4h"
    EIGHT_HOURS = "8h"
    TWELVE_HOURS = "12h"
    ONE_DAY = "1d"
    TWO_DAYS = "2d"
    THREE_DAYS = "3d"

@mcp.tool()
async def get_ticket_fields() -> Dict[str, Any]:
    """Get ticket fields from Freshdesk."""
    url = f"https://{FRESHDESK_DOMAIN}/api/v2/ticket_fields"
    headers = {
        "Authorization": f"Basic {base64.b64encode(f'{FRESHDESK_API_KEY}:X'.encode()).decode()}"
    }
    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers)
        return response.json()


@mcp.tool()
async def get_tickets(page: Optional[int] = 1, per_page: Optional[int] = 30) -> Dict[str, Any]:
    """Get tickets from Freshdesk with pagination support."""
    # Validate input parameters
    if page < 1:
        return {"error": "Page number must be greater than 0"}

    if per_page < 1 or per_page > 100:
        return {"error": "Page size must be between 1 and 100"}

    url = f"https://{FRESHDESK_DOMAIN}/api/v2/tickets"

    params = {
        "page": page,
        "per_page": per_page
    }

    headers = {
        "Authorization": f"Basic {base64.b64encode(f'{FRESHDESK_API_KEY}:X'.encode()).decode()}",
        "Content-Type": "application/json"
    }

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, headers=headers, params=params)
            response.raise_for_status()

            # Parse pagination from Link header
            link_header = response.headers.get('Link', '')
            pagination_info = parse_link_header(link_header)

            tickets = response.json()

            return {
                "tickets": tickets,
                "pagination": {
                    "current_page": page,
                    "next_page": pagination_info.get("next"),
                    "prev_page": pagination_info.get("prev"),
                    "per_page": per_page
                }
            }

        except httpx.HTTPStatusError as e:
            return {"error": f"Failed to fetch tickets: {str(e)}"}
        except Exception as e:
            return {"error": f"An unexpected error occurred: {str(e)}"}

@mcp.tool()
async def get_ticket(ticket_id: int):
    """Get a ticket in Freshdesk."""
    url = f"https://{FRESHDESK_DOMAIN}/api/v2/tickets/{ticket_id}"
    headers = {
        "Authorization": f"Basic {base64.b64encode(f'{FRESHDESK_API_KEY}:X'.encode()).decode()}"
    }

    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers)
        return response.json()

@mcp.tool()
async def search_tickets(query: str) -> Dict[str, Any]:
    """Search for tickets in Freshdesk."""
    url = f"https://{FRESHDESK_DOMAIN}/api/v2/search/tickets"
    headers = {
        "Authorization": f"Basic {base64.b64encode(f'{FRESHDESK_API_KEY}:X'.encode()).decode()}"
    }
    params = {"query": query}
    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers, params=params)
        return response.json()

@mcp.tool()
async def get_ticket_conversation(ticket_id: int)-> list[Dict[str, Any]]:
    """Get a ticket conversation in Freshdesk."""
    url = f"https://{FRESHDESK_DOMAIN}/api/v2/tickets/{ticket_id}/conversations"
    headers = {
        "Authorization": f"Basic {base64.b64encode(f'{FRESHDESK_API_KEY}:X'.encode()).decode()}"
    }
    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers)
        return response.json()

@mcp.tool()
async def get_agents(page: Optional[int] = 1, per_page: Optional[int] = 30)-> list[Dict[str, Any]]:
    """Get all agents in Freshdesk with pagination support."""
    # Validate input parameters
    if page < 1:
        return {"error": "Page number must be greater than 0"}

    if per_page < 1 or per_page > 100:
        return {"error": "Page size must be between 1 and 100"}
    url = f"https://{FRESHDESK_DOMAIN}/api/v2/agents"
    headers = {
        "Authorization": f"Basic {base64.b64encode(f'{FRESHDESK_API_KEY}:X'.encode()).decode()}"
    }
    params = {
        "page": page,
        "per_page": per_page
    }
    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers, params=params)
        return response.json()

@mcp.tool()
async def list_contacts(page: Optional[int] = 1, per_page: Optional[int] = 30)-> list[Dict[str, Any]]:
    """List all contacts in Freshdesk with pagination support."""
    url = f"https://{FRESHDESK_DOMAIN}/api/v2/contacts"
    headers = {
        "Authorization": f"Basic {base64.b64encode(f'{FRESHDESK_API_KEY}:X'.encode()).decode()}"
    }
    params = {
        "page": page,
        "per_page": per_page
    }
    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers, params=params)
        return response.json()

@mcp.tool()
async def get_contact(contact_id: int)-> Dict[str, Any]:
    """Get a contact in Freshdesk."""
    url = f"https://{FRESHDESK_DOMAIN}/api/v2/contacts/{contact_id}"
    headers = {
        "Authorization": f"Basic {base64.b64encode(f'{FRESHDESK_API_KEY}:X'.encode()).decode()}"
    }
    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers)
        return response.json()

@mcp.tool()
async def search_contacts(query: str)-> list[Dict[str, Any]]:
    """Search for contacts in Freshdesk."""
    url = f"https://{FRESHDESK_DOMAIN}/api/v2/contacts/autocomplete"
    headers = {
        "Authorization": f"Basic {base64.b64encode(f'{FRESHDESK_API_KEY}:X'.encode()).decode()}"
    }
    params = {"term": query}
    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers, params=params)
        return response.json()

@mcp.tool()
async def list_canned_responses(folder_id: int)-> list[Dict[str, Any]]:
    """List all canned responses in Freshdesk."""
    url = f"https://{FRESHDESK_DOMAIN}/api/v2/canned_response_folders/{folder_id}/responses"
    headers = {
        "Authorization": f"Basic {base64.b64encode(f'{FRESHDESK_API_KEY}:X'.encode()).decode()}"
    }
    canned_responses = []
    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers)
        for canned_response in response.json():
            canned_responses.append(canned_response)
    return canned_responses

@mcp.tool()
async def list_canned_response_folders()-> list[Dict[str, Any]]:
    """List all canned response folders in Freshdesk."""
    url = f"https://{FRESHDESK_DOMAIN}/api/v2/canned_response_folders"
    headers = {
        "Authorization": f"Basic {base64.b64encode(f'{FRESHDESK_API_KEY}:X'.encode()).decode()}"
    }
    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers)
        return response.json()

@mcp.tool()
async def view_canned_response(canned_response_id: int)-> Dict[str, Any]:
    """View a canned response in Freshdesk."""
    url = f"https://{FRESHDESK_DOMAIN}/api/v2/canned_responses/{canned_response_id}"
    headers = {
        "Authorization": f"Basic {base64.b64encode(f'{FRESHDESK_API_KEY}:X'.encode()).decode()}"
    }
    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers)
        return response.json()
@mcp.tool()
async def list_solution_articles(folder_id: int)-> list[Dict[str, Any]]:
    """List all solution articles in Freshdesk."""
    solution_articles = []
    url = f"https://{FRESHDESK_DOMAIN}/api/v2/solutions/folders/{folder_id}/articles"
    headers = {
        "Authorization": f"Basic {base64.b64encode(f'{FRESHDESK_API_KEY}:X'.encode()).decode()}"
    }
    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers)
        for article in response.json():
            solution_articles.append(article)
    return solution_articles

@mcp.tool()
async def list_solution_folders(category_id: int)-> list[Dict[str, Any]]:
    if not category_id:
        return {"error": "Category ID is required"}
    """List all solution folders in Freshdesk."""
    url = f"https://{FRESHDESK_DOMAIN}/api/v2/solutions/categories/{category_id}/folders"
    headers = {
        "Authorization": f"Basic {base64.b64encode(f'{FRESHDESK_API_KEY}:X'.encode()).decode()}"
    }
    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers)
        return response.json()

@mcp.tool()
async def list_solution_categories()-> list[Dict[str, Any]]:
    """List all solution categories in Freshdesk."""
    url = f"https://{FRESHDESK_DOMAIN}/api/v2/solutions/categories"
    headers = {
        "Authorization": f"Basic {base64.b64encode(f'{FRESHDESK_API_KEY}:X'.encode()).decode()}"
    }
    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers)
        return response.json()

@mcp.tool()
async def view_solution_category(category_id: int)-> Dict[str, Any]:
    """View a solution category in Freshdesk."""
    url = f"https://{FRESHDESK_DOMAIN}/api/v2/solutions/categories/{category_id}"
    headers = {
        "Authorization": f"Basic {base64.b64encode(f'{FRESHDESK_API_KEY}:X'.encode()).decode()}"
    }
    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers)
        return response.json()

@mcp.tool()
async def view_solution_category_folder(folder_id: int)-> Dict[str, Any]:
    """View a solution category folder in Freshdesk."""
    url = f"https://{FRESHDESK_DOMAIN}/api/v2/solutions/folders/{folder_id}"
    headers = {
        "Authorization": f"Basic {base64.b64encode(f'{FRESHDESK_API_KEY}:X'.encode()).decode()}"
    }
    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers)
        return response.json()
@mcp.tool()
async def view_solution_article(article_id: int)-> Dict[str, Any]:
    """View a solution article in Freshdesk."""
    url = f"https://{FRESHDESK_DOMAIN}/api/v2/solutions/articles/{article_id}"
    headers = {
        "Authorization": f"Basic {base64.b64encode(f'{FRESHDESK_API_KEY}:X'.encode()).decode()}"
    }
    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers)
        return response.json()

@mcp.tool()
async def view_agent(agent_id: int)-> Dict[str, Any]:
    """View an agent in Freshdesk."""
    url = f"https://{FRESHDESK_DOMAIN}/api/v2/agents/{agent_id}"
    headers = {
        "Authorization": f"Basic {base64.b64encode(f'{FRESHDESK_API_KEY}:X'.encode()).decode()}"
    }
    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers)
        return response.json()

@mcp.tool()
async def search_agents(query: str) -> list[Dict[str, Any]]:
    """Search for agents in Freshdesk."""
    url = f"https://{FRESHDESK_DOMAIN}/api/v2/agents/autocomplete?term={query}"
    headers = {
        "Authorization": f"Basic {base64.b64encode(f'{FRESHDESK_API_KEY}:X'.encode()).decode()}"
    }
    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers)
        return response.json()
@mcp.tool()
async def list_groups(page: Optional[int] = 1, per_page: Optional[int] = 30)-> list[Dict[str, Any]]:
    """List all groups in Freshdesk."""
    url = f"https://{FRESHDESK_DOMAIN}/api/v2/groups"
    headers = {
        "Authorization": f"Basic {base64.b64encode(f'{FRESHDESK_API_KEY}:X'.encode()).decode()}"
    }
    params = {
        "page": page,
        "per_page": per_page
    }
    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers, params=params)
        return response.json()

@mcp.tool()
async def view_group(group_id: int) -> Dict[str, Any]:
    """View a group in Freshdesk."""
    url = f"https://{FRESHDESK_DOMAIN}/api/v2/groups/{group_id}"
    headers = {
        "Authorization": f"Basic {base64.b64encode(f'{FRESHDESK_API_KEY}:X'.encode()).decode()}"
    }
    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers)
        return response.json()

@mcp.tool()
async def view_ticket_field(ticket_field_id: int) -> Dict[str, Any]:
    """View a ticket field in Freshdesk."""
    url = f"https://{FRESHDESK_DOMAIN}/api/v2/admin/ticket_fields/{ticket_field_id}"
    headers = {
        "Authorization": f"Basic {base64.b64encode(f'{FRESHDESK_API_KEY}:X'.encode()).decode()}"
    }
    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers)
        return response.json()

@mcp.tool()
async def list_contact_fields()-> list[Dict[str, Any]]:
    """List all contact fields in Freshdesk."""
    url = f"https://{FRESHDESK_DOMAIN}/api/v2/contact_fields"
    headers = {
        "Authorization": f"Basic {base64.b64encode(f'{FRESHDESK_API_KEY}:X'.encode()).decode()}"
    }
    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers)
        return response.json()

@mcp.tool()
async def view_contact_field(contact_field_id: int) -> Dict[str, Any]:
    """View a contact field in Freshdesk."""
    url = f"https://{FRESHDESK_DOMAIN}/api/v2/contact_fields/{contact_field_id}"
    headers = {
        "Authorization": f"Basic {base64.b64encode(f'{FRESHDESK_API_KEY}:X'.encode()).decode()}"
    }
    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers)
        return response.json()

@mcp.tool()
async def get_field_properties(field_name: str):
    """Get properties of a specific field by name."""
    url = f"https://{FRESHDESK_DOMAIN}/api/v2/ticket_fields"
    headers = {
        "Authorization": f"Basic {base64.b64encode(f'{FRESHDESK_API_KEY}:X'.encode()).decode()}"
    }
    actual_field_name=field_name
    if field_name == "type":
        actual_field_name="ticket_type"
    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers)
        response.raise_for_status()  # Raise error for bad status codes
        fields = response.json()
    # Filter the field by name
    matched_field = next((field for field in fields if field["name"] == actual_field_name), None)

    return matched_field

@mcp.tool()
async def list_companies(page: Optional[int] = 1, per_page: Optional[int] = 30) -> Dict[str, Any]:
    """List all companies in Freshdesk with pagination support."""
    # Validate input parameters
    if page < 1:
        return {"error": "Page number must be greater than 0"}

    if per_page < 1 or per_page > 100:
        return {"error": "Page size must be between 1 and 100"}

    url = f"https://{FRESHDESK_DOMAIN}/api/v2/companies"

    params = {
        "page": page,
        "per_page": per_page
    }

    headers = {
        "Authorization": f"Basic {base64.b64encode(f'{FRESHDESK_API_KEY}:X'.encode()).decode()}",
        "Content-Type": "application/json"
    }

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, headers=headers, params=params)
            response.raise_for_status()

            # Parse pagination from Link header
            link_header = response.headers.get('Link', '')
            pagination_info = parse_link_header(link_header)

            companies = response.json()

            return {
                "companies": companies,
                "pagination": {
                    "current_page": page,
                    "next_page": pagination_info.get("next"),
                    "prev_page": pagination_info.get("prev"),
                    "per_page": per_page
                }
            }

        except httpx.HTTPStatusError as e:
            return {"error": f"Failed to fetch companies: {str(e)}"}
        except Exception as e:
            return {"error": f"An unexpected error occurred: {str(e)}"}

@mcp.tool()
async def view_company(company_id: int) -> Dict[str, Any]:
    """Get a company in Freshdesk."""
    url = f"https://{FRESHDESK_DOMAIN}/api/v2/companies/{company_id}"
    headers = {
        "Authorization": f"Basic {base64.b64encode(f'{FRESHDESK_API_KEY}:X'.encode()).decode()}",
        "Content-Type": "application/json"
    }

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, headers=headers)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            return {"error": f"Failed to fetch company: {str(e)}"}
        except Exception as e:
            return {"error": f"An unexpected error occurred: {str(e)}"}

@mcp.tool()
async def search_companies(query: str) -> Dict[str, Any]:
    """Search for companies in Freshdesk."""
    url = f"https://{FRESHDESK_DOMAIN}/api/v2/companies/autocomplete"
    headers = {
        "Authorization": f"Basic {base64.b64encode(f'{FRESHDESK_API_KEY}:X'.encode()).decode()}",
        "Content-Type": "application/json"
    }
    # Use the name parameter as specified in the API
    params = {"name": query}

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, headers=headers, params=params)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            return {"error": f"Failed to search companies: {str(e)}"}
        except Exception as e:
            return {"error": f"An unexpected error occurred: {str(e)}"}

@mcp.tool()
async def find_company_by_name(name: str) -> Dict[str, Any]:
    """Find a company by name in Freshdesk."""
    url = f"https://{FRESHDESK_DOMAIN}/api/v2/companies/autocomplete"
    headers = {
        "Authorization": f"Basic {base64.b64encode(f'{FRESHDESK_API_KEY}:X'.encode()).decode()}",
        "Content-Type": "application/json"
    }
    params = {"name": name}

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, headers=headers, params=params)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            return {"error": f"Failed to find company: {str(e)}"}
        except Exception as e:
            return {"error": f"An unexpected error occurred: {str(e)}"}

@mcp.tool()
async def list_company_fields() -> List[Dict[str, Any]]:
    """List all company fields in Freshdesk."""
    url = f"https://{FRESHDESK_DOMAIN}/api/v2/company_fields"
    headers = {
        "Authorization": f"Basic {base64.b64encode(f'{FRESHDESK_API_KEY}:X'.encode()).decode()}",
        "Content-Type": "application/json"
    }

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, headers=headers)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            return {"error": f"Failed to fetch company fields: {str(e)}"}
        except Exception as e:
            return {"error": f"An unexpected error occurred: {str(e)}"}

@mcp.tool()
async def view_ticket_summary(ticket_id: int) -> Dict[str, Any]:
    """Get the summary of a ticket in Freshdesk."""
    url = f"https://{FRESHDESK_DOMAIN}/api/v2/tickets/{ticket_id}/summary"
    headers = {
        "Authorization": f"Basic {base64.b64encode(f'{FRESHDESK_API_KEY}:X'.encode()).decode()}",
        "Content-Type": "application/json"
    }

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, headers=headers)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            return {"error": f"Failed to fetch ticket summary: {str(e)}"}
        except Exception as e:
            return {"error": f"An unexpected error occurred: {str(e)}"}

def main():
    logging.info("Starting Freshdesk MCP server")
    mcp.run(transport='stdio')

if __name__ == "__main__":
    main()
