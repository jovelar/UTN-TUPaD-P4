interface NavbarProps {
  titulo: string
}

export const Navbar = ({ titulo }: NavbarProps) => {
  return (
    <nav className="bg-blue-700 text-white">
      <div className="max-w-6xl mx-auto px-4 py-4">
        <h1 className="text-2xl font-bold">{titulo}</h1>
      </div>
    </nav>
  )
}