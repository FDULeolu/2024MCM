from part import *

def buy_parts(ware_house, part: Part, N: int):
    batch = []
    for _ in range(N):
        batch.append(part.get_part())
    ware_house['part' + part.id] = batch
    return N * part.get_price()

def assemble_sf_parts(ware_house, sf_product: SF_Product):
    batch = []
    parts = [value for key, value in ware_house.items() if 'part' in key]
    assemble_number = min(len(row) for row in parts)
    for i in range(assemble_number):
        batch.append(sf_product.assemble([row[i] for row in parts]))
    ware_house['sf_product' + sf_product.id] = batch
    for part in parts:
        part[:] = part[assemble_number:]
    return assemble_number * sf_product.get_assemble_cost()

def assemble_product_from_parts(ware_house, product: Product):
    batch = []
    parts = ware_house['sf_product']
    assemble_number = min(len(row) for row in parts)
    for i in range(assemble_number):
        batch.append(product.assemble([row[i] for row in parts]))
    ware_house['product'].append(batch)
    for part in parts:
        part[:] = part[assemble_number:]
    return assemble_number * product.get_assemble_cost()

def assemble_product_from_sf_products(ware_house, product: Product):
    batch = []
    parts = ware_house['part']
    assemble_number = min(len(row) for row in parts)
    for i in range(assemble_number):
        batch.append(product.assemble([row[i] for row in parts]))
    ware_house['product'].append(batch)
    for part in parts:
        part[:] = part[assemble_number:]
    return assemble_number * product.get_assemble_cost()

def check(parts: list[list]):
    cost = 0
    not_qualified = []
    for row in parts:
        cost += len(row) * row[0].get_check_cost()
        not_qualified.append([part for part in row if not part.qualified])
        row[:] = [part for part in row if part.qualified]
    return not_qualified, cost

def disassemble(ware_house, not_qualified_product):
    cost = 0
    for row in not_qualified_product:
        cost += len(row) * row[0].get_disassemble_cost()
