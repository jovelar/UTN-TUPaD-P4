import { Navbar } from './components/Navbar'
import { ProductoList } from './components/ProductoList'
import { ProductoForm } from './components/ProductoForm'
import { Footer } from './components/Footer'
import type { Producto } from './types/producto'

const productos: Producto[] = [
  { id: 1, nombre: 'Silla Ergonómica', descripcion: 'Silla ergonómica con apoyabrazos', precio: 250000 },
  { id: 2, nombre: 'Escritorio', descripcion: 'Escritorio de madera', precio: 180000 },
  { id: 3, nombre: 'Lámpara de Escritorio', descripcion: 'Lámpara LED para oficina', precio: 45000 },
]

export const App = () => {
  return (
    <div className="min-h-screen flex flex-col bg-gray-100">
      <Navbar titulo="Gestor de Productos" />
      <main className="flex-1 w-full max-w-6xl mx-auto px-4 py-8 grid grid-cols-1 lg:grid-cols-3 gap-8">
        <section className="lg:col-span-2 flex flex-col gap-4">
          <h2 className="text-2xl font-bold text-gray-900">Productos</h2>
          <ProductoList productos={productos} />
        </section>
        <aside>
          <ProductoForm titulo="Nuevo producto" />
        </aside>
      </main>
      <Footer texto="TP5" />
    </div>
  )
}