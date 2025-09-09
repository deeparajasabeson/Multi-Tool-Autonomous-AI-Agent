import os
import requests
import mcp

from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP

load_dotenv()

API_KEY = os.getenv('EXCHANGE_RATE_API_KEY')

mcp = FastMCP('currency-converter-server', port=8081)

@mcp.tool()
def convert_currency(amount: float, from_currency: str, to_currency: str) -> str:
    """Convert currency using real-time exchange rates"""
    url = f'https://v6.exchangerate-api.com/v6/{API_KEY}/pair/{from_currency}/{to_currency}'
    response = requests.get(url).json()
    if response.get('result') == 'error':
        return f"Error converting currency: {response.get('error-type', 'Unknown error')}"
    return (
        f'{amount} {from_currency.upper()} = '
        f'{response["conversion_result"]:.2f} {to_currency.upper()} '
        f'(Rate: {response["conversion_rate"]:.4f})'
    )

if __name__ == "__main__":
    print("Starting MCP server...")
    mcp.run()
