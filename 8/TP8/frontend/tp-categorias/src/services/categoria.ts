// import CategoriaCard from "../components/CategoriaCard";
import type { Categoria } from "../types/categoria";

const API_URL = "http://127.0.0.1:8000/categorias";

export async function getCategorias(): Promise<Categoria[]> {
    const response = await fetch(`${API_URL}/?limit=50`);
    if (!response.ok) {
        throw new Error("Error al obtener las categorias");
    }
    return response.json();
}

export async function crearCategoria(data: { nombre: string; descripcion: string }): Promise <Categoria> {

    const response = await fetch(`${API_URL}/`,{
        method:'POST',
        headers:{'Content-Type':'application/json'},
        body:JSON.stringify(data),
    });

    if(!response.ok){
        throw new Error("Error al crear la categoria");
    }
    return response.json();
}

export async function actualizarCategoria(id:number, data: { nombre: string; descripcion: string }): Promise <Categoria> {

    const response = await fetch(`${API_URL}/${id}`,{
        method:'PUT',
        headers:{'Content-Type':'application/json'},
        body:JSON.stringify(data),
    });

    if(!response.ok){
        throw new Error("Error al actualizar la categoria");
    }
    return response.json();
}

export async function eliminarCategoria(id:number): Promise<void>{
    const response = await fetch(`${API_URL}/${id}`,{
        method:'DELETE'
    })
    if(!response.ok){
        throw new Error("Error al eliminar la categoria");
    }
}