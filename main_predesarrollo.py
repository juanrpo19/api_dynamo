import sys

import uvicorn
from api.app import create_app

application = create_app()

if __name__ == "__main__":
    args = sys.argv
    host = args[1] if len(args) > 1 else "127.0.0.1"
    port = int(args[2]) if len(args) > 2 else 8000
    uvicorn.run("main:application", reload=True, host=host, port=port)
