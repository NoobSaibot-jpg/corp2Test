# Warehouse Management System / Система управління складом

## English

This project is a full-stack warehouse management system built with **Flask** (Python) for the backend and **React** for the frontend.

### Features
- Product and service catalog
- Customer management
- Goods receipts (purchases)
- Goods issues (sales)
- Invoices
- Stock balance and reports
- Print-ready documents (invoices, receipts, issues)
- Ukrainian language interface

### Project Structure
```
corp2Test/
  backend/    # Flask backend (API, models, migrations)
  frontend/   # React frontend (UI, forms, logic)
```

### Quick Start

#### 1. Backend (Flask)
- Go to the backend folder:
  ```sh
  cd backend
  ```
- Create and activate a virtual environment (optional but recommended):
  ```sh
  python -m venv venv
  venv\Scripts\activate  # On Windows
  source venv/bin/activate  # On Linux/Mac
  ```
- Install dependencies:
  ```sh
  pip install -r requirements.txt
  ```
- Initialize the database:
  ```sh
  python init_db.py
  python migrate_add_fields_2024_06.py
  ```
- Run the backend server:
  ```sh
  python run.py
  ```

#### 2. Frontend (React)
- Go to the frontend folder:
  ```sh
  cd ../frontend
  ```
- Install dependencies:
  ```sh
  npm install
  ```
- Start the development server:
  ```sh
  npm start
  ```
- The app will be available at [http://localhost:3000](http://localhost:3000)

#### 3. Usage
- Open the app in your browser.
- Use the navigation bar to manage products, customers, receipts, issues, invoices, and reports.
- Print documents directly from the edit dialog.

---

## Українською

Цей проєкт — повноцінна система управління складом на **Flask** (Python, бекенд) та **React** (фронтенд).

### Можливості
- Каталог товарів та послуг
- Управління контрагентами
- Прибуткові накладні (надходження)
- Видаткові накладні (продажі)
- Рахунки-фактури
- Залишки та звіти
- Друк документів (накладні, рахунки)
- Український інтерфейс

### Структура проєкту
```
corp2Test/
  backend/    # Flask бекенд (API, моделі, міграції)
  frontend/   # React фронтенд (UI, форми, логіка)
```

### Швидкий старт

#### 1. Бекенд (Flask)
- Перейдіть у папку backend:
  ```sh
  cd backend
  ```
- Створіть та активуйте віртуальне середовище (опційно):
  ```sh
  python -m venv venv
  venv\Scripts\activate  # Windows
  source venv/bin/activate  # Linux/Mac
  ```
- Встановіть залежності:
  ```sh
  pip install -r requirements.txt
  ```
- Ініціалізуйте базу даних:
  ```sh
  python init_db.py
  python migrate_add_fields_2024_06.py
  ```
- Запустіть сервер:
  ```sh
  python run.py
  ```

#### 2. Фронтенд (React)
- Перейдіть у папку frontend:
  ```sh
  cd ../frontend
  ```
- Встановіть залежності:
  ```sh
  npm install
  ```
- Запустіть фронтенд:
  ```sh
  npm start
  ```
- Додаток буде доступний за адресою [http://localhost:3000](http://localhost:3000)

#### 3. Використання
- Відкрийте додаток у браузері.
- Керуйте товарами, контрагентами, накладними, рахунками та звітами через меню.
- Друкуйте документи прямо з діалогу редагування.

---

**Author / Автор:**
- Timofii Manko / Тимофій Манько