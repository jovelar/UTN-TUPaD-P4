# Pruebas de Productos con Postman

Postman sirve para el punto **c) del TP**: *"Agregar al archivo .zip los json de prueba"*. Una colección exportada de Postman es un archivo `.json` (RN-11: *".json de Postman o .http de REST Client"*).

Postman **no abre** archivos `.http`, así que las pruebas se cargan a mano, una por una. Los datos los copiás de `tests/test_api.http`.

## 1. Crear la colección (una sola vez)
1. Abrí Postman.
2. En el panel izquierdo, **Collections**, hacé clic en **`+`** (o **New → Collection**).
3. Ponele de nombre `TP5 - Productos`.

## 2. Cargar una prueba: ejemplo con la prueba 6 (Crear Producto)
1. Clic derecho en la colección `TP5 - Productos` y elegí **Add request**.
2. Arriba a la izquierda, donde dice `New Request`, ponele el nombre: `6. Crear Producto`.
3. En el desplegable de la izquierda, que dice `GET`, elegí **POST**.
4. En la barra de URL escribí: `http://127.0.0.1:8000/productos/`
5. Debajo de la URL, hacé clic en la pestaña **Body**, elegí **raw** y, en el desplegable de la derecha que dice `Text`, elegí **JSON**.
6. En el cuadro de texto pegá **las líneas 46 a 54** de `tests/test_api.http` (desde `{` hasta `}`).
7. Hacé clic en **Send**, el botón azul a la derecha de la URL.
8. Abajo aparece la respuesta. Arriba a la derecha de la respuesta dice **`Status: 201 Created`**.
9. Guardá con **Ctrl+S**.

## 3. Las demás pruebas
Repetí el paso 2 con cada fila. Si la columna "Body" dice "—", no hace falta el paso 5 ni el 6.

| Nombre | Método | URL | Body (líneas de `tests/test_api.http`) | Esperado |
|---|---|---|---|---|
| 7. Listar Productos | GET | `http://127.0.0.1:8000/productos/?skip=0&limit=5` | — | 200 |
| 8. Detalle Producto | GET | `http://127.0.0.1:8000/productos/1` | — | 200 |
| 9. Actualizar Producto | PUT | `http://127.0.0.1:8000/productos/1` | 67 a 75 | 200 |
| 9.1 Nombre duplicado | POST | `http://127.0.0.1:8000/productos/` | 81 a 89 | 409 |
| 10. Consultar Stock | GET | `http://127.0.0.1:8000/productos/1/stock` | — | 200 |
| 11. Eliminar Producto | DELETE | `http://127.0.0.1:8000/productos/1` | — | 200 |
| 11.1 Eliminar inexistente | DELETE | `http://127.0.0.1:8000/productos/99` | — | 404 |
| 12. Detalle inexistente | GET | `http://127.0.0.1:8000/productos/99` | — | 404 |
| 13. Producto inválido | POST | `http://127.0.0.1:8000/productos/` | 111 a 119 | 422 |
| 13.1 Nombre solo espacios | POST | `http://127.0.0.1:8000/productos/` | 125 a 133 | 422 |

## 4. Exportar el `.json` para la entrega (cuando estén todas)
1. Clic derecho en la colección `TP5 - Productos` y elegí **Export**.
2. Elegí **Collection v2.1** y luego **Export**.
3. Guardalo en la carpeta `tests\` del proyecto.
