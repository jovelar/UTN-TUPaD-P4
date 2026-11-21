import type { Producto } from "../types/producto";

const API_URL = "http://127.0.0.1:8000/productos";

export type ProductoData = Omit<Producto, "id">;

export async function getProductos(): Promise<Producto[]> {
    const response = await fetch(`${API_URL}/?limit=50`);
    if (!response.ok) {
        throw new Error("Error al obtener los productos");
    }
    return response.json();
}

export async function crearProducto(data: ProductoData): Promise<Producto> {
    const response = await fetch(`${API_URL}/`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data),
    });
    if (!response.ok) {
        throw new Error("Error al crear el producto");
    }
    return response.json();
}

export async function actualizarProducto(id: number, data: ProductoData): Promise<Producto> {
    const response = await fetch(`${API_URL}/${id}`, {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data),
    });
    if (!response.ok) {
        throw new Error("Error al actualizar el producto");
    }
    return response.json();
}

export async function eliminarProducto(id: number): Promise<void> {
    const response = await fetch(`${API_URL}/${id}`, {
        method: "DELETE",
    });
    if (!response.ok) {
        throw new Error("Error al eliminar el producto");
    }
}