from sqlalchemy import Integer, Float, Boolean, DateTime, ForeignKey, Text, DECIMAL, CheckConstraint, Column, MetaData, String, Table, select
from sqlalchemy.orm import Mapped, mapped_column, relationship, declarative_base
from sqlalchemy.sql import func


Base = declarative_base()


class Product(Base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    price = Column(DECIMAL(10, 2), nullable=False)
    product_type = Column(String(50), nullable=False)
    current_quantity = Column(Integer, nullable=False, default=0)
    for_baby = Column(Boolean, nullable=False)
    size = Column(String(50))
    color = Column(String(50))
    line = Column(String(50))
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    # Relationships
    product_images = relationship("ProductImage", back_populates="product", cascade="all, delete-orphan")
    images = relationship("Image", secondary="product_images", back_populates="products", overlaps="product_images")
    inventory_history = relationship("InventoryHistory", back_populates="product", cascade="all, delete-orphan")
    cart_items = relationship("CartItem", back_populates="product", cascade="all, delete-orphan")
    sale_items = relationship("SaleItem", back_populates="product")
    reviews = relationship("Review", back_populates="product", cascade="all, delete-orphan")

class Image(Base):
    __tablename__ = 'images'

    id = Column(Integer, primary_key=True, autoincrement=True)
    small_url = Column(String(255), nullable=False)
    medium_url = Column(String(255), nullable=False)
    large_url = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=func.now())

    # Relationships
    product_images = relationship("ProductImage", back_populates="image", cascade="all, delete-orphan")
    products = relationship("Product", secondary="product_images", back_populates="images", overlaps="product_images")

class ProductImage(Base):
    __tablename__ = 'product_images'

    product_id = Column(Integer, ForeignKey('products.id', ondelete='CASCADE'), primary_key=True)
    image_id = Column(Integer, ForeignKey('images.id', ondelete='CASCADE'), primary_key=True)

    # Relationships
    product = relationship("Product", back_populates="product_images", overlaps="images,products")
    image = relationship("Image", back_populates="product_images", overlaps="images,products")

class InventoryHistory(Base):
    __tablename__ = 'inventory_history'

    id = Column(Integer, primary_key=True, autoincrement=True)
    product_id = Column(Integer, ForeignKey('products.id', ondelete='CASCADE'), nullable=False)
    previous_quantity = Column(Integer, nullable=False)
    quantity_change = Column(Integer, nullable=False)
    new_quantity = Column(Integer, nullable=False)
    movement_type = Column(String(20), nullable=False)
    reference_number = Column(String(50))
    sale_id = Column(Integer, ForeignKey('sales.id', ondelete='SET NULL'))
    notes = Column(Text)
    created_at = Column(DateTime, default=func.now())

    # Relationships
    product = relationship("Product", back_populates="inventory_history")
    sale = relationship("Sale", back_populates="inventory_history")

class Client(Base):
    __tablename__ = 'clients'

    id = Column(Integer, primary_key=True, autoincrement=True)
    is_admin = Column(Boolean, nullable=False, default=False)
    email = Column(String(255), nullable=False, unique=True)
    password_hash = Column(String(255), nullable=False)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    date_joined = Column(DateTime, default=func.now())
    is_afiliado = Column(Boolean, nullable=False, default=False)

    # Relationships
    addresses = relationship("Address", back_populates="client", cascade="all, delete-orphan")
    afiliado = relationship("Afiliado", back_populates="client", uselist=False, cascade="all, delete-orphan")
    cart_items = relationship("CartItem", back_populates="client", cascade="all, delete-orphan")
    sales = relationship("Sale", back_populates="client")
    returns = relationship("Return", back_populates="client")
    reviews = relationship("Review", back_populates="client", cascade="all, delete-orphan")

class Address(Base):
    __tablename__ = 'addresses'

    id = Column(Integer, primary_key=True, autoincrement=True)
    client_id = Column(Integer, ForeignKey('clients.id', ondelete='CASCADE'), nullable=False)
    street_address = Column(String(255), nullable=False)
    city = Column(String(100), nullable=False)
    state = Column(String(100), nullable=False)
    postal_code = Column(String(20), nullable=False)
    country = Column(String(100), nullable=False)
    is_default = Column(Boolean, nullable=False, default=False)
    created_at = Column(DateTime, default=func.now())

    # Relationships
    client = relationship("Client", back_populates="addresses")
    sales = relationship("Sale", back_populates="shipping_address")

class Afiliado(Base):
    __tablename__ = 'afiliados'

    client_id = Column(Integer, ForeignKey('clients.id', ondelete='CASCADE'), primary_key=True)
    cell_phone = Column(String(20), nullable=False)

    # Relationships
    client = relationship("Client", back_populates="afiliado")

