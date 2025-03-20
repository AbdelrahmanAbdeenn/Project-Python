# Library Management System

## **Abdelrahman Abdeen**

### **1. Overview**
The **Library Management System** is a structured and maintainable **RESTful API** developed using **Flask** and **PostgreSQL**. This system enables managing books and members within a library. The core functionalities include adding, updating, deleting, borrowing, and returning books while also managing member registrations.

---

### **2. Architecture & Design**
This system follows **Domain-Driven Design (DDD)** principles, which divide the application into four main layers:

---

### **2.1 Domain Layer**
**Folder:** `src/domain`

This layer contains the core business entities, representing the essential data objects used in the system:
- **`BaseEntity`**: A generic parent class for all entities.
- **`BookEntity`**: Defines attributes like `id`, `title`, `author`, `is_borrowed`, `borrowed_by`, and `borrowed_date`.
- **`MemberEntity`**: Defines attributes such as `id`, `name`, `email`, and `borrowed_books` (stores book details for borrowed books).

**Member-Book Relationship**
- Members and Books have a **join relationship**, allowing each **Member** to view the books they currently borrowed.
- This ensures **seamless retrieval of borrowed book data** when querying for a member.

---

### **2.2 Infrastructure Layer**
**Folder:** `src/infrastructure`

This layer handles **database interaction** through **SQLAlchemy** and includes repositories that provide an abstraction over direct database operations.

#### **Repositories:**
- **`BaseRepo`**: A generic repository providing CRUD operations (`get_all`, `get_by_id`, `add`, `update`, `delete`).
- **`BookRepo`**: A specific repository handling books.
- **`MemberRepo`**: A specific repository handling members.

**Dynamic Primary Key Handling**
- Different entities (Books & Members) have **different primary keys** (`id` for books is **auto-incremented**, while `id` for members is a **UUID**).
- Instead of duplicating repository logic, the **BaseRepo dynamically handles different entity primary keys**.

#### **Database Components:**
- **Unit of Work (UoW)**: Manages database transactions.
- **Schema Definitions**: Defines the database schema using **SQLAlchemy**.
- **Database Connection**: Establishes the connection to **PostgreSQL**.

This structure allows **efficient database access** while keeping the **domain logic separate from persistence concerns**.

---

### **2.3 Application Layer**
**Folder:** `src/application`

This layer contains **service classes** that handle the business logic and interact with repositories.

#### **Service Classes:**
- **`BaseServices`**: Handles generic CRUD operations for any entity type, ensuring code reusability.
- **`BookServices`**: Extends `BaseServices` to add **book-specific operations** like borrowing and returning books.
- **`MemberServices`**: Extends `BaseServices` to handle **member-related functionality**.

**Helper Functions:**
- **`_get_book_by_id()`**: Retrieves a book and raises an error if not found.
- **`_get_member_by_id()`**: Retrieves a member and raises an error if not found.
- **`_validate_creation()`**: Ensures an entity **doesn't already exist** before adding it.

By placing these **reusable functions** in the **application layer**, we keep the **services clean and well-structured**.

---

### **2.4 Presentation Layer**
**Folder:** `src/presentation`

This is the **entry point for API requests**, exposing **endpoints** that interact with the **Application Layer**.

#### **Key Responsibilities:**
Handling **API requests and responses**.
Validating **user input** before passing it to the business logic.
Converting **entities into JSON format**.
Managing **global error handling**.

#### **Implemented APIs:**
- **BookApi** : Handles CRUD operations for books.
- **MemberApi** : Handles CRUD operations for members.
- **BorrowApi** : Handles book borrowing.
- **ReturnApi** : Handles book returns.

**Member Entity and Borrowed Books**
- **Members can now see the books they have borrowed.**
- When retrieving a **member’s details**, the system **automatically includes a list of borrowed books**.
- This is achieved using **SQL joins**, eliminating the need for multiple queries.

#### **Global Error Handling**
**Folder:** `src/presentation/error_handling`

A **centralized error-handling mechanism** provides structured JSON responses across all endpoints. This prevents inconsistent error messages and **simplifies debugging**.

##### **Common Errors Handled:**
- **`ValueError`** → Raised when business logic conditions fail (e.g., borrowing an already borrowed book).
- **`IntegrityError`** → Raised when a **database constraint is violated** (e.g., duplicate entry).
- **`NotFound (404)` & `BadRequest (400)`** → Ensures clear API responses for invalid requests.
- **`Exception`** → Catches any unexpected errors to prevent system crashes.

---

### **3. Project Setup**
#### **Prerequisites**
Ensure you have **Python, PostgreSQL, and `pyenv` installed** on your system.

#### **Installation Steps**
```sh
# Clone the repository
git clone https://github.com/AbdelrahmanAbdeenn/Project-Python.git

# Navigate to the project directory
cd Project-Python

# Install dependencies
pip install -r requirements.txt
```

#### **Database Setup**
```sh
# Create the PostgreSQL database
CREATE DATABASE library_db;
```

#### **Apply Migrations**
```sh
alembic upgrade head
```

---
