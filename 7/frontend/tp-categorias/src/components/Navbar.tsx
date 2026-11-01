type NavBarProps = {
    titulo: string
}

// Componente de presentación: no tiene estado propio. Recibe `count` por
// props y lo muestra. El estado vive en el padre (Counter) y los hijos
// reciben sólo los datos que necesitan para renderizar.
function Navbar({ titulo }: NavBarProps) {
  return (
    <nav className="bg-blue-600 px-6 py-4 text-white">
      <h1 className="text-xl font-bold">{titulo}</h1>
    </nav>
  )
}

export default Navbar
