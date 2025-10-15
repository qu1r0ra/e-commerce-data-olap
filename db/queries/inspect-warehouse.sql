-- Data to compare for Production Validation Testing (PVT)

SELECT      *
FROM        "DimProducts"
WHERE       "productCode" = <replace-with-sample>

SELECT      *
FROM        "DimRiders"
WHERE       "sourceId" = <replace-with-sample>

SELECT      *
FROM        "DimUsers"
WHERE       "productCode" = <replace-with-sample>

SELECT      *
FROM        "FactSales" fs
JOIN        "DimUsers" du ON fs."userId" = du."id"
JOIN        "DimDate" dd ON fs."deliveryDateId" = dd."id"
JOIN        "DimRiders" dr ON fs."deliveryRiderId" = dr."id"
JOIN        "DimProducts" dp ON fs."productId" = dp."id"
WHERE       fs."sourceId" = <replace-with-sample>
AND         dp."name" = <replace-with-sample>

--- Query to check duplicates for Duplicate Data Check Testing (DDCT)

SELECT      "sourceId", COUNT(*) duplicate_count
FROM        <replace-with-sample>
GROUP BY    <replace-with-sample>
HAVING      COUNT(*) > 1
