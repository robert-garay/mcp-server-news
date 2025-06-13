import asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from dotenv import load_dotenv

load_dotenv()

async def main():
    # Path to the MCP server script
    server_script = "mcp_news_server.py"
    
    # Set up stdio connection to the server
    server_params = StdioServerParameters(command="python", args=[server_script])
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            print("Connected to MCP News Server!")
            # List available tools
            tools = await session.list_tools()
            print("Available tools:", [t.name for t in tools.tools])
            # Prompt user for a search query
            query = input("Enter a news search query: ").strip()
            params = {"q": query, "page_size": 5}
            # Call the news.search tool
            result = await session.call_tool("news.search", params)
            print("\nTop News Results:")
            for idx, article in enumerate(result, 1):
                print(f"\n{idx}. {article['title']}")
                print(f"   Source: {article['source']}")
                print(f"   Published: {article['published_at']}")
                print(f"   URL: {article['url']}")
                if article.get('description'):
                    print(f"   Description: {article['description']}")

if __name__ == "__main__":
    asyncio.run(main()) 