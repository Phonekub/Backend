from flask import Flask,jsonify,request
from flask_cors import CORS,cross_origin
from pymongo.mongo_client import MongoClient
app = Flask(__name__)
uri = "mongodb+srv://mongo:mongo@cluster0.cgejftk.mongodb.net/?retryWrites=true&w=majority"
CORS(app)
app.config['CORS_HEADERS']='Content-Type'
# products=[
# {"id":0,"name":"Notebook Acer Swift","price":45900,"img":"https://img.advice.co.th/images_nas/pic_product4/A0147295/A0147295_s.jpg"},
# {"id":1,"name":"Notebook Asus Vivo","price":19900,"img":"https://img.advice.co.th/images_nas/pic_product4/A0146010/A0146010_s.jpg"},
# {"id":2,"name":"Notebook Lenovo Ideapad","price":32900,"img":"https://img.advice.co.th/images_nas/pic_product4/A0149009/A0149009_s.jpg"},
# {"id":3,"name":"Notebook MSI Prestige","price":54900,"img":"https://img.advice.co.th/images_nas/pic_product4/A0149954/A0149954_s.jpg"},
# {"id":4,"name":"Notebook DELL XPS","price":99900,"img":"https://img.advice.co.th/images_nas/pic_product4/A0146335/A0146335_s.jpg"},
# {"id":5,"name":"Notebook HP Envy","price":46900,"img":"https://img.advice.co.th/images_nas/pic_product4/A0145712/A0145712_s.jpg"}];

client = MongoClient(uri)
db = client["products"]
collection = db["prod_info"]
products=[]
all_pro = collection.find()
for pro in all_pro:
    new_p={
        "id":pro["id"],
        "name":pro["name"],
        "price":pro["price"]
    }
    products.append(new_p)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/products",methods=["GET"])
def get_all_products():
    return jsonify(products),200

@app.route("/products",methods=["POST"])
@cross_origin()
def post_products():
    data = request.get_json(products)
    new_pro={
        "id":data["id"],
        "name":data["name"],
        "price":data["price"]
        
    }
    collection.insert_one({
        "id":data["id"],
        "name":data["name"],
        "price":data["price"]
    })
    products.append(new_pro);
    return jsonify(products),200

@app.route("/products/<int:id>",methods=["PUT"])
@cross_origin()
def put_products(id):
    pro_id=str(id)
    prod = None
    for p in products:
        t = str(p["id"])
        if t == pro_id:
            prod = p
            break
    if prod:
        data = request.get_json(products)
        prod.update(data)
        collection.update_many( {"id":pro_id},
                                {"$set":{"name":data["name"],
                                        "price":data["price"]                          
                                        }
                                })
        return jsonify(products),200
    else:
        return jsonify(products),404


@app.route("/products/<int:id>",methods=["DELETE"])
@cross_origin()
def del_products(id):
    pro_id=str(id)
    prod = None
    for p in products:
        t = str(p["id"])
        if t == pro_id:
            prod = p
            break
    if prod:
        products.remove(prod)
        collection.delete_one({"id":pro_id})
        return jsonify(products),200
    else:
        return jsonify(products),404
  


if __name__ == "__main__":
    app.run(host="0.0.0.0",port=5000,debug=True)
    
