CREATE TABLE products (
    id INTEGER AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    price DECIMAL(10,2) NOT NULL,
    product_type VARCHAR(50) NOT NULL,
    current_quantity INTEGER NOT NULL DEFAULT 0,
    for_baby BOOLEAN NOT NULL,
    size VARCHAR(50),
    color VARCHAR(50),
    line VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_product_type (product_type)
);

CREATE TABLE images (
    id INTEGER AUTO_INCREMENT PRIMARY KEY,
    product_id INTEGER NOT NULL,
    small_url VARCHAR(255) NOT NULL,
    medium_url VARCHAR(255) NOT NULL,
    large_url VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE,
    INDEX idx_product_id (product_id)
);

CREATE TABLE inventory_history (
    id INTEGER AUTO_INCREMENT PRIMARY KEY,
    product_id INTEGER NOT NULL,
    previous_quantity INTEGER NOT NULL,
    quantity_change INTEGER NOT NULL,
    new_quantity INTEGER NOT NULL,
    movement_type VARCHAR(20) NOT NULL, -- 'shipment', 'sale', 'return', 'adjustment'
    reference_number VARCHAR(50),
    sale_id INTEGER, -- Reference to sale if this is a sale movement
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE,
    FOREIGN KEY (sale_id) REFERENCES sales(id) ON DELETE SET NULL,
    INDEX idx_product_history (product_id, created_at)
);

CREATE TABLE clients (
    id INTEGER AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(255) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    date_joined TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_afiliado BOOLEAN NOT NULL DEFAULT FALSE,
    INDEX idx_email (email)
);

CREATE TABLE addresses (
    id INTEGER AUTO_INCREMENT PRIMARY KEY,
    client_id INTEGER NOT NULL,
    street_address VARCHAR(255) NOT NULL,
    city VARCHAR(100) NOT NULL,
    state VARCHAR(100) NOT NULL,
    postal_code VARCHAR(20) NOT NULL,
    country VARCHAR(100) NOT NULL,
    is_default BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (client_id) REFERENCES clients(id) ON DELETE CASCADE
);

CREATE TABLE afiliados (
    client_id INTEGER PRIMARY KEY,
    cell_phone VARCHAR(20) NOT NULL,
    FOREIGN KEY (client_id) REFERENCES clients(id) ON DELETE CASCADE
);

CREATE TABLE cart_items (
    id INTEGER AUTO_INCREMENT PRIMARY KEY,
    client_id INTEGER NOT NULL,
    product_id INTEGER NOT NULL,
    quantity INTEGER NOT NULL DEFAULT 1,
    added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (client_id) REFERENCES clients(id) ON DELETE CASCADE,
    FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE,
    INDEX idx_cart_items (client_id, product_id)
);

CREATE TABLE sales (
    id INTEGER AUTO_INCREMENT PRIMARY KEY,
    client_id INTEGER NOT NULL,
    shipping_address_id INTEGER NOT NULL,
    total_amount DECIMAL(10,2) NOT NULL,
    payment_method VARCHAR(50) NOT NULL,
    payment_status VARCHAR(20) NOT NULL DEFAULT 'pending', -- 'pending', 'completed', 'failed', 'refunded'
    shipping_status VARCHAR(20) NOT NULL DEFAULT 'pending', -- 'pending', 'shipped', 'delivered', 'returned'
    tracking_number VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (client_id) REFERENCES clients(id) ON DELETE RESTRICT,
    FOREIGN KEY (shipping_address_id) REFERENCES addresses(id) ON DELETE RESTRICT,
    INDEX idx_client_sales (client_id),
    INDEX idx_sale_status (payment_status, shipping_status)
);

CREATE TABLE sale_items (
    id INTEGER AUTO_INCREMENT PRIMARY KEY,
    sale_id INTEGER NOT NULL,
    product_id INTEGER NOT NULL,
    quantity INTEGER NOT NULL,
    unit_price DECIMAL(10,2) NOT NULL,
    total_price DECIMAL(10,2) NOT NULL,
    FOREIGN KEY (sale_id) REFERENCES sales(id) ON DELETE CASCADE,
    FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE RESTRICT,
    INDEX idx_sale_items (sale_id)
);

