from starlette.applications import Starlette
from starlette.routing import Route
from starlette.responses import JSONResponse

async def homepage(request):
    return JSONResponse({'message': 'Hello, World!'})

routes = [
    Route('/', homepage),
]

app = Starlette(routes=routes)
