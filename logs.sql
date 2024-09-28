CREATE TABLE logs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    log_entry TEXT NOT NULL,
    log_type VARCHAR(50),
    log_user VARCHAR(50),
    log_date DATE,
    log_time TIME,
    priority VARCHAR(10),
    hostname VARCHAR(100),
    appname VARCHAR(100),
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
