# MCP News Server

A true Model Context Protocol (MCP) server for retrieving news article data with advanced filtering capabilities, using NewsAPI.org as the backend. Includes a sample MCP client for interactive querying.

## Features
- **MCP-compliant**: Implements the official Model Context Protocol using the Python SDK.
- **Exposes a `news.search` tool**: Query news articles with filters (keywords, language, source, author, date range, etc.).
- **Real news data**: Integrates with NewsAPI.org (requires API key).
- **Sample MCP client**: Command-line client to interact with the server and display results.

## Setup
1. **Clone the repository**
2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
3. **Set up your NewsAPI key:**
   - Create a `.env` file in the project root:
     ```
     NEWS_API_KEY=your_newsapi_key_here
     ```

## Running the MCP News Server
The MCP server exposes a `news.search` tool for use by any MCP-compatible client or agent.

```bash
python mcp_news_server.py
```

## Using the Sample MCP Client
The sample client connects to the MCP server, prompts for a search query, and prints the top news results.

1. **Start the server** (in one terminal):
   ```bash
   python mcp_news_server.py
   ```
2. **Run the client** (in another terminal):
   ```bash
   python mcp_news_client.py
   ```
3. **Follow the prompt** to enter your news search query and view results.

## How It Works
- The server uses the [mcp](https://github.com/modelcontextprotocol/python-sdk) Python SDK to expose a `news.search` tool.
- The tool fetches news from NewsAPI.org using your filters.
- The client connects via MCP stdio, invokes the tool, and displays the results.

## Advanced Usage
- You can connect any MCP-compatible client (e.g., Claude Desktop, Cursor, custom agents) to this server.
- Extend the server to expose more tools, resources, or prompts as needed.

## Testing
- The original FastAPI server and tests are still available for reference, but the MCP server is the recommended entry point for agentic/LLM workflows.

---
**MCP News Server** – for powerful, flexible, and standardized news data retrieval in the AI ecosystem. 