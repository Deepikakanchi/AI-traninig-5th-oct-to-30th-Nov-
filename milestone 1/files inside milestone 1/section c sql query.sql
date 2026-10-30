--C1. Display all parts belonging to the Mechanical category.

SELECT * FROM parts 
WHERE category='Mechanical';

--C2. Display parts with unit_price above 1000, ordered from highest price to lowest.
SELECT * FROM parts
WHERE unit_price>1000
ORDER BY unit_price DESC;

--C3. Find the average unit_price for each category.
SELECT category,AVG(unit_price) AS avgunitprice
FROM parts
GROUP BY category;

--C4. Find the total stock quantity for each category.
SELECT category,SUM(stock_qty) AS totalstock
FROM parts
GROUP BY category;

--C5. Display every purchase order with supplier_name, order_date and status using a JOIN.

SELECT 
purchase_orders.po_id,
suppliers.supplier_name,
purchase_orders.order_date,
purchase_orders.status
FROM purchase_orders
JOIN suppliers ON purchase_orders.supplier_id=suppliers.supplier_id;

--C6. Join purchase_orders, purchase_order_items and parts to display po_id, part_name, quantity and
--unit_price.
SELECT
po.po_id, 
p.part_name,
poi.quantity,
p.unit_price
FROM purchase_orders po
JOIN purchase_order_items poi ON po.po_id=poi.po_id
JOIN parts p ON  poi.part_id=p.part_id;


--C7. Extend the previous query to calculate line_total = quantity × unit_price.
SELECT
po.po_id, 
p.part_name,
poi.quantity,
p.unit_price,
poi.quantity *p.unit_price AS line_total
FROM purchase_orders po
JOIN purchase_order_items poi ON po.po_id=poi.po_id
JOIN parts p ON  poi.part_id=p.part_id;


--C8. Use a LEFT JOIN to display all suppliers, including suppliers that have never received a purchase order.
SELECT suppliers.supplier_name,po.po_id
FROM suppliers 
LEFT JOIN purchase_orders po on suppliers.supplier_id=po.supplier_id;


--C9. Display only suppliers that have no purchase orders.
SELECT suppliers.supplier_name
FROM suppliers 
LEFT JOIN purchase_orders po on suppliers.supplier_id=po.supplier_id
WHERE po.po_id IS NULL;

--C10. Create a view named purchase_order_summary showing po_id, supplier_name, part_name, quantity,
--unit_price, line_total and status. Query the view for Pending orders.
CREATE VIEW purchase_order_summary AS  
SELECT
po.po_id, 
s.supplier_name,
p.part_name,
poi.quantity,
p.unit_price,
poi.quantity *p.unit_price AS line_total,
po.status
FROM purchase_orders po
JOIN suppliers s ON po.supplier_id=s.supplier_id
JOIN purchase_order_items poi ON po.po_id=poi.po_id
JOIN parts p ON  poi.part_id=p.part_id;


SELECT *FROM  purchase_order_summary WHERE status='Pending';

--C11. Create a function calculate_part_discount(amount): if amount >= 2000 return 10% of amount, otherwise
--return 0. Use it with the parts table.
CREATE FUNCTION  calculate_part_discount(amount NUMERIC)
RETURNS NUMERIC
AS $$
BEGIN
	IF amount>= 2000 THEN
		 RETURN 0.1*amount;
	ELSE
		RETURN 0;
	END IF;
	
END;
$$ LANGUAGE plpgsql;

SELECT part_name,unit_price,calculate_part_discount(unit_price) AS discount
FROM parts;


--C12. Create a function final_part_price(amount) that returns amount minus calculate_part_discount(amount).
--Use it in a SELECT query.

CREATE FUNCTION final_part_price(amount NUMERIC)
RETURNS NUMERIC AS 
$$
BEGIN 
	RETURN amount-calculate_part_discount(amount);
END;
$$ LANGUAGE plpgsql;

SELECT part_name,unit_price,final_part_price(unit_price) AS final_price 
FROM parts;


--C13. Create a stored procedure with parameters named update_po_status that accepts po_id and new_status
--and updates the matching purchase order. Call it once and verify the result.

CREATE OR REPLACE PROCEDURE update_po_status(p_po_id INT,p_new_status VARCHAR)
AS $$
BEGIN
	UPDATE purchase_orders
	SET status=p_new_status
	WHERE po_id=p_po_id;
	COMMIT;
END;
$$  LANGUAGE plpgsql;

CALL update_po_status(1,'Shipped');

SELECT *FROM purchase_orders WHERE po_id=1;



--C14. Create a stored procedure without parameters named mark_old_pending_orders that changes Pending
--orders dated before 2026-10-04 to Received. Run it and verify the results.

CREATE OR REPLACE PROCEDURE mark_old_pending_orders()
AS $$
BEGIN
	UPDATE purchase_orders
	SET status='Received'
	WHERE status='Pending' AND order_date<'2026-10-04';
	COMMIT;
END;
$$  LANGUAGE plpgsql;

CALL mark_old_pending_orders();

SELECT *FROM purchase_orders WHERE status='Received';





