from fastapi import HTTPException

from ..domain.cart import Cart
from ..domain.user import User
from ..service.product_service import ProductService
from ..service.user_service import UserService


class CartService:
    def __init__(self, user_service: UserService, product_service: ProductService, cart_for_users: dict):
        self.user_service = user_service
        self.product_service = product_service
        self.user_carts = cart_for_users

    def add_product_to_cart_for_user(self, user_id: str, product_id: str, outlet_id: str) -> dict:
        user = self.user_service.fetch_user_by_id(user_id)
        if user is None:
            raise HTTPException(status_code=404, detail=f"User '{user_id}' not found")

        cart = self.fetch_cart_for_user(user)
        if cart is None:
            raise HTTPException(status_code=404, detail=f"Cart not found for user '{user_id}'")

        product = self.product_service.get_product(product_id, outlet_id)
        if product is None:
            raise HTTPException(status_code=404, detail=f"Product '{product_id}' not found in outlet '{outlet_id}'")

        cart.products.append(product)
        return {"cart": cart.to_json(), "product": product.to_json(), "selling_price": product.selling_price}

    def get_cart_for_user(self, user_id: str) -> Cart:
        user = self.user_service.fetch_user_by_id(user_id)
        if user is None:
            raise HTTPException(status_code=404, detail=f"User '{user_id}' not found")

        cart = self.fetch_cart_for_user(user)
        if cart is None:
            raise HTTPException(status_code=404, detail=f"Cart not found for user '{user_id}'")

        return cart

    def fetch_cart_for_user(self, user: User) -> Cart | None:
        return self.user_carts.get(user.user_id)
