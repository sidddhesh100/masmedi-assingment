from flask import Blueprint, Response, request
from datetime import datetime
from app import current_app

import uuid

product = Blueprint("product", __name__, url_prefix="/product/")

@product.route("create_product/", methods=["POST"])
def create_product():
    request_body = request.get_data()
    """request_body params
    product name 
    is_available
    is_sell
    """
    request_body["product_id"] = uuid.uuid4()
    request_body["create_date"] = datetime.now()
    current_app["DB_CONN"]["masmedi"]["products"].insert(request_body)
    return Response({
        "status":True,
        "message": "product created successfully"
    })

@product.route("update_product/", method=["POST"])
def update_product():
    """
    request body
    product_id
    update_details

    """
    body = request.get_data()
    if not body.get("product_id"):
        return Response({
            "status":False,
            "message":"Please provide product Id"
        })
    current_app["DB_CONN"]["masmedi"]["products"].update({"product_id": body.get("product_id")}, {"$set": body.get("update_details",{})})
    return Response({
        "status":True,
        "message": "product update successfully"
    })
    
@product.route("delete_product/", method=["GET"])
def update_product():
    product_id = request.query_string.get("product_id","")
    current_app["DB_CONN"]["masmedi"]["products"].delete({"product_id": product_id})
    return Response({
        "status":True,
        "message": "product removed successfully"
    })
    
    
@product.route("place_order")
def place_order():
    """
    user_id
    product_id
    
    user structure
    user_id
    user_name
    user_purchase_list
    """
    body = request.get_data()
    if not body.get("user_id") or body.get("product_id"):
        return Response({
            "status":False,
            "message":"Please provide valid data"
        })
    if body.get("user_id"):
        user = current_app["CB_CONN"]["masmedi"]["user"].find_one({"user_id": body.get("user_id","")})
        if not user:
            return Response({
                "status":False,
                "message":"User not found for the menioned id"
            })
    
    current_app["DB_CONN"]["masmedi"]["products"].update({"product_id": body.get("product_id","")},{"$set":{"is_sell": "SOLD"}})
    current_app["DB_CONN"]["masmedi"]["user"].update({"user_id": body.get("user_id")}, {"$push": {"user_purchase_list": body.get("product_id")}})
    return Response({
        "status":True,
        "message": f"product sold successfully to this {user.get('user_name','')}"
    })