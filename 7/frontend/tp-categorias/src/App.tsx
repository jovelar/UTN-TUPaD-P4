
import { useEffect, useState } from 'react'
import Navbar from './components/Navbar'
import CategoriaList from './components/CategoriaList'
import CategoriaModal from './components/CategoriaModal'
import type { Categoria } from './types/categoria'

const API_URL = 'http://localhost:8000/categorias'

function App() {
  const [categorias, setCategorias] = useState<Categoria[]>([])
  const [modalAbierto, setModalAbierto] = useState(false)
  const [categoriaEditando, setCategoriaEditando] = useState<Categoria | null>(
    null,
  )

  const cargarCategorias = async () => {
    const response = await fetch(`${API_URL}/?limit=50`)
    const data: Categoria[] = await response.json()
    setCategorias(data)
  }

  useEffect(() => {
    cargarCategorias()
  }, [])

  const handleCreate = async (data: { nombre: string; descripcion: string }) => {
    await fetch(`${API_URL}/`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data),
    })
    await cargarCategorias()
  }

  const handleUpdate = async (
    id: number,
    data: { nombre: string; descripcion: string },
  ) => {
    await fetch(`${API_URL}/${id}`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data),
    })
    await cargarCategorias()
  }

  const handleDelete = async (id: number) => {
    await fetch(`${API_URL}/${id}`, { method: 'DELETE' })
    await cargarCategorias()
  }

  const abrirParaCrear = () => {
    setCategoriaEditando(null)
    setModalAbierto(true)
  }

  const abrirParaEditar = (categoria: Categoria) => {
    setCategoriaEditando(categoria)
    setModalAbierto(true)
  }

  const cerrarModal = () => {
    setModalAbierto(false)
    setCategoriaEditando(null)
  }

  const handleSubmit = async (data: { nombre: string; descripcion: string }) => {
    if (categoriaEditando) {
      await handleUpdate(categoriaEditando.id, data)
    } else {
      await handleCreate(data)
    }
    cerrarModal()
  }

  return (
    <div className="min-h-screen bg-gray-100">
      <Navbar titulo="Gestión de Categorías" />
      <main className="mx-auto max-w-5xl p-6">
        <button
          type="button"
          onClick={abrirParaCrear}
          className="mb-6 rounded bg-green-600 px-4 py-2 text-white"
        >
          Nueva categoría
        </button>
        <CategoriaList
          categorias={categorias}
          onEdit={abrirParaEditar}
          onDelete={handleDelete}
        />
      </main>
      {modalAbierto && (
        <CategoriaModal
          categoriaEditando={categoriaEditando}
          onSubmit={handleSubmit}
          onCancel={cerrarModal}
        />
      )}
    </div>
  )
}

export default App




// import { useState } from 'react'
// import heroImg from './assets/hero.png'
// import reactLogo from './assets/react.svg'
// import viteLogo from './assets/vite.svg'
// import './App.css'

// function App() {
//   const [count, setCount] = useState(0)

//   return (
//     <>
//       <section id="center">
//         <div className="hero">
//           <img src={heroImg} className="base" width="170" height="179" alt="" />
//           <img src={reactLogo} className="framework" alt="React logo" />
//           <img src={viteLogo} className="vite" alt="Vite logo" />
//         </div>
//         <div>
//           <h1 className="text-4xl font-bold text-red-500">Get started</h1>
//           <p>
//             Edit <code>src/App.tsx</code> and save to test <code>HMR</code>
//           </p>
//         </div>
//         <button
//           type="button"
//           className="counter"
//           onClick={() => setCount((count) => count + 1)}
//         >
//           Count is {count}
//         </button>
//       </section>

//       <div className="ticks"></div>

//       <section id="next-steps">
//         <div id="docs">
//           <svg className="icon" role="presentation" aria-hidden="true">
//             <use href="/icons.svg#documentation-icon"></use>
//           </svg>
//           <h2>Documentation</h2>
//           <p>Your questions, answered</p>
//           <ul>
//             <li>
//               <a href="https://vite.dev/" target="_blank">
//                 <img className="logo" src={viteLogo} alt="" />
//                 Explore Vite
//               </a>
//             </li>
//             <li>
//               <a href="https://react.dev/" target="_blank">
//                 <img className="button-icon" src={reactLogo} alt="" />
//                 Learn more
//               </a>
//             </li>
//           </ul>
//         </div>
//         <div id="social">
//           <svg className="icon" role="presentation" aria-hidden="true">
//             <use href="/icons.svg#social-icon"></use>
//           </svg>
//           <h2>Connect with us</h2>
//           <p>Join the Vite community</p>
//           <ul>
//             <li>
//               <a href="https://github.com/vitejs/vite" target="_blank">
//                 <svg
//                   className="button-icon"
//                   role="presentation"
//                   aria-hidden="true"
//                 >
//                   <use href="/icons.svg#github-icon"></use>
//                 </svg>
//                 GitHub
//               </a>
//             </li>
//             <li>
//               <a href="https://chat.vite.dev/" target="_blank">
//                 <svg
//                   className="button-icon"
//                   role="presentation"
//                   aria-hidden="true"
//                 >
//                   <use href="/icons.svg#discord-icon"></use>
//                 </svg>
//                 Discord
//               </a>
//             </li>
//             <li>
//               <a href="https://x.com/vite_js" target="_blank">
//                 <svg
//                   className="button-icon"
//                   role="presentation"
//                   aria-hidden="true"
//                 >
//                   <use href="/icons.svg#x-icon"></use>
//                 </svg>
//                 X.com
//               </a>
//             </li>
//             <li>
//               <a href="https://bsky.app/profile/vite.dev" target="_blank">
//                 <svg
//                   className="button-icon"
//                   role="presentation"
//                   aria-hidden="true"
//                 >
//                   <use href="/icons.svg#bluesky-icon"></use>
//                 </svg>
//                 Bluesky
//               </a>
//             </li>
//           </ul>
//         </div>
//       </section>

//       <div className="ticks"></div>
//       <section id="spacer"></section>
//     </>
//   )
// }

// export default App
