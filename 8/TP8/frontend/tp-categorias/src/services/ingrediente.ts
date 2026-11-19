import type { Ingrediente } from "../types/ingredientes";

const API_URL = "http://127.0.0.1:8000/ingredientes";

export type IngredienteData = Omit<Ingrediente, "id">;

export async function getIngredientes(): Promise<Ingrediente[]> {
    const response = await fetch(`${API_URL}/?limit=100`);
    if (!response.ok) {
        throw new Error("Error al obtener los ingredientes");
    }
    return response.json();
}

export async function crearIngrediente(data: IngredienteData): Promise<Ingrediente> {
    const response = await fetch(`${API_URL}/`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data),
    });
    if (!response.ok) {
        throw new Error("Error al crear el ingrediente");
    }
    return response.json();
}

export async function actualizarIngrediente(id: number, data: IngredienteData): Promise<Ingrediente> {
    const response = await fetch(`${API_URL}/${id}`, {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data),
    });
    if (!response.ok) {
        throw new Error("Error al actualizar el ingrediente");
    }
    return response.json();
}

export async function eliminarIngrediente(id: number): Promise<void> {
    const response = await fetch(`${API_URL}/${id}`, {
        method: "DELETE",
    });
    if (!response.ok) {
        throw new Error("Error al eliminar el ingrediente");
    }
}