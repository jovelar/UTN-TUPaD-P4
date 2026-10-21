import { useEffect, useState } from 'react'
import CounterControls from './CounterControls'
import CounterDisplay from './CounterDisplay'

// Componente padre: el estado `count` vive acá y baja a los hijos por props
// (flujo de datos unidireccional).
function Counter() {
  const [count, setCount] = useState(0)

  // Efecto con dependencia: se ejecuta después de cada render en el que
  // cambió `count`.
  useEffect(() => {
    console.log('El contador cambió:', count)
  }, [count])

  // Efecto con array vacío: se ejecuta una sola vez, al montar el componente.
  // La función que devuelve (cleanup) se ejecuta al desmontarlo.
  useEffect(() => {
    console.log('Counter se montó')
    return () => {
      console.log('Counter se desmontó')
    }
  }, [])

  return (
    <div>
      <CounterDisplay count={count} />
      <CounterControls setCount={setCount} />
    </div>
  )
}

export default Counter
