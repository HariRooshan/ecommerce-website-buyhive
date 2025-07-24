-- Create the products table with quantity
CREATE TABLE products (
    id INT PRIMARY KEY,
    name VARCHAR(255),
    brand VARCHAR(255),
    price DECIMAL(10, 2),
    image VARCHAR(255),
    quantity INT
);

-- Insert product records
INSERT INTO products (id, name, brand, price, image, quantity) VALUES
(1, 'iphone 15', 'Apple', 89999.00, 'phone.png', 10),
(2, 'Smart Watch Pro', 'Apple', 29999.00, 'watch.jpg', 25),
(3, 'Laptop Core i5', 'Dell', 79999.00, 'laptop.jpg', 6);