CREATE TABLE returns (
    id INTEGER AUTO_INCREMENT PRIMARY KEY,
    sale_id INTEGER NOT NULL,
    client_id INTEGER NOT NULL,
    return_reason VARCHAR(255) NOT NULL,
    return_status VARCHAR(20) NOT NULL DEFAULT 'pending', -- 'pending', 'approved', 'rejected', 'completed'
    refund_amount DECIMAL(10,2) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (sale_id) REFERENCES sales(id) ON DELETE RESTRICT,
    FOREIGN KEY (client_id) REFERENCES clients(id) ON DELETE RESTRICT,
    INDEX idx_return_status (return_status)
);

CREATE TABLE return_items (
    id INTEGER AUTO_INCREMENT PRIMARY KEY,
    return_id INTEGER NOT NULL,
    sale_item_id INTEGER NOT NULL,
    quantity INTEGER NOT NULL,
    unit_price DECIMAL(10,2) NOT NULL,
    total_price DECIMAL(10,2) NOT NULL,
    FOREIGN KEY (return_id) REFERENCES returns(id) ON DELETE CASCADE,
    FOREIGN KEY (sale_item_id) REFERENCES sale_items(id) ON DELETE RESTRICT,
    INDEX idx_return_items (return_id)
);

CREATE TABLE discounts (
    id INTEGER AUTO_INCREMENT PRIMARY KEY,
    code VARCHAR(50) UNIQUE,
    description TEXT,
    discount_type VARCHAR(20) NOT NULL, -- 'percentage', 'fixed_amount'
    discount_value DECIMAL(10,2) NOT NULL,
    start_date TIMESTAMP NOT NULL,
    end_date TIMESTAMP NOT NULL,
    min_purchase_amount DECIMAL(10,2),
    max_discount_amount DECIMAL(10,2),
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_discount_code (code),
    INDEX idx_discount_dates (start_date, end_date)
);

CREATE TABLE reviews (
    id INTEGER AUTO_INCREMENT PRIMARY KEY,
    product_id INTEGER NOT NULL,
    client_id INTEGER NOT NULL,
    rating INTEGER NOT NULL CHECK (rating BETWEEN 1 AND 5),
    comment TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE,
    FOREIGN KEY (client_id) REFERENCES clients(id) ON DELETE CASCADE,
    INDEX idx_product_reviews (product_id),
    INDEX idx_client_reviews (client_id)
);

DELIMITER //

CREATE TRIGGER after_inventory_change
AFTER INSERT ON inventory_history
FOR EACH ROW
BEGIN
    UPDATE products 
    SET current_quantity = NEW.new_quantity
    WHERE id = NEW.product_id;
END//

CREATE TRIGGER after_sale_item_insert
AFTER INSERT ON sale_items
FOR EACH ROW
BEGIN
    INSERT INTO inventory_history (
        product_id,
        previous_quantity,
        quantity_change,
        new_quantity,
        movement_type,
        sale_id
    )
    SELECT 
        NEW.product_id,
        p.current_quantity,
        -NEW.quantity,
        p.current_quantity - NEW.quantity,
        'sale',
        CONCAT('SALE-', NEW.sale_id)
    FROM products p
    WHERE p.id = NEW.product_id;
END//

-- Trigger to handle returns
CREATE TRIGGER after_return_item_insert
AFTER INSERT ON return_items
FOR EACH ROW
BEGIN
    INSERT INTO inventory_history (
        product_id,
        previous_quantity,
        quantity_change,
        new_quantity,
        movement_type,
        reference_number
    )
    SELECT 
        si.product_id,
        p.current_quantity,
        NEW.quantity,
        p.current_quantity + NEW.quantity,
        'return',
        CONCAT('RETURN-', NEW.return_id)
    FROM sale_items si
    JOIN products p ON si.product_id = p.id
    WHERE si.id = NEW.sale_item_id;
END//

DELIMITER ;
