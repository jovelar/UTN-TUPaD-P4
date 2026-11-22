import { Link, useNavigate } from "react-router-dom"
import { useAuthStore } from "../store/authStore"

type NavBarProps = {
    titulo: string
}

function Navbar({ titulo }: NavBarProps) {
  const user = useAuthStore((s) => s.user)
  const logout = useAuthStore((s) => s.logout)
  const navigate = useNavigate()

  const cerrarSesion = async () => {
    await logout()
    navigate("/login")
  }

  return (
    <nav className="bg-blue-600 px-6 py-4 text-white flex items-center gap-6">
      <h1 className="text-xl font-bold">{titulo}</h1>
      {user && (
        <>
          <Link to="/categories">Categorías</Link>
          <Link to="/products">Productos</Link>
          {user.roles.includes("admin") && <Link to="/admin/users">Usuarios</Link>}
          <span className="ml-auto">
            {user.nombre} {user.apellido} ({user.roles.join(", ")})
          </span>
          <button
            type="button"
            onClick={cerrarSesion}
            className="rounded bg-white px-3 py-1 text-blue-600 hover:bg-gray-100"
          >
            Cerrar sesión
          </button>
        </>
      )}
    </nav>
  )
}

export default Navbar