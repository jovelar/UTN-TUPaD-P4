from typing import List, Optional
from .schemas import ProveedorCreate, ProveedorRead
from fastapi import HTTPException, status

# Simulamos que la BD guarda objetos tipo ProductoRead (con ID asignado)
db_proveedores: List[ProveedorRead] = []
id_counter = 1


def crear(data: ProveedorCreate) -> ProveedorRead:
    global id_counter
    codigo_existente(data.codigo)
    nuevo = ProveedorRead(id=id_counter, **data.model_dump())
    db_proveedores.append(nuevo)
    id_counter += 1
    return nuevo


def obtener_todos(skip: int, limit: int,activo:Optional[bool]) -> List[ProveedorRead]:
    activos=[]
    for prov in db_proveedores:
        if activo is None or prov.activo==activo:
            activos.append(prov)
    return activos[skip:skip+limit]


def obtener_por_id(id: int) -> Optional[ProveedorRead]:
    for p in db_proveedores:
        if p.id == id:
            return p
    return None


def actualizar_total(id: int, data: ProveedorCreate) -> Optional[ProveedorRead]:
    for index, p in enumerate(db_proveedores):
        if p.id == id:
            if data.codigo != p.codigo and codigo_existente(data.codigo):
                raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Ya existe otro proveedor con ese código")
            proveedor_actualizado = ProveedorRead(id=id, **data.model_dump())
            db_proveedores[index] = proveedor_actualizado
            return proveedor_actualizado
    return None


def desactivar(id: int) -> Optional[ProveedorRead]:
    for index, p in enumerate(db_proveedores):
        if p.id == id:
            if not p.activo:
                raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="El proveedor ya está dado de baja")
            p_dict = p.model_dump()
            p_dict["activo"] = False
            proveedor_actualizado = ProveedorRead(**p_dict)
            db_proveedores[index] = proveedor_actualizado
            return proveedor_actualizado
    return None




# def obtener_estado_stock(id: int) -> Optional[dict]:
#     proveedor = obtener_por_id(id)
#     if not proveedor:
#         return None

#     # La lógica de negocio vive aquí
#     alerta_stock = proveedor.stock < proveedor.stock_minimo

#     return {
#         "stock": proveedor.stock,
#         "bajo_stock_minimo": alerta_stock,
#         "activo": proveedor.activo,
#     }

def codigo_existente(codigo:str )->bool:
    encontrado:bool=False
    for prov in db_proveedores:
        if prov.codigo==codigo:
            encontrado=True
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="El codigo de proveedor ya existe")
    return encontrado