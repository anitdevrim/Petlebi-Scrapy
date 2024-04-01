CREATE TABLE IF NOT EXISTS products(
    id INT PRIMARY KEY AUTO_INCREMENT,
    product_name VARCHAR(100) NOT NULL,
    product_id VARCHAR(15) NOT NULL,
    product_brand VARCHAR(50) NOT NULL,
    product_price DECIMAL(10,2) NOT NULL,
    product_stock VARCHAR(20) NOT NULL,
    product_category VARCHAR(150) NOT NULL,
    product_url VARCHAR(150) NOT NULL,
    product_image VARCHAR(150) NOT NULL,
    product_barcode VARCHAR(20) NOT NULL,
    product_description VARCHAR(500) NOT NULL,
    product_sku VARCHAR(20) NOT NULL
);