class CartItem(Base):
    __tablename__ = 'cart_items'

    id = Column(Integer, primary_key=True, autoincrement=True)
    client_id = Column(Integer, ForeignKey('clients.id', ondelete='CASCADE'), nullable=False)
    product_id = Column(Integer, ForeignKey('products.id', ondelete='CASCADE'), nullable=False)
    quantity = Column(Integer, nullable=False, default=1)
    added_at = Column(DateTime, default=func.now())

    # Relationships
    client = relationship("Client", back_populates="cart_items")
    product = relationship("Product", back_populates="cart_items")

class Sale(Base):
    __tablename__ = 'sales'

    id = Column(Integer, primary_key=True, autoincrement=True)
    client_id = Column(Integer, ForeignKey('clients.id', ondelete='RESTRICT'), nullable=False)
    shipping_address_id = Column(Integer, ForeignKey('addresses.id', ondelete='RESTRICT'), nullable=False)
    total_amount = Column(DECIMAL(10, 2), nullable=False)
    payment_method = Column(String(50), nullable=False)
    payment_status = Column(String(20), nullable=False, default='pending')
    shipping_status = Column(String(20), nullable=False, default='pending')
    tracking_number = Column(String(50))
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    # Relationships
    client = relationship("Client", back_populates="sales")
    shipping_address = relationship("Address", back_populates="sales")
    sale_items = relationship("SaleItem", back_populates="sale", cascade="all, delete-orphan")
    returns = relationship("Return", back_populates="sale")
    inventory_history = relationship("InventoryHistory", back_populates="sale")

class SaleItem(Base):
    __tablename__ = 'sale_items'

    id = Column(Integer, primary_key=True, autoincrement=True)
    sale_id = Column(Integer, ForeignKey('sales.id', ondelete='CASCADE'), nullable=False)
    product_id = Column(Integer, ForeignKey('products.id', ondelete='RESTRICT'), nullable=False)
    quantity = Column(Integer, nullable=False)
    unit_price = Column(DECIMAL(10, 2), nullable=False)
    total_price = Column(DECIMAL(10, 2), nullable=False)

    # Relationships
    sale = relationship("Sale", back_populates="sale_items")
    product = relationship("Product", back_populates="sale_items")
    return_items = relationship("ReturnItem", back_populates="sale_item")

class Return(Base):
    __tablename__ = 'returns'

    id = Column(Integer, primary_key=True, autoincrement=True)
    sale_id = Column(Integer, ForeignKey('sales.id', ondelete='RESTRICT'), nullable=False)
    client_id = Column(Integer, ForeignKey('clients.id', ondelete='RESTRICT'), nullable=False)
    return_reason = Column(String(255), nullable=False)
    return_status = Column(String(20), nullable=False, default='pending')
    refund_amount = Column(DECIMAL(10, 2), nullable=False)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    # Relationships
    sale = relationship("Sale", back_populates="returns")
    client = relationship("Client", back_populates="returns")
    return_items = relationship("ReturnItem", back_populates="return_record", cascade="all, delete-orphan")

class ReturnItem(Base):
    __tablename__ = 'return_items'

    id = Column(Integer, primary_key=True, autoincrement=True)
    return_id = Column(Integer, ForeignKey('returns.id', ondelete='CASCADE'), nullable=False)
    sale_item_id = Column(Integer, ForeignKey('sale_items.id', ondelete='RESTRICT'), nullable=False)
    quantity = Column(Integer, nullable=False)
    unit_price = Column(DECIMAL(10, 2), nullable=False)
    total_price = Column(DECIMAL(10, 2), nullable=False)

    # Relationships
    return_record = relationship("Return", back_populates="return_items")
    sale_item = relationship("SaleItem", back_populates="return_items")

class Discount(Base):
    __tablename__ = 'discounts'

    id = Column(Integer, primary_key=True, autoincrement=True)
    code = Column(String(50), unique=True)
    description = Column(Text)
    discount_type = Column(String(20), nullable=False)
    discount_value = Column(DECIMAL(10, 2), nullable=False)
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=False)
    min_purchase_amount = Column(DECIMAL(10, 2))
    max_discount_amount = Column(DECIMAL(10, 2))
    is_active = Column(Boolean, nullable=False, default=True)
    created_at = Column(DateTime, default=func.now())

class Review(Base):
    __tablename__ = 'reviews'

    id = Column(Integer, primary_key=True, autoincrement=True)
    product_id = Column(Integer, ForeignKey('products.id', ondelete='CASCADE'), nullable=False)
    client_id = Column(Integer, ForeignKey('clients.id', ondelete='CASCADE'), nullable=False)
    rating = Column(Integer, nullable=False)
    comment = Column(Text)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    # Add check constraint for rating
    __table_args__ = (
        CheckConstraint('rating >= 1 AND rating <= 5', name='check_rating_range'),
    )

    # Relationships
    product = relationship("Product", back_populates="reviews")
    client = relationship("Client", back_populates="reviews")
