-- Таблица клиентов
CREATE TABLE customer (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    address TEXT,
    phone TEXT
);

-- Таблица товаров и услуг
CREATE TABLE product (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    type TEXT NOT NULL, -- 'product' или 'service'
    unit TEXT,
    price REAL
);

-- Заказы
CREATE TABLE "order" (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date DATE NOT NULL,
    customer_id INTEGER NOT NULL,
    status TEXT,
    FOREIGN KEY (customer_id) REFERENCES customer(id)
);

-- Позиции заказа
CREATE TABLE order_item (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    order_id INTEGER NOT NULL,
    product_id INTEGER NOT NULL,
    quantity REAL NOT NULL,
    price REAL,
    FOREIGN KEY (order_id) REFERENCES "order"(id),
    FOREIGN KEY (product_id) REFERENCES product(id)
);

-- Счета-фактуры
CREATE TABLE invoice (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    order_id INTEGER NOT NULL,
    date DATE NOT NULL,
    total REAL,
    FOREIGN KEY (order_id) REFERENCES "order"(id)
);

-- Приходные накладные
CREATE TABLE goods_receipt (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date DATE NOT NULL,
    number TEXT,
    supplier_id INTEGER,
    FOREIGN KEY (supplier_id) REFERENCES customer(id)
);

CREATE TABLE goods_receipt_item (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    goods_receipt_id INTEGER NOT NULL,
    product_id INTEGER NOT NULL,
    quantity REAL NOT NULL,
    price REAL,
    FOREIGN KEY (goods_receipt_id) REFERENCES goods_receipt(id),
    FOREIGN KEY (product_id) REFERENCES product(id)
);

-- Расходные накладные
CREATE TABLE goods_issue (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date DATE NOT NULL,
    number TEXT,
    customer_id INTEGER,
    FOREIGN KEY (customer_id) REFERENCES customer(id)
);

CREATE TABLE goods_issue_item (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    goods_issue_id INTEGER NOT NULL,
    product_id INTEGER NOT NULL,
    quantity REAL NOT NULL,
    price REAL,
    FOREIGN KEY (goods_issue_id) REFERENCES goods_issue(id),
    FOREIGN KEY (product_id) REFERENCES product(id)
);

-- Налоговые накладные
CREATE TABLE tax_invoice (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    goods_issue_id INTEGER NOT NULL,
    date DATE NOT NULL,
    number TEXT,
    FOREIGN KEY (goods_issue_id) REFERENCES goods_issue(id)
);

-- Партии товара для FIFO
CREATE TABLE stock_batch (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_id INTEGER NOT NULL,
    quantity REAL NOT NULL,
    received_date DATE NOT NULL,
    cost REAL NOT NULL,
    FOREIGN KEY (product_id) REFERENCES product(id)
); 