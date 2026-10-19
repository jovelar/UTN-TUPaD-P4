interface FooterProps {
  texto: string
}

export const Footer = ({ texto }: FooterProps) => {
  return (
    <footer className="bg-gray-800 text-gray-300">
      <div className="max-w-6xl mx-auto px-4 py-4 text-center text-sm">
        {texto}
      </div>
    </footer>
  )
}