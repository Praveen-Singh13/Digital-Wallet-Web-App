INSERT INTO categories (name, type, user_id) VALUES
('Food', 'expense', NULL),
('Travel', 'expense', NULL),
('Shopping', 'expense', NULL),
('Bills', 'expense', NULL),
('Health', 'expense', NULL),
('Education', 'expense', NULL),
('Salary', 'income', NULL),
('Freelance', 'income', NULL),
('Investments', 'income', NULL);


INSERT INTO users (name, email, password) VALUES
('Demo User', 'demo@example.com', '$pbkdf2-sha256$29000$ZnptpFQJfV0uQp8I4.$M8cFHWlW8X94C1RJCYlnVSrRpltnB2IV/YIiYw8pNiU');


INSERT INTO wallet (user_id, balance) VALUES (1, 5000);


INSERT INTO transactions (user_id, amount, category_id, merchant, type, date) VALUES
(1, 250, 1, 'McDonalds', 'expense', datetime('now', '-2 days')),
(1, 1200, 2, 'Uber', 'expense', datetime('now', '-1 days')),
(1, 5000, 7, 'Company XYZ', 'income', datetime('now', '-5 days'));
