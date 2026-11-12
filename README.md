# Latino TV HD

Lista M3U personalizada con canales de Republica Dominicana, Puerto Rico, Venezuela, Colombia y Mexico.

## Lista

Cuando el flujo automatico haya terminado, la lista publica estara disponible en:

https://raw.githubusercontent.com/rsanchezdelacruz5/Latino-tv/main/Latino-TV-HD.m3u

## Filtros

- Resolucion etiquetada: 720p, 1080p, 1440p, 2160p, 4K o UHD.
- Categorias: noticias, deportes, peliculas, series, infantil, entretenimiento, animacion, familiar y comedia.
- Se eliminan URLs duplicadas.
- Se agrupan los canales por pais y categoria.

El filtro es conservador: los canales que no indiquen explicitamente una resolucion HD/UHD en sus metadatos pueden quedar fuera aunque transmitan en alta definicion.

## Actualizacion automatica

GitHub Actions reconstruye la lista diariamente y tambien permite ejecutarla manualmente desde la pestana **Actions** del repositorio.

## Uso

- VLC: Medio > Abrir ubicacion de red y pegar el enlace Raw de arriba.
- TiviMate: Add Playlist > M3U Playlist y pegar el mismo enlace.

## Fuente y aviso

Los datos se obtienen de las listas publicas del proyecto [iptv-org/iptv](https://github.com/iptv-org/iptv). Es un catalogo comunitario: los enlaces pueden cambiar o dejar de funcionar. Utiliza unicamente canales y streams cuya distribucion tengas autorizacion para recibir.
