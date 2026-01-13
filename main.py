# main.py
from server import mcp

# Import tools so they get registered via decorators
 
import tools.get_gdp_tools

# Entry point to run the server
if __name__ == "__main__":
    mcp.run()