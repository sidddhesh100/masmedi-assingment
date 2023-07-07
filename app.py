from flask import Flask
from flask import Response, request
import json
from pymongo import MongoClient
import uuid
from datetime import datetime


app = Flask(__name__)

app.config["DB_CONN"] = MongoClient("mongodb://localhost:27017")

MIME_TYPE = "application/json"


@app.route("/create_product/", methods=["POST"])
def create_product():
    """Create product
    This api is use to add product

    request body:
        - product_name(str): name of the product
        - product_quantiyt(int): quantity

    Returns:
        Response:
            - status: successful or not
            - message: error message or successful message
            - product_id: Id of the created product
    """
    request_body = request.get_json()
    request_body["product_id"] = str(uuid.uuid4())
    request_body["created_date"] = datetime.now()
    request_body["is_sold"] = False
    app.config["DB_CONN"]["masmedi"]["products"].insert_one(request_body)
    return Response(json.dumps({
        "status":True,
        "message": "product created successfully",
        "product_id": request_body["product_id"]
    }), mimetype=MIME_TYPE)

@app.route("/update_product/", methods=["POST"])
def update_product():
    """Update product
    This api is use to Update the existing product

    request body:
        - product_id(str): unique id of the product
        - update_details(object): dictionary object contains details which need to be updated

    Returns:
        Response:
            - status: successful or not
            - message: error message or successful message
            - product_id: Id of the created product
    """
    body = request.get_json()
    if not body.get("product_id"):
        return Response(json.dumps({
            "status":False,
            "message":"Please provide product Id"
        }), mimetype=MIME_TYPE)
    if len(body.get("update_details"))==0:
        return Response(json.dumps({
            "status":False,
            "message":"Please provide the details which need to be updated"
        }), mimetype=MIME_TYPE)
    product = app.config["DB_CONN"]["masmedi"]["products"].find_one({"product_id": body.get("product_id")})
    if not product:
        return Response(json.dumps({
            "status":False,
            "message":f"product is not available for this{body.get('product_id')}. Provide approprite product id "
        }), mimetype=MIME_TYPE)
    app.config["DB_CONN"]["masmedi"]["products"].update_one({"product_id": body.get("product_id")}, {"$set": body.get("update_details",{})})
    return Response(json.dumps({
        "status":True,
        "message": "product updated successfully"
    }), mimetype=MIME_TYPE)

@app.route("/delete_product/", methods=["GET"])
def delete_product():
    """Delete product
    This api is use to delete the existing product

    query params:
        - product_id(str): Unique id of the product

    Returns:
        Response:
            - status: successful or not
            - message: error message or successful message
            - product_id: Id of the created product
    """
    product_id = request.args.get("product_id","")
    app.config["DB_CONN"]["masmedi"]["products"].delete_one({"product_id": product_id})
    return Response(json.dumps({
        "status":True,
        "message": "product removed successfully"
    }), mimetype=MIME_TYPE)

@app.route("/place_order", methods=["POST"])
def place_order():
    """Place order
    This api is use to place the order for the available products

    request body:
        - product_id(str): unique id of the product
        - user_id(str): Unique id of the user

    Returns:
        Response:
            - status: successful or not
            - message: error message or successful message
    """
    body = request.get_json()
    if not body.get("user_id") or not body.get("product_id"):
        return Response(json.dumps({
            "status":False,
            "message":"Please provide valid data"
        }), mimetype=MIME_TYPE)
    if body.get("user_id"):
        user = app.config["DB_CONN"]["masmedi"]["users"].find_one({"user_id": body.get("user_id","")})
        if not user:
            return Response(json.dumps({
                "status":False,
                "message":"User not found for the menioned user id"
            }), mimetype=MIME_TYPE)
        if not user.get("user_purchase_list"):
            app.config["DB_CONN"]["masmedi"]["user"].update_one({"user_id": body.get("user_id")}, {"$set": {"user_purchase_list": []}})
    app.config["DB_CONN"]["masmedi"]["products"].update_one({"product_id": body.get("product_id","")},{"$set":{"is_sold": True}})
    app.config["DB_CONN"]["masmedi"]["users"].update_one({"user_id": body.get("user_id")}, {"$push": {"user_purchase_list": body.get("product_id")}})
    return Response(json.dumps({
        "status":True,
        "message": f"product sold successfully to this {user.get('user_name','')}"
    }), mimetype=MIME_TYPE)


if __name__=="__main__":
    app.run(debug=True)