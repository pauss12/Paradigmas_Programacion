import time
import asyncio

async def cocinar_carne(tipo_carne):
    print(f"Cocinando la carne de {tipo_carne}")
    await asyncio.sleep(3)
    print(f"Carne de {tipo_carne} cocinada")

async def preparar_extra(extra):
    print(f"Extra de {extra} preparado")
    await asyncio.sleep(1)

# Funcion que prepara una hamburguesa
async def process_order(order):
    await cocinar_carne(order["carne"])
    await preparar_extra(order["extra"])
    print(f"\nLa hamburguesa de {order['carne']} con {order['extra']} esta lista\n")

async def generate_orders():

    orders = [
        {"carne": "vaca", "extra": "lechuga"},
        {"carne": "pollo", "extra": "mozarella"},
        {"carne": "vegana", "extra": "tomate"}
    ]

    tasks = []
    for order in orders:
        task = asyncio.create_task(process_order(order))
        tasks.append(task)
    
    await asyncio.gather(*tasks)
   

async def main():

    await generate_orders()

asyncio.run(main())