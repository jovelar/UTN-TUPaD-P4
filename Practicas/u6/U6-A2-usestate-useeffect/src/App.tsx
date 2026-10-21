import { useState } from 'react'
import Counter from './Counter'

// Estado `mostrar` + renderizado condicional: el botón monta y desmonta
// <Counter />. Sirve para ver en la consola del navegador cuándo se ejecuta
// el efecto de montaje y cuándo su función de limpieza.
function App() {
  const [mostrar, setMostrar] = useState(true)

  return (
    <main>
      <h1>useState + useEffect</h1>
      <p>
        Abrir la consola del navegador: ahí se ven los mensajes de{' '}
        <code>useEffect</code> (cambios de <code>count</code>, montaje y
        desmontaje de <code>Counter</code>).
      </p>
      <button type="button" onClick={() => setMostrar((prev) => !prev)}>
        {mostrar ? 'Ocultar contador' : 'Mostrar contador'}
      </button>
      {mostrar && <Counter />}
    </main>
  )
}

export default App
