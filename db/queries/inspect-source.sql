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


-- Random rows to compare to the data warehouse

SELECT *
FROM YourTableName
ORDER BY RAND()
LIMIT 5;


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
