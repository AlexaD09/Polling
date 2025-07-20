CREATE TABLE usuarios (
    id_usuario SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    correo VARCHAR(100) UNIQUE NOT NULL,
    pssw VARCHAR(100) NOT NULL,
    rol VARCHAR(50) DEFAULT 'cliente'
);

INSERT INTO
    public.usuarios
VALUES (
        1,
        'Dayana',
        'dayana@mail.com',
        '$2b$12$K/hOX.megM3hUX5XmCubhuvKoPgYXRjL.gBF14bQpcHRlHmDQB8pm',
        'cliente'
    );

INSERT INTO
    public.usuarios
VALUES (
        2,
        'Liliana Carolina Pilatuña Caiza',
        'liliana@mail.com',
        '$2b$12$bLk86L2nuqX9rwN4uls3VOg2o.TM7T554XOCXRZILt2WqW5rmaaUO',
        'cliente'
    );

INSERT INTO
    public.usuarios
VALUES (
        6,
        'Juan David Pilatuña Caiza',
        'juan@mail.com',
        '$2b$12$8kzX7yVUXuRrZfd9OvgAnOjANIC35rCH4Oinaq1J5OCp.ZD8lOuvG',
        'cliente'
    );

INSERT INTO
    public.usuarios
VALUES (
        7,
        'Javier Alexandra Chasipanta Caiza',
        'javier@mail.com',
        '$2b$12$iKLMq1jMcy/4EOpJMojZ2.LGELvGJz96S/WwvQ9H2sf65Z3.YVULS',
        'cliente'
    );

INSERT INTO
    public.usuarios
VALUES (
        0,
        'admin',
        'admin@mail.com',
        '$2b$12$SGmcNROTtuYXp3A.Ab0Qlue37myZY3nS5znMT/GnrA6p2akhIWRv6',
        'admin'
    );

INSERT INTO
    public.usuarios
VALUES (
        3,
        'empleado',
        'empleado@mail.com',
        '$2b$12$mYgv1F2bFFmlxAoIG0wcPuIuRTUwjCIfQCK0v4xgQk4B/.K3jWTFO',
        'empleado'
    );

INSERT INTO
    public.usuarios
VALUES (
        10,
        'Maria Fernanda Llano',
        'fernanda@mail.com',
        '$2b$12$j.nOThdlYs54s7xUJX1y5.ur8Vppgn82FdN7T44rbrDX2j8.TMeta',
        'cliente'
    );

INSERT INTO
    public.usuarios
VALUES (
        11,
        'Elvis Enrique Pilatuña',
        'elvis@mail.com',
        '$2b$12$8mnwStahguESrt.TjG8SlukbcbZG19HlzymRjjUjWStEh3exBNEG6',
        'empleado'
    );

INSERT INTO
    public.usuarios
VALUES (
        12,
        'Alexa Maciel Pilatuña',
        'alexa@mail.com',
        '$2b$12$wDUYKp0QOfQLfl2DLmrMi.mivbrd7viAr/.ZmFdYB2Mi9Xj9sBDPy',
        'empleado'
    );

INSERT INTO
    public.usuarios
VALUES (
        13,
        'Andres Sebastian Factos Vargas',
        'andres@mail.com',
        '$2b$12$Svq372LrW9FXdU8Yu6PifOJdPW8TqDf.k57wjCUFQE8I7nsCIqixO',
        'empleado'
    );

INSERT INTO
    public.usuarios
VALUES (
        14,
        'Viviana Guisella Chimarro',
        'viviana@mail.com',
        '$2b$12$VUaIW3uI7JYVeIhEnYIzQ.bltLgNJUaQkfK9imQlVsqPfc1dlWmb2',
        'empleado'
    );

-- Obtener usuario por correo
CREATE OR REPLACE FUNCTION sp_get_usuario_por_correo(p_correo VARCHAR)
RETURNS TABLE (
    id_usuario INT,
    nombre VARCHAR,
    correo VARCHAR,
    pssw VARCHAR,
    rol VARCHAR
) AS $$
BEGIN
    RETURN QUERY
    SELECT u.id_usuario,
           u.nombre,
           u.correo,
           u.pssw,
           u.rol
    FROM usuarios u
    WHERE u.correo = p_correo;
END;
$$ LANGUAGE plpgsql;

-- Crear usuario (insertar)
CREATE OR REPLACE FUNCTION sp_create_usuario(
    p_nombre VARCHAR,
    p_correo VARCHAR,
    p_pssw VARCHAR,
    p_rol VARCHAR
)
RETURNS VOID AS $$
BEGIN
    INSERT INTO usuarios (nombre, correo, pssw, rol)
    VALUES (p_nombre, p_correo, p_pssw, p_rol);
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION obtener_todos_usuarios()
RETURNS TABLE (
    id_usuario INTEGER,
    nombre VARCHAR,
    correo VARCHAR,
    rol VARCHAR
) AS $$
BEGIN
    RETURN QUERY
    SELECT u.id_usuario AS id_usuario, u.nombre, u.correo, u.rol
    FROM usuarios u;
END;
$$ LANGUAGE plpgsql;

