# U6 · Actividad 4 — Custom Hooks: useForm

Código de apoyo de la Actividad 4 de la Unidad 6 de Programación IV (React + TypeScript).
Implementa el custom hook `useForm` y su especialización para el dominio de categorías
(`useCategoriasForm`), usada desde un modal controlado.

## Qué muestra cada archivo

- `src/hooks/useForm.ts`: el hook genérico (`<T extends Record<string, unknown>>`), con
  `handleChange` (actualiza un campo por su atributo `name`, con spread operator; acepta
  inputs, textareas y selects), `resetForm` y `setFormValues`, que permite precargar datos
  desde afuera del hook.
- `src/components/ContactForm.tsx`: ejemplo básico de uso, un formulario de nombre y email que
  usa `useForm` directamente.
- `src/hooks/useCategoriasForm.ts`: especialización del hook genérico para categorías.
- `src/components/CategoriaModal.tsx`: modal controlado que usa `useCategoriasForm`. Recibe la
  categoría a editar (o `null` para crear una nueva) y sólo dispara callbacks, sin lógica de
  negocio propia.
- `src/App.tsx`: mantiene la lista de categorías en memoria, abre y cierra el modal y agrega
  categorías nuevas con id, `created_at` y `updated_at`.

## Cómo ejecutarlo

```bash
pnpm install
pnpm dev
```

Para verificar que compila: `pnpm build`.

## Nota: `type`, no `interface`

`useForm<T>` exige `T extends Record<string, unknown>`. Una `interface` con las mismas
propiedades que un `type` no cumple esa restricción (TypeScript no le asigna una firma de
índice), así que `useForm<MiInterface>(...)` no compila y da un error como este:

```
Type 'MiInterface' does not satisfy the constraint 'Record<string, unknown>'.
  Index signature for type 'string' is missing in type 'MiInterface'.
```

Por eso `src/types.ts` declara `ContactFormData` y `CategoriaFormData` con `type`. El hook
no cambia: lo que se ajusta es el tipo que se le pasa.
