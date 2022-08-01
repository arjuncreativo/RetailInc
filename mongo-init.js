
db.createUser(
    {
        user: "retailuser",
        pwd: "Retail@user",
        roles: [
            {
                role: "readWrite",
                db: "myretail"
            }
        ]
    }
);
db = new Mongo().getDB("myretail");
db.createCollection('price', { capped: false });
db.price.createIndex( {_id : 1} , {unqiue : true} )

db.price.insertMany([
 {
    _id: 13860428,
    value: 10.00,
    currency_code: 'USD'
  },
  {
    _id: 13860427,
    value: 12.00,
    currency_code: 'USD'
  }
    
]);