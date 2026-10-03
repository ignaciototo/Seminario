# Seminario de Actualización

## Clase 03: Introducción a Git y GitHub

Conectar un proyecto local con un repositorio en GitHub.

1. Crear repositorio local
Ejecutar el comando `git init` dentro de la carpeta que se quiere convertir en repositorio. Incluir .gitignore para evitar subir al repositorio remoto librerías y otros archivos que no son necesarios enviar.

2. Crear repositorio remoto
Desde GitHub, crear un repositorio nuevo. Si el repositorio local ya tiene README y gitignore, destildar "Add a README" ni "Add .gitignore" para evitar el conflicto de historias no relacionadas al hacer el primer push.

3. Conectar el repositorio local con el remoto
Ejecutar git remote add con la URL del repositorio (HTTPS o SSH): `git remote add origin https://github.com/usuario/nombre-repo.git`

4. Commit
`git add .`
`git commit -m "comentario"`

5. Subir cambios a GitHub
`git push -u origin main`
**NOTA**:El flag -u registra la relación entre la rama local main y origin/main. En los siguientes push no es necesario incluirlo.

## Ticket de Salida

1. **README duplicado**
   Al crear el repositorio en GitHub, si no se desmarcan las 3 opciones iniciales que vienen activas por defecto, se creará uno con README. Como en el repositorio local ya tenía un README, Git rechaza el push por tener historiales desconectados. Se soluciona trayendo los cambios remotos con `git pull origin main --allow-unrelated-histories`, ajustando manualmente el conflicto, y ejecutando `git add`, `git commit` y el posterior `git push`.

2. **Carpeta sin ignorar**
   Sin el archivo `.gitignore` todo el contenido del repo local se envía al remoto (incluyendo carpetas que no se deberían enviar porque pesan mucho y no son de utilidad en el remoto). Para solucionarlo sin borrar los archivos de mi máquina, se puede ejecutar `git rm -r --cached nombre_carpeta`, hacer commit del cambio y crear el `.gitignore` agregando las carpetas correspondientes para que Git no la vuelva a detectar a futuro.

3. **Ramas master / main**
   El repositorio local se inició con el nombre `master`, mientras que GitHub crea por defecto la rama `main`. Se resuelve cambiando el nombre de la rama local a `main` con `git branch -m master main`, y luego `git push -u origin main`. Para borrar la rama vieja: `git push origin --delete master`.
