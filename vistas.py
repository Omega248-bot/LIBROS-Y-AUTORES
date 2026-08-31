from fastapi import APIRouter, Form, Request
from fastapi.templating import Jinja2Templates


from dependencias import ConnectionDep
from esquemas import AutorActualizar, AutorCrear, LibroActualizar, LibroCrear
from repositorio import (
    actualizar_autor, actualizar_libro, crear_autor, crear_libro,
    eliminar_autor, eliminar_libro, obtener_autor, obtener_autores,
    obtener_autores_de_libro, obtener_libro, obtener_libros,
    obtener_libros_de_autor,
)

router = APIRouter(tags=["vistas"])
templates = Jinja2Templates(directory="templates")

@router.get("/")
async def inicio(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="inicio.html",
    )


@router.get("/libros")
async def listar_libros(request: Request, conn: ConnectionDep):
    libros = await obtener_libros(conn)
    return templates.TemplateResponse(
        request=request,
        name="libros.html",
        context={"libros": libros},
    )


@router.post("/libros")
async def crear_libro_vista(
    request: Request,
    conn: ConnectionDep,
    titulo: str = Form(),
    fecha_publicacion: int | None = Form(default=None),
):
    libro = LibroCrear(titulo=titulo, fecha_publicacion=fecha_publicacion)
    await crear_libro(conn, libro.titulo, libro.fecha_publicacion)
    libros = await obtener_libros(conn)
    return templates.TemplateResponse(
        request=request,
        name="partials/tabla_libros.html",
        context={"libros": libros},
    )


@router.get("/libros/{libro_id}/editar")
async def editar_libro_vista(request: Request, conn: ConnectionDep, libro_id: int):
    libro = await obtener_libro(conn, libro_id)
    return templates.TemplateResponse(
        request=request,
        name="partials/fila_editar_libro.html",
        context={"libro": libro},
    )


@router.get("/libros/{libro_id}/cancelar")
async def cancelar_edicion_libro_vista(request: Request, conn: ConnectionDep, libro_id: int):
    libro = await obtener_libro(conn, libro_id)
    return templates.TemplateResponse(
        request=request,
        name="partials/fila_libro.html",
        context={"libro": libro},
    )


@router.get("/libros/{libro_id}/autores")
async def ver_autores_libro_vista(request: Request, conn: ConnectionDep, libro_id: int):
    libro = await obtener_libro(conn, libro_id)
    autores = await obtener_autores_de_libro(conn, libro_id)
    return templates.TemplateResponse(
        request=request,
        name="partials/fila_autores_libro.html",
        context={"libro": libro, "autores": autores},
    )


@router.get("/libros/{libro_id}/autores/cerrar")
async def cerrar_autores_libro_vista(request: Request, conn: ConnectionDep, libro_id: int):
    libro = await obtener_libro(conn, libro_id)
    return templates.TemplateResponse(
        request=request,
        name="partials/fila_libro.html",
        context={"libro": libro},
    )


@router.put("/libros/{libro_id}")
async def actualizar_libro_vista(
    request: Request,
    conn: ConnectionDep,
    libro_id: int,
    titulo: str = Form(),
    fecha_publicacion: int | None = Form(default=None),
):
    libro = LibroActualizar(titulo=titulo, fecha_publicacion=fecha_publicacion)
    await actualizar_libro(conn, libro_id, libro.titulo, libro.fecha_publicacion)
    libro_actualizado = await obtener_libro(conn, libro_id)
    return templates.TemplateResponse(
        request=request,
        name="partials/fila_libro.html",
        context={"libro": libro_actualizado},
    )


@router.delete("/libros/{libro_id}")
async def eliminar_libro_vista(request: Request, conn: ConnectionDep, libro_id: int):
    await eliminar_libro(conn, libro_id)
    libros = await obtener_libros(conn)
    return templates.TemplateResponse(
        request=request,
        name="partials/tabla_libros.html",
        context={"libros": libros},
    )


@router.get("/autores")
async def listar_autores(request: Request, conn: ConnectionDep):
    autores = await obtener_autores(conn)
    return templates.TemplateResponse(
        request=request,
        name="autores.html",
        context={"autores": autores},
    )


@router.post("/autores")
async def crear_autor_vista(
    request: Request,
    conn: ConnectionDep,
    nombre: str = Form(),
    pais: str | None = Form(default=None),
    nacimiento: int | None = Form(default=None),
):
    autor = AutorCrear(nombre=nombre, pais=pais, nacimiento=nacimiento)
    await crear_autor(conn, autor.nombre, autor.pais, autor.nacimiento)
    autores = await obtener_autores(conn)
    return templates.TemplateResponse(
        request=request,
        name="partials/tabla_autores.html",
        context={"autores": autores},
    )


@router.get("/autores/{autor_id}/editar")
async def editar_autor_vista(request: Request, conn: ConnectionDep, autor_id: int):
    autor = await obtener_autor(conn, autor_id)
    return templates.TemplateResponse(
        request=request,
        name="partials/fila_editar_autor.html",
        context={"autor": autor},
    )


@router.get("/autores/{autor_id}/cancelar")
async def cancelar_edicion_vista(request: Request, conn: ConnectionDep, autor_id: int):
    autor = await obtener_autor(conn, autor_id)
    return templates.TemplateResponse(
        request=request,
        name="partials/fila_autor.html",
        context={"autor": autor},
    )


@router.get("/autores/{autor_id}/libros")
async def ver_libros_autor_vista(request: Request, conn: ConnectionDep, autor_id: int):
    autor = await obtener_autor(conn, autor_id)
    libros = await obtener_libros_de_autor(conn, autor_id)
    return templates.TemplateResponse(
        request=request,
        name="partials/fila_libros_autor.html",
        context={"autor": autor, "libros": libros},
    )


@router.get("/autores/{autor_id}/libros/cerrar")
async def cerrar_libros_autor_vista(request: Request, conn: ConnectionDep, autor_id: int):
    autor = await obtener_autor(conn, autor_id)
    return templates.TemplateResponse(
        request=request,
        name="partials/fila_autor.html",
        context={"autor": autor},
    )


@router.put("/autores/{autor_id}")
async def actualizar_autor_vista(
    request: Request,
    conn: ConnectionDep,
    autor_id: int,
    nombre: str = Form(),
    pais: str | None = Form(default=None),
    nacimiento: int | None = Form(default=None),
):
    autor = AutorActualizar(nombre=nombre, pais=pais, nacimiento=nacimiento)
    await actualizar_autor(conn, autor_id, autor.nombre, autor.pais, autor.nacimiento)
    autor_actualizado = await obtener_autor(conn, autor_id)
    return templates.TemplateResponse(
        request=request,
        name="partials/fila_autor.html",
        context={"autor": autor_actualizado},
    )


@router.delete("/autores/{autor_id}")
async def eliminar_autor_vista(request: Request, conn: ConnectionDep, autor_id: int):
    await eliminar_autor(conn, autor_id)
    autores = await obtener_autores(conn)
    return templates.TemplateResponse(
        request=request,
        name="partials/tabla_autores.html",
        context={"autores": autores},
    )