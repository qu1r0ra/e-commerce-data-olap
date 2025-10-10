-- Number of entries per table

SELECT 		COUNT(*)
FROM		Couriers;

SELECT 		COUNT(*)
FROM		OrderItems;

SELECT 		COUNT(*)
FROM		Orders;

SELECT 		COUNT(*)
FROM		Products;

SELECT 		COUNT(*)
FROM		Riders;

SELECT 		COUNT(*)
FROM		Users;


-- Data to compare for Production Validation Testing (PVT)

SELECT 		*
FROM 		Products
ORDER BY 	RAND()
LIMIT 		1;

SELECT 		*
FROM 		Riders r
JOIN        Couriers c ON r.courierId = c.id
ORDER BY 	RAND()
LIMIT 		1;

SELECT 		*
FROM 		Users
ORDER BY 	RAND()
LIMIT 		1;

SELECT		o.id, p.name, p.category, p.price, oi.quantity, c.name, r.firstName, r.lastName, r.vehicleType, u.firstName, u.lastName, u.dateOfBirth
FROM		Orders o
JOIN		Users u ON o.userId = u.id
JOIN		Riders r ON o.deliveryRiderId = r.id
JOIN		Couriers c ON r.courierId = c.id
JOIN		OrderItems oi ON oi.OrderId = o.id
JOIN		Products p ON oi.ProductId = p.id
ORDER BY	RAND()
LIMIT		3;


-- Entries per table

SELECT		*
FROM		Couriers;

SELECT		*
FROM		OrderItems;

SELECT		*
FROM		Orders;

SELECT		*
FROM		Products;

SELECT		*
FROM		Riders;

SELECT		*
FROM		Users;
