-- Ejecutar en Supabase > SQL Editor

create table if not exists contactos (
  id_contacto bigint generated always as identity primary key,
  nombre   text not null,
  email    text not null,
  telefono text not null,
  foto     text default 'default.png'
);

-- Si tu tabla contactos YA existe con la columna "imagen", ejecuta solo esta línea:
-- alter table contactos rename column imagen to foto;

create table if not exists sesiones_abiertas (
  token text not null
);

-- Para esta práctica (llave anon) se desactiva RLS; en producción se usarían políticas.
alter table contactos disable row level security;
alter table sesiones_abiertas disable row level security;

-- Refresca la caché de esquema de la API
notify pgrst, 'reload schema';
