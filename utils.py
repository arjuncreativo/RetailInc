import os
import aiohttp
import motor.motor_asyncio


class MongoWrapper():

    def __init__(self) -> None:
        
        self.client = None
        pass

    async def create_connection(self):
        """
        Initialize Mongo DB Connection
        Get the connections string from the environment variable
        mongodb://<user>:<password>@<host>:port/
        """
        str_connection = os.environ.get('ME_CONFIG_MONGODB_URL', None)
        self.client = motor.motor_asyncio.AsyncIOMotorClient(
            str_connection, serverSelectionTimeoutMS=5000)
        await self.client.server_info()
        self.client.db = self.client.get_database(
            os.environ.get('DB', 'myretail'))
        return self.client

    async def get_item(self, id_):
        """
        Query an Item from mongo DB
        Args:
            id_ (integer): Id used to index the item in mongo collecction

        Returns:
            dict: Dictionary with id, price and currency code
            {'_id': 13860428.0, 'value': 10.0, 'currency_code': 'USD'}
        """
        price_info = {'current_price': 'Price Not Available'}
        result = await self.client.db.price.find_one({'_id': int(id_)})
        if result:
            price_info['current_price'] = {'value': result['value'],
                                           'currency_code': result['currency_code']}
        return price_info

    async def update_item(self, id_, payload):
        """ Update the price in to Mongo db

        Args:
            payload (dict): Include Id Price and currency code

        Returns:
            _type_: _description_
        """
        try:
            inserted_id = await self.client.db.price.update_one(
                {"_id": int(id_)}, payload)
        except Exception as msg:
            inserted_id = None
        return inserted_id


async def request_url(url):
    """
    Request a url and responds back with the result set
    Parrams
    url: The Url to get the response
    type: string
    req_method: GET, POST, PUT, DELETE
    payload: The payload that should be sent in the request body
    """
    response = {}
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as results:
            try:
                dct_output = await results.json()
                response = {'name':  dct_output['data']['product']
                            ['item']['product_description']['title']}
            except Exception as msg:
                response = {'error': 'No Products found'}

    return response
