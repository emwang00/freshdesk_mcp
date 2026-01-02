# Freshdesk MCP Server
[![smithery badge](https://smithery.ai/badge/@effytech/freshdesk_mcp)](https://smithery.ai/server/@effytech/freshdesk_mcp)

[![Trust Score](https://archestra.ai/mcp-catalog/api/badge/quality/effytech/freshdesk_mcp)](https://archestra.ai/mcp-catalog/effytech__freshdesk_mcp)

An MCP server implementation that integrates with Freshdesk, enabling AI models to interact with Freshdesk modules and perform various support operations.

## Features

- **Freshdesk Integration**: Seamless interaction with Freshdesk API endpoints
- **AI Model Support**: Enables AI models to perform support operations through Freshdesk
- **Comprehensive Operations**: Support for tickets, agents, contacts, companies, groups, canned responses, and knowledge base articles
- **Pagination Support**: Built-in pagination for list operations (tickets, agents, contacts, companies, groups)
- **Search Capabilities**: Search functionality for tickets, agents, contacts, and companies

## Components

### Tools

The server offers several tools for Freshdesk operations:

#### Ticket Operations

- `get_ticket_fields`: Get all ticket fields
  - **Inputs**: None

- `get_tickets`: Get all tickets with pagination support
  - **Inputs**:
    - `page` (number, optional, default: 1): Page number to fetch
    - `per_page` (number, optional, default: 30): Number of tickets per page (1-100)

- `get_ticket`: Get a single ticket
  - **Inputs**:
    - `ticket_id` (number, required): ID of the ticket to get

- `search_tickets`: Search for tickets based on criteria
  - **Inputs**:
    - `query` (string, required): Search query string

- `get_ticket_conversation`: Get conversation for a ticket
  - **Inputs**:
    - `ticket_id` (number, required): ID of the ticket

- `view_ticket_summary`: Get the summary of a ticket
  - **Inputs**:
    - `ticket_id` (number, required): ID of the ticket

- `view_ticket_field`: View a ticket field
  - **Inputs**:
    - `ticket_field_id` (number, required): ID of the ticket field

- `get_field_properties`: Get properties of a specific field by name
  - **Inputs**:
    - `field_name` (string, required): Name of the field

#### Agent Operations

- `get_agents`: Get all agents with pagination support
  - **Inputs**:
    - `page` (number, optional, default: 1): Page number
    - `per_page` (number, optional, default: 30): Number of agents per page (1-100)

- `view_agent`: Get a single agent
  - **Inputs**:
    - `agent_id` (number, required): ID of the agent

- `search_agents`: Search for agents
  - **Inputs**:
    - `query` (string, required): Search query

#### Contact Operations

- `list_contacts`: Get all contacts with pagination support
  - **Inputs**:
    - `page` (number, optional, default: 1): Page number
    - `per_page` (number, optional, default: 30): Contacts per page (1-100)

- `get_contact`: Get a single contact
  - **Inputs**:
    - `contact_id` (number, required): ID of the contact

- `search_contacts`: Search for contacts
  - **Inputs**:
    - `query` (string, required): Search query

- `list_contact_fields`: List all contact fields
  - **Inputs**: None

- `view_contact_field`: View a contact field
  - **Inputs**:
    - `contact_field_id` (number, required): ID of the contact field

#### Company Operations

- `list_companies`: Get all companies with pagination support
  - **Inputs**:
    - `page` (number, optional, default: 1): Page number
    - `per_page` (number, optional, default: 30): Companies per page (1-100)

- `view_company`: Get a single company
  - **Inputs**:
    - `company_id` (number, required): ID of the company

- `search_companies`: Search for companies
  - **Inputs**:
    - `query` (string, required): Search query

- `find_company_by_name`: Find a company by name
  - **Inputs**:
    - `name` (string, required): Company name

- `list_company_fields`: Get all company fields
  - **Inputs**: None

#### Group Operations

- `list_groups`: List all groups with pagination support
  - **Inputs**:
    - `page` (number, optional, default: 1): Page number
    - `per_page` (number, optional, default: 30): Groups per page (1-100)

- `view_group`: View a group
  - **Inputs**:
    - `group_id` (number, required): ID of the group

#### Canned Response Operations

- `list_canned_response_folders`: List all canned response folders
  - **Inputs**: None

- `list_canned_responses`: List all canned responses in a folder
  - **Inputs**:
    - `folder_id` (number, required): ID of the folder

- `view_canned_response`: View a canned response
  - **Inputs**:
    - `canned_response_id` (number, required): ID of the canned response

#### Solution (Knowledge Base) Operations

- `list_solution_categories`: List all solution categories
  - **Inputs**: None

- `view_solution_category`: View a solution category
  - **Inputs**:
    - `category_id` (number, required): ID of the category

- `list_solution_folders`: List all solution folders in a category
  - **Inputs**:
    - `category_id` (number, required): ID of the category

- `view_solution_category_folder`: View a solution category folder
  - **Inputs**:
    - `folder_id` (number, required): ID of the folder

- `list_solution_articles`: List all solution articles in a folder
  - **Inputs**:
    - `folder_id` (number, required): ID of the folder

- `view_solution_article`: View a solution article
  - **Inputs**:
    - `article_id` (number, required): ID of the article

## Getting Started

### Installing via Smithery

To install freshdesk_mcp for Claude Desktop automatically via [Smithery](https://smithery.ai/server/@effytech/freshdesk_mcp):

```bash
npx -y @smithery/cli install @effytech/freshdesk_mcp --client claude
```

### Prerequisites

- A Freshdesk account (sign up at [freshdesk.com](https://freshdesk.com))
- Freshdesk API key
- `uvx` installed (`pip install uv` or `brew install uv`)

### Configuration

1. Generate your Freshdesk API key from the Freshdesk admin panel
2. Set up your domain and authentication details

### Usage with Claude Desktop

1. Install Claude Desktop if you haven't already
2. Add the following configuration to your `claude_desktop_config.json`:

```json
"mcpServers": {
  "freshdesk-mcp": {
    "command": "uvx",
    "args": [
        "freshdesk-mcp"
    ],
    "env": {
      "FRESHDESK_API_KEY": "<YOUR_FRESHDESK_API_KEY>",
      "FRESHDESK_DOMAIN": "<YOUR_FRESHDESK_DOMAIN>"
    }
  }
}
```

**Important Notes**:
- Replace `YOUR_FRESHDESK_API_KEY` with your actual Freshdesk API key
- Replace `YOUR_FRESHDESK_DOMAIN` with your Freshdesk domain (e.g., `yourcompany.freshdesk.com`)

## Example Operations

Once configured, you can ask Claude to perform operations like:

- "Get all tickets from page 1"
- "Search for tickets with query 'status:2 priority:3'"
- "Get ticket conversation for ticket ID 12345"
- "List all agents"
- "Search for contacts matching 'john@example.com'"
- "Find company by name 'Acme Corporation'"
- "List all solution categories"
- "View canned responses in folder 1"


## Testing

For testing purposes, you can start the server manually:

```bash
uvx freshdesk-mcp --env FRESHDESK_API_KEY=<your_api_key> --env FRESHDESK_DOMAIN=<your_domain>
```

## Troubleshooting

- Verify your Freshdesk API key and domain are correct
- Ensure proper network connectivity to Freshdesk servers
- Check API rate limits and quotas
- Verify the `uvx` command is available in your PATH

## License

This MCP server is licensed under the MIT License. See the LICENSE file in the project repository for full details.
