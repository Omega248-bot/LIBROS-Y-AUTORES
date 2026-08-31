async def obtener_autores(conn) -> list[dict]:
    rows = await conn.fetch(
        "SELECT * FROM autores ORDER BY id"
    )

    return [dict(row) for row in rows]


async def obtener_autor(
    conn,
    autor_id: int
) -> dict | None:

    row = await conn.fetchrow(
        "SELECT * FROM autores WHERE id = $1",
        autor_id
    )

    return dict(row) if row else None


async def crear_autor(
    conn,
    nombre: str,
    pais: str | None,
    nacimiento: int | None
) -> dict:

    row = await conn.fetchrow(
        """
        INSERT INTO autores (nombre, pais, nacimiento)
        VALUES ($1, $2, $3)
        RETURNING *
        """,
        nombre,
        pais,
        nacimiento,
    )

    return dict(row)


async def actualizar_autor(
    conn,
    autor_id: int,
    nombre: str,
    pais: str | None,
    nacimiento: int | None
) -> dict | None:

    row = await conn.fetchrow(
        """
        UPDATE autores
        SET nombre = $1,
            pais = $2,
            nacimiento = $3
        WHERE id = $4
        RETURNING *
        """,
        nombre,
        pais,
        nacimiento,
        autor_id,
    )

    return dict(row) if row else None


async def obtener_libros_de_autor(
    conn,
    autor_id: int
) -> list[dict]:

    rows = await conn.fetch(
        """
        SELECT l.libro_id, l.titulo, l.fecha_publicacion
        FROM libros l
        JOIN "Autores_Libros" al ON al.libro_id = l.libro_id
        WHERE al.autor_id = $1
        ORDER BY l.titulo
        """,
        autor_id
    )

    return [dict(row) for row in rows]


async def eliminar_autor(
    conn,
    autor_id: int
) -> bool:

    result = await conn.execute(
        "DELETE FROM autores WHERE id = $1",
        autor_id
    )

    return result == "DELETE 1"


async def obtener_libros(conn) -> list[dict]:
    rows = await conn.fetch(
        "SELECT * FROM libros ORDER BY libro_id"
    )

    return [dict(row) for row in rows]


async def obtener_libro(
    conn,
    libro_id: int
) -> dict | None:

    row = await conn.fetchrow(
        "SELECT * FROM libros WHERE libro_id = $1",
        libro_id
    )

    return dict(row) if row else None


async def crear_libro(
    conn,
    titulo: str,
    fecha_publicacion: int | None
) -> dict:

    row = await conn.fetchrow(
        """
        INSERT INTO libros (titulo, fecha_publicacion)
        VALUES ($1, $2)
        RETURNING *
        """,
        titulo,
        fecha_publicacion,
    )

    return dict(row)


async def actualizar_libro(
    conn,
    libro_id: int,
    titulo: str,
    fecha_publicacion: int | None
) -> dict | None:

    row = await conn.fetchrow(
        """
        UPDATE libros
        SET titulo = $1,
            fecha_publicacion = $2
        WHERE libro_id = $3
        RETURNING *
        """,
        titulo,
        fecha_publicacion,
        libro_id,
    )

    return dict(row) if row else None


async def eliminar_libro(
    conn,
    libro_id: int
) -> bool:

    result = await conn.execute(
        "DELETE FROM libros WHERE libro_id = $1",
        libro_id
    )

    return result == "DELETE 1"


async def obtener_autores_de_libro(
    conn,
    libro_id: int
) -> list[dict]:

    rows = await conn.fetch(
        """
        SELECT a.id, a.nombre, a.pais, a.nacimiento
        FROM autores a
        JOIN "Autores_Libros" al ON al.autor_id = a.id
        WHERE al.libro_id = $1
        ORDER BY a.nombre
        """,
        libro_id
    )

    return [dict(row) for row in rows]