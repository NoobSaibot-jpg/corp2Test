import sqlite3

conn = sqlite3.connect('instance/app.db')
c = conn.cursor()

# Добавление новых полей в customer
for sql in [
    "ALTER TABLE customer ADD COLUMN type TEXT;",
    "ALTER TABLE customer ADD COLUMN email TEXT;",
    "ALTER TABLE customer ADD COLUMN ipn TEXT;",
    "ALTER TABLE customer ADD COLUMN bank_name TEXT;",
    "ALTER TABLE customer ADD COLUMN bank_account TEXT;",
    "ALTER TABLE customer ADD COLUMN mfo TEXT;",
    "ALTER TABLE customer ADD COLUMN contact_person TEXT;",
    "ALTER TABLE customer ADD COLUMN contact_phone TEXT;",
    "ALTER TABLE customer ADD COLUMN contact_email TEXT;",
    "ALTER TABLE customer ADD COLUMN discount REAL;",
    "ALTER TABLE customer ADD COLUMN credit_limit REAL;",
    "ALTER TABLE customer ADD COLUMN payment_terms TEXT;",
    "ALTER TABLE customer ADD COLUMN notes TEXT;",
    "ALTER TABLE customer ADD COLUMN country TEXT;",
    "ALTER TABLE customer ADD COLUMN city TEXT;",
    "ALTER TABLE customer ADD COLUMN postal_code TEXT;",
    "ALTER TABLE customer ADD COLUMN website TEXT;",
    "ALTER TABLE customer ADD COLUMN tax_system TEXT;",
    "ALTER TABLE customer ADD COLUMN vat_payer BOOLEAN;",
    "ALTER TABLE customer ADD COLUMN vat_certificate TEXT;"
]:
    try:
        c.execute(sql)
    except Exception:
        pass

# Добавление новых полей в product
for sql in [
    "ALTER TABLE product ADD COLUMN description TEXT;",
    "ALTER TABLE product ADD COLUMN barcode TEXT;",
    "ALTER TABLE product ADD COLUMN weight REAL;",
    "ALTER TABLE product ADD COLUMN volume REAL;",
    "ALTER TABLE product ADD COLUMN manufacturer TEXT;",
    "ALTER TABLE product ADD COLUMN country TEXT;",
    "ALTER TABLE product ADD COLUMN 'group' TEXT;",
    "ALTER TABLE product ADD COLUMN subgroup TEXT;",
    "ALTER TABLE product ADD COLUMN vat_rate INTEGER;",
    "ALTER TABLE product ADD COLUMN min_stock REAL;",
    "ALTER TABLE product ADD COLUMN max_stock REAL;",
    "ALTER TABLE product ADD COLUMN supplier TEXT;",
    "ALTER TABLE product ADD COLUMN supplier_price REAL;",
    "ALTER TABLE product ADD COLUMN notes TEXT;"
]:
    try:
        c.execute(sql)
    except Exception:
        pass

# Добавление новых полей в goods_receipt
for sql in [
    "ALTER TABLE goods_receipt ADD COLUMN contract TEXT;",
    "ALTER TABLE goods_receipt ADD COLUMN warehouse TEXT;",
    "ALTER TABLE goods_receipt ADD COLUMN organization TEXT;",
    "ALTER TABLE goods_receipt ADD COLUMN operation_type TEXT;",
    "ALTER TABLE goods_receipt ADD COLUMN responsible TEXT;",
    "ALTER TABLE goods_receipt ADD COLUMN comment TEXT;",
    "ALTER TABLE goods_receipt ADD COLUMN pricing_note TEXT;"
]:
    try:
        c.execute(sql)
    except Exception:
        pass

# Добавление новых полей в goods_issue
for sql in [
    "ALTER TABLE goods_issue ADD COLUMN contract TEXT;",
    "ALTER TABLE goods_issue ADD COLUMN warehouse TEXT;",
    "ALTER TABLE goods_issue ADD COLUMN organization TEXT;",
    "ALTER TABLE goods_issue ADD COLUMN operation_type TEXT;",
    "ALTER TABLE goods_issue ADD COLUMN responsible TEXT;",
    "ALTER TABLE goods_issue ADD COLUMN comment TEXT;",
    "ALTER TABLE goods_issue ADD COLUMN pricing_note TEXT;"
]:
    try:
        c.execute(sql)
    except Exception:
        pass

conn.commit()
conn.close()
print('Migration complete!') 