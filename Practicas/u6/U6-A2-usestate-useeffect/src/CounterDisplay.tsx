type CounterDisplayProps = {
  count: number
}

// Componente de presentación: no tiene estado propio. Recibe `count` por
// props y lo muestra. El estado vive en el padre (Counter) y los hijos
// reciben sólo los datos que necesitan para renderizar.
function CounterDisplay({ count }: CounterDisplayProps) {
  return <h2>Contador: {count}</h2>
}

export default CounterDisplay
