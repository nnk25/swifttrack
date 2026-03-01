# SwiftTrack — Logistics Microservices Platform

## Quickstart

```bash
docker compose up --build
```

## Services & Ports

| Service              | Port  | Description                          |
|----------------------|-------|--------------------------------------|
| auth-service         | 8000  | User registration & JWT login        |
| order-service        | 8001  | Order management & status tracking   |
| notification-service | 8003  | WebSocket real-time notifications    |
| ros-mock             | 8010  | Mock Route Optimization REST API     |
| RabbitMQ Management  | 15672 | RabbitMQ admin UI (guest/guest)      |

## API Usage

### 1. Register a CLIENT user
```
POST http://localhost:8000/auth/register
{
  "username": "alice",
  "email": "alice@example.com",
  "password": "secret",
  "role": "CLIENT"
}
```

### 2. Login
```
POST http://localhost:8000/auth/login
{
  "username": "alice",
  "password": "secret"
}
```
Copy the `access_token` from the response.

### 3. Create an Order
```
POST http://localhost:8001/api/v1/orders
Authorization: Bearer <token>
{
  "description": "Electronics shipment",
  "destination": "123 Main St"
}
```

### 4. Check Order Status
```
GET http://localhost:8001/api/v1/orders/{order_id}
Authorization: Bearer <token>
```

### 5. Connect to WebSocket for real-time updates
```
ws://localhost:8003/ws/notifications
```

## Event Flow

```
order.created
    → cms-adapter  → cms.confirmed
    → wms-adapter  → wms.registered
                        → ros-adapter → ros.route_assigned
                                           → notification-service (WebSocket push)
```

## Saga Compensation

If an order_id ends with `999`, the CMS adapter simulates a failure.
The order transitions to `FAILED` and an `order.compensate` event is published.
The WMS adapter rolls back the warehouse registration.

## DRIVER Workflow

Register a DRIVER user, login, then:
```
POST http://localhost:8001/api/v1/drivers/{driver_id}/deliveries/{order_id}/complete
Authorization: Bearer <driver_token>
```
