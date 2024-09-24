WITH duplicates AS (
    SELECT id, 
           tg,
           ROW_NUMBER() OVER (PARTITION BY tg ORDER BY id) AS row_num
    FROM member
)
DELETE FROM member
WHERE id IN (
    SELECT id
    FROM duplicates
    WHERE row_num > 1
);