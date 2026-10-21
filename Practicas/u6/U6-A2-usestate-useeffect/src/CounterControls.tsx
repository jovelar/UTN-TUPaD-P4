import type { Dispatch, SetStateAction } from 'react'

type CounterControlsProps = {
  setCount: Dispatch<SetStateAction<number>>
}

// Botones para sumar y restar. Recibe `setCount` por props desde el padre.
// Usa la forma funcional `prev => prev + 1` porque el valor nuevo depende del
// anterior: así React siempre parte del estado más reciente.
function CounterControls({ setCount }: CounterControlsProps) {
  const incrementar = () => setCount((prev) => prev + 1)
  const decrementar = () => setCount((prev) => prev - 1)

  return (
    <div>
      <button type="button" onClick={decrementar}>
        -
      </button>
      <button type="button" onClick={incrementar}>
        +
      </button>
    </div>
  )
}

export default CounterControls
