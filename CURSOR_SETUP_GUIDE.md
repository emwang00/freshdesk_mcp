# Step-by-Step Guide: Setting Up Freshdesk MCP in Cursor

This guide will help you configure the Freshdesk MCP server to work with Cursor.

## Prerequisites

1. **Python 3.10+** installed on your system
2. **Freshdesk Account** with API access
3. **Freshdesk API Key** (get it from your Freshdesk admin panel)
4. **Freshdesk Domain** (e.g., `yourcompany.freshdesk.com`)
5. **uv** package manager (for installing the MCP server)

## Step 1: Install uv (if not already installed)

The MCP server uses `uvx` to run. Install `uv` first:

**Windows (PowerShell):**
```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

**macOS/Linux:**
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Or via pip:
```bash
pip install uv
```

## Step 2: Install the Freshdesk MCP Server

You have two options:

### Option A: Install from PyPI (if published)

If the package is published on PyPI, you can install it globally:
```bash
pip install freshdesk-mcp
```

Or use uvx (which will handle it automatically):
```bash
uvx freshdesk-mcp
```

### Option B: Install from Local GitHub Repository

If you want to use the local repository:

1. **Clone or navigate to your repository:**
   ```bash
   cd C:\Users\emily.wang\freshdesk_mcp\freshdesk_mcp
   ```

2. **Install the package in development mode:**
   ```bash
   pip install -e .
   ```

   Or using uv:
   ```bash
   uv pip install -e .
   ```

## Step 3: Locate Cursor's MCP Configuration File

Cursor stores MCP server configurations in a JSON file. The location depends on your OS:

**Windows:**
```
%APPDATA%\Cursor\User\globalStorage\rooveterinaryinc.roo-cline\settings\cline_mcp_settings.json
```

Or it might be in:
```
%APPDATA%\Cursor\User\settings.json
```

**macOS:**
```
~/Library/Application Support/Cursor/User/globalStorage/rooveterinaryinc.roo-cline/settings/cline_mcp_settings.json
```

**Linux:**
```
~/.config/Cursor/User/globalStorage/rooveterinaryinc.roo-cline/settings/cline_mcp_settings.json
```

## Step 4: Configure the MCP Server in Cursor

1. **Open the MCP settings file** in Cursor or your text editor

2. **Add the Freshdesk MCP configuration**. The file should look like this:

```json
{
  "mcpServers": {
    "freshdesk-mcp": {
      "command": "uvx",
      "args": [
        "freshdesk-mcp"
      ],
      "env": {
        "FRESHDESK_API_KEY": "YOUR_FRESHDESK_API_KEY_HERE",
        "FRESHDESK_DOMAIN": "yourcompany.freshdesk.com"
      }
    }
  }
}
```

**Important:** Replace:
- `YOUR_FRESHDESK_API_KEY_HERE` with your actual Freshdesk API key
- `yourcompany.freshdesk.com` with your actual Freshdesk domain

### Alternative: If using local installation

If you installed from the local repository, you can use Python directly:

```json
{
  "mcpServers": {
    "freshdesk-mcp": {
      "command": "python",
      "args": [
        "-m",
        "freshdesk_mcp.server"
      ],
      "env": {
        "FRESHDESK_API_KEY": "YOUR_FRESHDESK_API_KEY_HERE",
        "FRESHDESK_DOMAIN": "yourcompany.freshdesk.com"
      }
    }
  }
}
```

Or with the full path to your Python executable:

```json
{
  "mcpServers": {
    "freshdesk-mcp": {
      "command": "C:\\Python\\python.exe",
      "args": [
        "-m",
        "freshdesk_mcp.server"
      ],
      "env": {
        "FRESHDESK_API_KEY": "YOUR_FRESHDESK_API_KEY_HERE",
        "FRESHDESK_DOMAIN": "yourcompany.freshdesk.com"
      }
    }
  }
}
```

## Step 5: Get Your Freshdesk API Key

1. Log in to your Freshdesk account
2. Go to **Profile Settings** (click your profile icon)
3. Navigate to **API** section
4. Copy your API key
5. Paste it in the configuration file (replace `YOUR_FRESHDESK_API_KEY_HERE`)

## Step 6: Restart Cursor

After saving the configuration file:
1. Close Cursor completely
2. Reopen Cursor
3. The MCP server should now be available

## Step 7: Verify the Setup

1. Open a chat in Cursor
2. Try asking Cursor to use Freshdesk functions, for example:
   - "List all tickets from Freshdesk"
   - "Get ticket #12345"
   - "Search for tickets with status open"

If the MCP server is working, Cursor should be able to call these functions.

## Troubleshooting

### Issue: "uvx command not found"
**Solution:** Make sure `uv` is installed and in your PATH. Try:
```bash
uv --version
```

If it's not found, add it to your PATH or use the Python method instead.

### Issue: "Module not found: freshdesk_mcp"
**Solution:** Make sure the package is installed:
```bash
pip install -e .
```

### Issue: "Authentication failed"
**Solution:** 
- Double-check your API key is correct
- Verify your Freshdesk domain is correct (should be just the subdomain, e.g., `yourcompany`, not `https://yourcompany.freshdesk.com`)

### Issue: MCP server not appearing in Cursor
**Solution:**
- Check the JSON syntax in your configuration file (use a JSON validator)
- Make sure you restarted Cursor after making changes
- Check Cursor's logs/console for error messages

## Testing the Server Manually

You can test the server manually before configuring it in Cursor:

```bash
uvx freshdesk-mcp --env FRESHDESK_API_KEY=your_key --env FRESHDESK_DOMAIN=yourcompany.freshdesk.com
```

Or if installed locally:
```bash
python -m freshdesk_mcp.server
```

(Set environment variables in your terminal first)

## Additional Notes

- The MCP server uses stdio transport, which is compatible with Cursor
- All Freshdesk operations are available through the MCP tools
- Make sure your Freshdesk API key has the necessary permissions for the operations you want to perform

