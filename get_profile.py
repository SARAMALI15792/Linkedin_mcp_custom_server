"""
Simple script to get LinkedIn profile using the custom MCP server tools
"""
import asyncio
from linkedin_mcp_server.tools import profile

async def main():
    print("Fetching your LinkedIn profile...\n")
    try:
        result = await profile.get_my_profile()
        print(result)
    except Exception as e:
        print(f"Error: {e}")
        print("\nMake sure your LINKEDIN_ACCESS_TOKEN is valid in the .env file")

if __name__ == "__main__":
    asyncio.run(main())
