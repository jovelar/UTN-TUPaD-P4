import { Link } from "react-router-dom"
type NavBarProps = {
    titulo: string
}

function Navbar({ titulo }: NavBarProps) {
  return (
    <nav className="bg-blue-600 px-6 py-4 text-white flex items-center gap-6">
      <h1 className="text-xl font-bold">{titulo}</h1>
      <Link to="/categorias">Categorias</Link>
      <Link to="/productos">Productos</Link>
      <Link to="/ingredientes">Ingredientes</Link>
    </nav>
  )
}

export default Navbar
