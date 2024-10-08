
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
--  you might want to watch the data base design again because this is my first design i am coming from non sql database
-- Users Table
CREATE TABLE Users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(255) NOT NULL,
    phone_number VARCHAR(15) NOT NULL UNIQUE,
    email VARCHAR(255) UNIQUE,
    address TEXT,
    membership_type_id UUID REFERENCES MembershipTypes(id),
    date_joined DATE NOT NULL DEFAULT CURRENT_DATE,
    is_active BOOLEAN NOT NULL DEFAULT TRUE
);

-- MembershipTypes Table
CREATE TABLE MembershipTypes (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    type_name VARCHAR(50) NOT NULL UNIQUE,
    benefits TEXT
);

-- Authors Table
CREATE TABLE Authors (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(255) NOT NULL,
    bio TEXT
);

-- Categories Table
CREATE TABLE Categories (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(100) NOT NULL UNIQUE,
    description TEXT
);

-- Books Table
CREATE TABLE Books (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    title VARCHAR(255) NOT NULL,
    author_id INT NOT NULL REFERENCES Authors(id),
    isbn VARCHAR(13) UNIQUE NOT NULL,
    count INT NOT NULL DEFAULT 1 CHECK (count >= 0),
    is_rentable BOOLEAN NOT NULL DEFAULT TRUE,
    publication_year YEAR,
    publisher VARCHAR(255),
    language VARCHAR(50)
);

-- Book_Categories Table
CREATE TABLE Book_Categories (
    book_id UUID REFERENCES Books(id) ON DELETE CASCADE,
    category_id UUID REFERENCES Categories(id) ON DELETE CASCADE,
    PRIMARY KEY (book_id, category_id)
);

-- Rent Table
CREATE TABLE Rent (
    id SERIAL PRIMARY KEY,
    user_id UUID NOT NULL REFERENCES Users(id),
    book_id UUID NOT NULL REFERENCES Books(id),
    rent_date DATE NOT NULL DEFAULT CURRENT_DATE,
    due_date DATE NOT NULL,
    return_date DATE,
    status VARCHAR(20) NOT NULL DEFAULT 'Rented' CHECK (status IN ('Rented', 'Returned', 'Overdue')),
    fine DECIMAL(5,2) DEFAULT 0.00
);

-- Optional: Book_Authors Table for Multiple Authors
CREATE TABLE Book_Authors (
    book_id UUID REFERENCES Books(id) ON DELETE CASCADE,
    author_id UUID REFERENCES Authors(id) ON DELETE CASCADE,
    PRIMARY KEY (book_id, author_id)
);

-- Optional: Book_Copies Table
CREATE TABLE Book_Copies (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    book_id UUID NOT NULL REFERENCES Books(id),
    status VARCHAR(20) NOT NULL DEFAULT 'Available' CHECK (status IN ('Available', 'Rented', 'Maintenance')),
    location VARCHAR(100)
);


CREATE TABLE orders (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES "user" (id) ON DELETE CASCADE,
    purchase_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    total_price DECIMAL(10, 2) NOT NULL
);

CREATE TABLE order_items (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    order_id UUID REFERENCES orders (id) ON DELETE CASCADE,
    book_id UUID REFERENCES book (id) ON DELETE CASCADE,
    quantity INT DEFAULT 1,
    price_per_item DECIMAL(10, 2) NOT NULL
);


--  create data base trigger for adding new items and check if the quantity is less then the items count in the books tabel
CREATE OR REPLACE FUNCTION check_and_update_book_quantity()
RETURNS TRIGGER AS $$
DECLARE
    available_quantity INTEGER;
BEGIN
    -- Get the available quantity of the book
    SELECT count INTO available_quantity
    FROM books
    WHERE id = NEW.book_id;

    -- Check if there is enough quantity to fulfill the order
    IF available_quantity < NEW.quantity THEN
        RAISE EXCEPTION 'Not enough quantity for book ID %: requested % but available %',
            NEW.book_id, NEW.quantity, available_quantity;
    END IF;

    -- Subtract the quantity from the books table
    UPDATE books
    SET count = count - NEW.quantity
    WHERE id = NEW.book_id;

    RETURN NEW;  -- Return the new row for insertion into order_items
END;
$$ LANGUAGE plpgsql;


--  init the trigger
CREATE TRIGGER before_order_item_insert
BEFORE INSERT ON order_items
FOR EACH ROW
EXECUTE FUNCTION check_and_update_book_quantity();


-- triggers
CREATE OR REPLACE FUNCTION update_rent_status()
RETURNS TRIGGER AS $$
BEGIN
    -- Update the status to 'Overdue' if the current date is greater than the due_date
    UPDATE Rent
    SET status = 'Overdue'
    WHERE due_date < CURRENT_DATE AND status = 'Rented';

    RETURN NULL;  -- No need to return anything from this trigger
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER check_due_date
AFTER INSERT OR UPDATE ON Rent
FOR EACH ROW
EXECUTE FUNCTION update_rent_status();




CREATE OR REPLACE FUNCTION decrement_book_count_on_rent()
RETURNS TRIGGER AS $$
BEGIN
    -- Check if the book is rentable
    IF (SELECT is_rentable FROM books WHERE id = NEW.book_id) IS FALSE THEN
        RAISE EXCEPTION 'Book ID % is not rentable', NEW.book_id;
    END IF;

    -- Check if there is enough quantity to fulfill the rent
    UPDATE books
    SET count = count - 1
    WHERE id = NEW.book_id AND count > 0;

    IF NOT FOUND THEN
        RAISE EXCEPTION 'Not enough quantity to rent book ID %', NEW.book_id;
    END IF;

    RETURN NEW;  -- Return the new row for insertion into Rent
END;
$$ LANGUAGE plpgsql;

-- Create trigger for rent operation
CREATE TRIGGER before_rent_insert
BEFORE INSERT ON Rent
FOR EACH ROW



EXECUTE FUNCTION decrement_book_count_on_rent();


CREATE OR REPLACE FUNCTION increment_book_count_on_return()
RETURNS TRIGGER AS $$
BEGIN
    -- Increment the book count when a book is returned
    UPDATE books
    SET count = count + 1
    WHERE id = NEW.book_id;

    RETURN NEW;  -- Return the new row for update in Rent
END;
$$ LANGUAGE plpgsql;

-- Create trigger for return operation
CREATE TRIGGER after_rent_update
AFTER UPDATE ON Rent
FOR EACH ROW
WHEN (NEW.return_date IS NOT NULL AND OLD.return_date IS NULL)
EXECUTE FUNCTION increment_book_count_on_return();