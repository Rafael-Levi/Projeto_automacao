from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy import text
from database import get_data_db
from sqlalchemy.orm import Session
import pandas as pd
router = APIRouter()

#Qual foi o total de receitas no ano de 1997
@router.get("/total_receitas_ano/" )
async def analysis_query(db: Session = Depends(get_data_db)):
    try:
            result = db.execute(text("""
                                    SELECT SUM(order_details.unit_price * order_details.quantity * (1.0 - order_details.discount)) AS total_revenues_1997
                                    FROM order_details
                                    INNER JOIN (
                                        SELECT order_id 
                                        FROM orders 
                                        WHERE strftime('%Y', order_date) = '1997'
                                    ) AS ord 
                                    ON ord.order_id = order_details.order_id;

                                     """))
            
            df = pd.DataFrame(result.fetchall(), columns=result.keys())
            print(df)
           
            return {"status": "success", "data": df.to_dict(orient="records")}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao executar consulta de análise: {str(e)}")

#Valor total que cada cliente já pagou até agora
@router.get("/valor_pago_por_cliente/" )
async def analysis_query(db: Session = Depends(get_data_db)):
    try:
            result = db.execute(text("""
                    SELECT 
                        customers.company_name, 
                        SUM(order_details.unit_price * order_details.quantity * (1.0 - order_details.discount)) AS total
                    FROM 
                        customers
                    INNER JOIN 
                        orders ON customers.customer_id = orders.customer_id
                    INNER JOIN 
                        order_details ON order_details.order_id = orders.order_id
                    GROUP BY 
                        customers.company_name
                    ORDER BY 
                        total DESC;
                                     """))
            
            df = pd.DataFrame(result.fetchall(), columns=result.keys())
            print(df)
           
            return {"status": "success", "data": df.to_dict(orient="records")}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao executar consulta de análise: {str(e)}")

#Separando os clientes em 5 grupos de acordo com o valor pago por cliente
@router.get("/valor_pago_por_cliente_agrupado/" )
async def analysis_query(db: Session = Depends(get_data_db)):
    try:
            result = db.execute(text("""
                    WITH OrderedCustomers AS (
                    SELECT 
                        customers.company_name, 
                        SUM(order_details.unit_price * order_details.quantity * (1.0 - order_details.discount)) AS total
                    FROM 
                        customers
                    INNER JOIN 
                        orders ON customers.customer_id = orders.customer_id
                    INNER JOIN 
                        order_details ON order_details.order_id = orders.order_id
                    GROUP BY 
                        customers.company_name
                    ORDER BY 
                        total DESC
                ),
                RankedCustomers AS (
                    SELECT 
                        company_name,
                        total,
                        ROW_NUMBER() OVER (ORDER BY total DESC) AS row_number,
                        (SELECT COUNT(*) FROM OrderedCustomers) AS total_rows
                    FROM 
                        OrderedCustomers
                )
                SELECT 
                    company_name,
                    total,
                    CAST((row_number * 5.0) / total_rows AS INTEGER) AS group_number
                FROM 
                    RankedCustomers
                ORDER BY 
                    total DESC;

                                     """))
            
            df = pd.DataFrame(result.fetchall(), columns=result.keys())
            print(df)
           
            return {"status": "success", "data": df.to_dict(orient="records")}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao executar consulta de análise: {str(e)}")

#Identifica os 10 produtos mais vendidos
@router.get("/Produtos_mais_vendidos/" )
async def analysis_query(db: Session = Depends(get_data_db)):
    try:
            result = db.execute(text("""
                    SELECT products.product_name, SUM(order_details.unit_price * order_details.quantity * (1.0 - order_details.discount)) AS sales
                    FROM products
                    INNER JOIN order_details ON order_details.product_id = products.product_id
                    GROUP BY products.product_name
                    ORDER BY sales DESC
                    LIMIT 10;
                                     """))
            
            df = pd.DataFrame(result.fetchall(), columns=result.keys())
            print(df)
           
            return {"status": "success", "data": df.to_dict(orient="records")}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao executar consulta de análise: {str(e)}")

#Quais clientes do Reino Unido pagaram mais de 1000 dólares
@router.get("/clientes_do_Reino_Unido_pagaram_mais_de_1000_dólares/" )
async def analysis_query(db: Session = Depends(get_data_db)):
    try:
            result = db.execute(text("""
                SELECT customers.contact_name, SUM(order_details.unit_price * order_details.quantity * (1.0 - order_details.discount) * 100) / 100 AS payments
                FROM customers
                INNER JOIN orders ON orders.customer_id = customers.customer_id
                INNER JOIN order_details ON order_details.order_id = orders.order_id
                WHERE LOWER(customers.country) = 'uk'
                GROUP BY customers.contact_name
                HAVING SUM(order_details.unit_price * order_details.quantity * (1.0 - order_details.discount)) > 1000;
                                     """))
            
            df = pd.DataFrame(result.fetchall(), columns=result.keys())
            print(df)
           
            return {"status": "success", "data": df.to_dict(orient="records")}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao executar consulta de análise: {str(e)}")