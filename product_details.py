import os
import utils
import async_lru
from aiohttp import web


routes = web.RouteTableDef()


@routes.view('/products/{id_}')
class RetailView(web.View):

    async def get(self):
        id_ = self.request.match_info.get('id_', None)
        return web.json_response(await self.get_resp(id_))

    async def put(self):
        id_ = self.request.match_info.get('id_', None)
        body = await self.request.json()
        return web.Response(text=await self.put_req(id_, body))

    @async_lru.alru_cache
    async def get_resp(self, id_):
        print('reached')
        dct_resp_api = await utils.request_url(os.environ.get('PRODUCT_URL', '{}').format(id_))
        obj_mongo = utils.MongoWrapper()
        await obj_mongo.create_connection()
        dct_resp_mongo = await obj_mongo.get_item(id_)
        dct_resp =  { **{'id': id_}, **dct_resp_api, **dct_resp_mongo}
        return dct_resp

    async def put_req(self, id_, body):
        obj_mongo = utils.MongoWrapper()
        
        await obj_mongo.create_connection()
        payload = {"$set": {'value': body['value'],
                   'currency_code': body['currency_code']}}
        await obj_mongo.update_item(id_, payload)
        print(self.get_resp.cache_info())
        self.get_resp.cache_clear()
        return 'Update Applied'


app = web.Application()
app.add_routes(routes)
web.run_app(app)
