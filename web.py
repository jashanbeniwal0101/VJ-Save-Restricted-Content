#Added by @v15hnuf6n1x
from aiohttp import web

routes = web.RouteTableDef()

@routes.get("/", allow_head=True)
async def _web_(request):
    return web.json_response("Instance running....")

async def web_serve():
    web_app = web.Application()
    web_app.add_routes(routes)
    return web_app
