# U6 · Actividad 2 — useState y useEffect

Código de apoyo de la Actividad 2 de la Unidad 6 de Programación IV (React + TypeScript).
Muestra un contador dividido en tres componentes (`Counter`, `CounterDisplay` y
`CounterControls`) manejado con `useState`, y dos usos de `useEffect`: uno que reacciona a
los cambios de `count` y otro que registra el montaje y el desmontaje del componente, con su
función de limpieza.

## Qué muestra cada archivo

- `src/Counter.tsx`: el estado `count` (`useState`), un `useEffect` con `[count]` como
  dependencia y un `useEffect` con array vacío `[]` que imprime un mensaje al montar y
  devuelve una función de limpieza que se ejecuta al desmontar.
- `src/CounterDisplay.tsx`: componente hijo que sólo recibe `count` por props y lo muestra.
- `src/CounterControls.tsx`: botones de sumar y restar que actualizan el estado con la forma
  funcional `setCount(prev => prev + 1)`.
- `src/App.tsx`: un botón "Mostrar/Ocultar contador" que monta y desmonta `<Counter />`, para
  ver en la consola los mensajes de montaje y desmontaje.

## Cómo ejecutarlo

```bash
pnpm install
pnpm dev
```

Abrir la URL que muestra Vite (por defecto `http://localhost:5173`) y la consola del
navegador para ver los mensajes de los efectos. Para verificar que compila: `pnpm build`.

## Nota sobre StrictMode

El proyecto usa `<StrictMode>`, el valor por defecto de Vite. En desarrollo, React monta,
desmonta y vuelve a montar cada componente una vez para ayudar a detectar efectos mal
limpiados. Por eso los mensajes "Counter se montó" y "Counter se desmontó" pueden aparecer
duplicados la primera vez: es el comportamiento esperado en modo desarrollo, no un error.
