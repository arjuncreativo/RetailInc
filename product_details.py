import os
import utils
import async_lru
from aiohttp import web


routes = web.RouteTableDef()


@routes.view('/products/{id_}')
class RetailView(web.View):

    async def get(self):
        """Get Product Details using Id

        Returns:
            _type_: Http Respons Json File
        """
        id_ = self.request.match_info.get('id_', None)
        return web.json_response(await self.get_resp(id_))

    async def put(self):
        id_ = self.request.match_info.get('id_', None)
        body = await self.request.json()
        return web.Response(text=await self.put_req(id_, body))

    @async_lru.alru_cache
    async def get_resp(self, id_):
        """Combine the response from myretail api and 
        Mongo db. 

        Args:
            id_ (_type_): Product id (str)

        Returns:
            _type_: Combined Json with Product and price info
        """
        dct_resp_api = await utils.request_url(os.environ.get('PRODUCT_URL', '{}').format(id_))
        obj_mongo = utils.MongoWrapper()
        await obj_mongo.create_connection()
        dct_resp_mongo = await obj_mongo.get_item(id_)
        dct_resp =  { **{'id': id_}, **dct_resp_api, **dct_resp_mongo}
        return dct_resp

    async def put_req(self, id_, body):
        """Update the Product price if product exists in the mongodb

        Args:
            id_ (_type_): Product Id(str)
            body (_type_): Json with Product price and currency code

        Returns:
            _type_: _description_
        """
        obj_mongo = utils.MongoWrapper()
        
        await obj_mongo.create_connection()
        #  Payload to update the product price
        #  If the Id is not present in the db nothing will be updated
        payload = {"$set": {'value': body['value'],
                   'currency_code': body['currency_code']}}
        await obj_mongo.update_item(id_, payload)
        self.get_resp.cache_clear()
        return 'Update Applied'


app = web.Application()
app.add_routes(routes)
web.run_app(app)
