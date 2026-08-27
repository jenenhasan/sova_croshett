# Sova Note

Sova Note is a backend API for a simple e-commerce style ordering flow: browse products, manage a session-based cart, and check out. Built with **Django** and **Django REST Framework**.

## Status

🚧 Work in progress. Core models, serializers, views, and routing are in place. Checkout order-creation logic (`CheckoutService`) is still being built.

## Features

- **Products** organized by category, with availability flags
- **Session-based cart** — no login required, cart is tied to the Django session
- **Cart items** with quantity management (add / update / remove), enforcing one entry per product per cart
- **Orders** with a status lifecycle (`pending → confirmed → completed / canceled`)
- **Checkout** endpoint that validates customer info before creating an order

## Tech Stack

- Python / Django
- Django REST Framework (DRF)
- postgresql

## Project Structure

```
sova_note/
├── models.py         # Category, Product, Cart, CartItem, Order, OrderItem
├── serializers.py     # DRF serializers for all models + CheckoutSerializer
├── views.py            # API views (products, cart, orders, checkout)
├── services.py        # CheckoutService — business logic for turning a cart into an order
└── urls.py              # URL routing for the API
```

## Data Model Overview

- `Category` → has many `Product`
- `Product` → belongs to a `Category`
- `Cart` → identified by `session_id`, has many `CartItem`
- `CartItem` → links a `Cart` to a `Product` with a `quantity`
- `Order` → customer info, status, total price, has many `OrderItem`
- `OrderItem` → links an `Order` to a `Product`, with quantity and a price snapshot

## API Endpoints

| Method | Endpoint                     | Description                          |
|--------|-------------------------------|---------------------------------------|
| GET    | `/products/`                  | List all available products           |
| GET    | `/products/<id>/`              | Get a single product                  |
| GET    | `/cart/`                       | Get the current session's cart        |
| POST   | `/cart/items/`                 | Add a product to the cart             |
| PATCH  | `/cart/items/<id>/`            | Update a cart item's quantity         |
| DELETE | `/cart/items/<id>/`            | Remove an item from the cart          |
| GET    | `/orders/<id>/`                 | Get a single order                    |
| POST   | `/checkout/`                   | Validate checkout info (order creation coming soon) |

## Getting Started

1. **Clone the repo**
   ```bash
   git clone https://github.com/jenenhasan/sova-crochet.git
   cd sova-note
   ```

2. **Create a virtual environment and install dependencies**
   ```bash
   python -m venv venv
   source venv/bin/activate  # on Windows: venv\Scripts\activate
   pip install django djangorestframework
   ```

3. **Run migrations**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

4. **Create a superuser (optional, for the admin panel)**
   ```bash
   python manage.py createsuperuser
   ```

5. **Run the development server**
   ```bash
   python manage.py runserver
   ```

The API will be available at `http://127.0.0.1:8000/`.

## Roadmap

- [ ] Implement `CheckoutService` to turn a validated cart + checkout data into an `Order` + `OrderItem`s
- [ ] Clear the cart after a successful checkout
- [ ] Add admin registration for models
- [ ] Add tests for cart and checkout flows
- [ ] Add authentication (optional, currently anonymous/session-based)

## License

Not yet decided.
