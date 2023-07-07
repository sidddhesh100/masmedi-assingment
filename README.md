# masmedi-assingment


This documentation provides an overview of the APIs available in the MassMedia Organization system. These APIs allow you to manage products and place orders within the organization.

## Table of Contents

- [Create Product](#create-product)
- [Update Product](#update-product)
- [Place Order](#place-order)
- [Delete Order](#delete-order)

## Create Product

Creates a new product in the MassMedia Organization system.

### Request

- Method: POST
- Endpoint: `/create_product`
- Headers:
  - Content-Type: application/json
- Sample Body:

```json
{
  "product_name": "flipkar"
}
```

### Response

- Sample Body:

```json
{
  "status": true,
  "message": "Product created successfully",
  "product_id": "182a497d-8323-4cbd-a0f4-777a47c33c63"
}
```

## Update Product

Updates an existing product in the MassMedia Organization system.

### Request

- Method: POST
- Endpoint: `update_product`
- Headers:
  - Content-Type: application/json
- Sample Body:

```json
{
  "product_id": "93d827c4-c6bc-43a4-89e9-fc9517c20955",
  "update_details": {
    "product_type": "home"
  }
}
```

### Response

- Smaple Body:

```json
{
  "status": true,
  "message": "Product updated successfully"
}
```

## Place Order

Places an order in the MassMedia Organization system.

### Request

- Method: POST
- Endpoint: `/place_order`
- Headers:
  - Content-Type: application/json
- Sample Body:

```json
{
  "user_id": "eb4953ee-0521-4a20-9c77-3edb12c5a588",
  "product_id": "93d827c4-c6bc-43a4-89e9-fc9517c20955"
}
```

### Response

- Sample Body:

```json
{
  "status": true,
  "message": "Product sold successfully"
}
```

## Delete Order

Deletes an order from the MassMedia Organization system.

### Request

- Method: GET
- Endpoint: `/delete_order`
- Sample Query Parameters:
  - product_id: f574b03c-065b-45b3-bd89-77c7df3fdaf9

### Response

- Body:

```json
{
  "status": true,
  "message": "Product removed successfully"
}
```

That's it! You now have the information you need to interact with the MassMedia Organization APIs.