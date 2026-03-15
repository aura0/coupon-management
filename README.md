
# Coupons Management API

### A Scalable, Extensible Discount Engine for E-Commerce

---

## 1. Project Overview

This project implements a **modular, extensible Coupon Management System** using:

* **Flask** (REST API)
* **SQLAlchemy** (ORM)
* **SQLite** (Database)
* **Strategy Pattern** (Coupon logic abstraction)
* **Service Layer Architecture**

The system is designed with **clean separation of concerns**, making it easy to scale, test, and extend.

---

## 2. System Architecture

### High-Level Architecture

```
Client (REST Client/Postman / Frontend)
        ↓
Flask Routes (Controller Layer)
        ↓
Service Layer (Business Logic)
        ↓
Coupon Engine (Strategy Dispatcher)
        ↓
Strategy Classes (Cart / Product / BxGy)
        ↓
Database (SQLite via SQLAlchemy)
```

---

### Layer Responsibilities

#### Routes Layer

* Handles HTTP requests
* Validates input
* Returns structured JSON responses
* Contains minimal business logic

#### Service Layer

* Contains core application logic
* Communicates with database models
* Calls Coupon Engine for calculations

#### Coupon Engine

* Implements **Strategy Pattern**
* Dynamically selects coupon logic based on coupon type
* Keeps system open for extension

#### Strategy Layer

Each coupon type has its own class:

* `CartWiseStrategy`
* `ProductWiseStrategy`
* `BxGyStrategy`

This ensures:

* No large conditional blocks
* Clean separation
* Easy addition of new coupon types

#### Database Layer

* Uses SQLAlchemy ORM
* Stores coupon type and JSON-based details
* Flexible schema design

---

## 3. Design Decisions (Senior-Level Explanation)

### 1. Strategy Pattern Used

Instead of using multiple `if-else` statements for coupon types,
we implemented the **Strategy Pattern**.

**Why?**

* Makes system extensible
* New coupon types can be added without modifying existing logic
* Follows Open/Closed Principle (SOLID)

---

### 2. Service Layer Architecture

Business logic is separated from routes.

**Benefits:**

* Cleaner controllers
* Easier unit testing
* Better maintainability
* Follows industry best practices

---

### 3. JSON-Based Coupon Details

Instead of fixed database columns, coupon rules are stored in a flexible `details` JSON field.

**Why?**

* Supports different coupon structures
* Avoids schema changes for new coupon types
* Highly scalable design

---

### 4. Modular Project Structure

Code is organized into:

* routes/
* services/
* strategies/
* models/

This improves:

* Readability
* Maintainability
* Team collaboration
* Scalability

---

### 5. Extensibility Focus

The system is designed so that:

To add a new coupon type:

1. Create new strategy class
2. Register it in CouponEngine
3. No changes needed in routes

This makes the system future-proof.

---

## 4. Implemented Features

### Coupon Types Supported

####  Cart-wise

* Applies discount on total cart value
* Threshold-based logic
* Percentage discount
```json
{
  "type": "cart-wise",
  "details": {
    "threshold": 100,
    "discount": 10
  }
}

####  Product-wise

* Applies discount to specific product
* Only if product exists in cart

```json
{
  "type": "product-wise",
  "details": {
    "product_id": 1,
    "discount": 20
  }
}
####  BxGy

* Buy X products
* Get Y products free
* Supports repetition limit
* Handles quantity calculations correctly
```json
{
  "type": "bxgy",
  "details": {
    "buy_products": [
      { "product_id": 1, "quantity": 2 }
    ],
    "get_products": [
      { "product_id": 3, "quantity": 1 }
    ],
    "repition_limit": 2
  }
}
---

### API Endpoints

2. **API Endpoints**

   - `POST /coupons` → Create new coupon
   - `GET /coupons` → Retrieve all coupons
   - `GET /coupons/{id}` → Retrieve coupon by ID
   - `PUT /coupons/{id}` → Update coupon
   - `DELETE /coupons/{id}` → Delete coupon
   - `POST /applicable-coupons` → List all applicable coupons for a cart
   - `POST /apply-coupon/{id}` → Apply a specific coupon to a cart
   - `GET /ping` → Health check
---

## 5. What Is NOT Covered

The following features are intentionally not implemented:

###  Coupon Expiration

No expiry date handling.

###  Usage Limits

No tracking of number of times a coupon is used.

### User-Based Coupons

Coupons are global.

### Coupon Stacking

Only one coupon can be applied at a time.

###  Automatic Best Coupon Selection

System does not automatically select the maximum discount coupon.

###  Advanced Product Validation

No external product catalog integration.

###  Authentication / Authorization

No login or role-based access control.

---

## 6. Assumptions

* Only one coupon applied per cart
* Product IDs are valid
* Prices are positive values
* Quantities are positive integers
* Discounts cannot exceed item price
* Cart input format is correct

---

## 7. Testing Strategy

### Unit Testing

* Uses `pytest`
* Tests service layer logic
* Tests coupon calculation
* Tests edge cases

### What Is Tested

* Cart-wise discount calculation
* Product-wise discount calculation
* BxGy repetition logic
* Applicable coupon filtering
* Error scenarios
* Invalid inputs

### Why Testing Is Important

* Ensures business logic correctness
* Prevents regression issues
* Validates edge cases
* Improves reliability

---

## 8. How to Run Tests

```bash
pytest
```

---

## 9. How to Run the Project

Install dependencies:

```bash
pip install -r requirements.txt
```

Run application:

```bash
python run.py
```

Server runs at:

```
http://127.0.0.1:5000
```

---

## 10. Future Enhancements

* Coupon expiration system
* Usage tracking
* User-specific coupons
* Coupon stacking
* Best-coupon auto selection engine
* Category-based coupons
* Redis caching
* Logging system
* Dockerization
* CI/CD pipeline
* Advanced integration tests

---

## 11. Conclusion

This project demonstrates:

* Clean architecture design
* Strategy-based extensible system
* Separation of concerns
* Scalable coupon engine
* Proper documentation of limitations
* Production-ready structural thinking
