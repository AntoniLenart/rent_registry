CREATE TABLE rentals (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    device_id TEXT NOT NULL,
    email TEXT NOT NULL,
    rental_date DATE NOT NULL,
    return_date DATE NOT NULL,
    device_type TEXT NOT NULL
);

CREATE TABLE history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    device_id TEXT NOT NULL,
    email TEXT NOT NULL,
    rental_date DATE NOT NULL,
    return_date DATE NOT NULL,
    device_type TEXT NOT NULL
);

ALTER TABLE history ADD COLUMN return_date_real TEXT;