CREATE TABLE quejas_oficina (
    id_queja SERIAL PRIMARY KEY,
    id_usuario SERIAL REFERENCES usuarios (id_usuario),
    nombre_cliente VARCHAR(100) NOT NULL,
    correo_cliente VARCHAR(100),
    titulo VARCHAR(255) NOT NULL,
    descripcion TEXT NOT NULL,
    estado VARCHAR(20) DEFAULT 'Pendiente',
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO
    public.quejas_oficina
VALUES (
        21,
        3,
        'Maria Luz Caiza Jacho',
        'maria@mail.com',
        'Falta de accesibilidad',
        'No hay facilidades para personas con movilidad reducida o discapacidades',
        'Pendiente',
        '2025-07-17 13:39:14.357368'
    );

INSERT INTO
    public.quejas_oficina
VALUES (
        18,
        3,
        'Esperanza Yuli Chimarro',
        'esperanza@mail.com',
        'Pol├¡tica de devoluci├│n complicada',
        'Intent├® devolver un producto y me pusieron muchas trabas o requisitos injustos.',
        'En proceso',
        '2025-07-16 17:21:58.835502'
    );

INSERT INTO
    public.quejas_oficina
VALUES (
        22,
        3,
        'Camila Estefania Sanchez',
        'camila@mail.com',
        'Mal trato del personal',
        'Un empleado fue grosero al momento de responder mis preguntas.',
        'Pendiente',
        '2025-07-18 23:36:40.30702'
    );

INSERT INTO
    public.quejas_oficina
VALUES (
        23,
        11,
        'Vanessa Garcia',
        'vanessa@mail.com',
        'Falta de higiene',
        'El lugar estaba sucio y no parec├¡a seguir normas de limpieza adecuadas.',
        'Resuelto',
        '2025-07-19 04:05:03.870991'
    );

INSERT INTO
    public.quejas_oficina
VALUES (
        24,
        3,
        'Juan Pablo Vargas',
        'pablo@mail.com',
        'Falta de opciones inclusivas',
        'No tienen opciones para personas con alergias, discapacidades o necesidades especiales.',
        'Resuelto',
        '2025-07-19 12:34:14.200911'
    );

INSERT INTO
    public.quejas_oficina
VALUES (
        25,
        3,
        'Hilda Garcia',
        'hilda@mail.com',
        'Temperatura inadecuada',
        'El aire acondicionado no funcionaba bien, hac├¡a mucho calor.',
        'Pendiente',
        '2025-07-19 14:18:01.736182'
    );

INSERT INTO
    public.quejas_oficina
VALUES (
        19,
        3,
        'Flor Valentina Cangui',
        'flor@mail.com',
        'Falta de respuesta a reclamos',
        'He enviado varias quejas y nadie me ha contestado ni dado soluci├│n.',
        'Resuelto',
        '2025-07-16 17:28:00.548192'
    );

INSERT INTO
    public.quejas_oficina
VALUES (
        17,
        3,
        'Claudia Ivonne Lucero',
        'ivonne@mail.com',
        'Ambiente del local inc├│modo',
        'El lugar estaba sucio, desordenado o con mala iluminaci├│n, no es agradable.',
        'Resuelto',
        '2025-07-16 17:15:31.126947'
    );

INSERT INTO
    public.quejas_oficina
VALUES (
        26,
        11,
        'Evelyn Navarrete',
        'evelyn@mail.com',
        'Publicidad enga├▒osa',
        'Ofrecen promociones que no cumplen o que tienen condiciones ocultas.',
        'Pendiente',
        '2025-07-19 16:21:07.004746'
    );

CREATE OR REPLACE FUNCTION sp_crear_queja(
    p_id_usuario INT,
    p_nombre_cliente VARCHAR,
    p_correo_cliente VARCHAR,
    p_titulo VARCHAR,
    p_descripcion TEXT,
    p_estado VARCHAR DEFAULT 'Pendiente'
)
RETURNS TABLE (
    id_queja INT,
    id_usuario INT,
    nombre_cliente VARCHAR,
    correo_cliente VARCHAR,
    titulo VARCHAR,
    descripcion TEXT,
    estado VARCHAR,
    fecha_creacion TIMESTAMP
)
AS $$
BEGIN
    RETURN QUERY
    INSERT INTO quejas_oficina (
        id_usuario, nombre_cliente, correo_cliente,
        titulo, descripcion, estado
    )
    VALUES (
        p_id_usuario, p_nombre_cliente, p_correo_cliente,
        p_titulo, p_descripcion, p_estado
    )
    RETURNING *;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION sp_obtener_quejas()
RETURNS TABLE (
    id_queja INT,
    id_usuario INT,
    nombre_cliente VARCHAR,
    correo_cliente VARCHAR,
    titulo VARCHAR,
    descripcion TEXT,
    estado VARCHAR,
    fecha_creacion TIMESTAMP
)
AS $$
BEGIN
    RETURN QUERY SELECT * FROM quejas_oficina;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION sp_obtener_queja_por_id(p_id_queja INT)
RETURNS TABLE (
    id_queja INT,
    id_usuario INT,
    nombre_cliente VARCHAR,
    correo_cliente VARCHAR,
    titulo VARCHAR,
    descripcion TEXT,
    estado VARCHAR,
    fecha_creacion TIMESTAMP
)
AS $$
BEGIN
    RETURN QUERY SELECT * FROM quejas_oficina WHERE id_queja = p_id_queja;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION sp_actualizar_estado_queja(
    p_id_queja INT,
    p_nuevo_estado VARCHAR
)
RETURNS TABLE (
    id_queja INT,
    id_usuario INT,
    nombre_cliente VARCHAR,
    correo_cliente VARCHAR,
    titulo VARCHAR,
    descripcion TEXT,
    estado VARCHAR,
    fecha_creacion TIMESTAMP
)
AS $$
BEGIN
    RETURN QUERY
    UPDATE quejas_oficina
    SET estado = p_nuevo_estado
    WHERE quejas_oficina.id_queja = p_id_queja
    RETURNING *;
END;
$$ LANGUAGE plpgsql;

select * from quejas_oficina