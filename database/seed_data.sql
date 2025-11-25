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
('Demo User', 'demo@example.com', 'scrypt:32768:8:1$Qjq63pZIw3NRDp63$34d7a4b6f9867a23cdc1a02c296c46f33ee4e06cd9f9b1fc2f5447e28b70ab09c3c305d86befcbf5781c0d5c644a423c58aac4837d5c10b49794be478ed2b5d3');


INSERT INTO wallet (user_id, balance) VALUES (1, 5000);


INSERT INTO transactions (user_id, amount, category_id, merchant, type, date) VALUES
(1, 250, 1, 'McDonalds', 'expense', datetime('now', '-2 days')),
(1, 1200, 2, 'Uber', 'expense', datetime('now', '-1 days')),
(1, 5000, 7, 'Company XYZ', 'income', datetime('now', '-5 days'));
