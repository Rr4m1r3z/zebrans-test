# zebrans-test

## Instrucciones para levantar el proyecto de forma local
+ Crea una carpeta contenedora llamada zebrand
+ Estando al nivel de la carpeta creada, ejecutar el siguiente comando de git
```
git clone git@github.com:Rr4m1r3z/zebrans-test.git zebrand
```
+ Una vez clonado el proyecto, se tendran que asiganar los valores de email y pass en el archivo .env, estos valores son para que se pueda realizar el envio del correo al momento de hacer algun movimiento en la sección de los productos, estos valores se tiene que asignar antes de la construcción de los contenedores ya que actuan cómo variables del sistema.
+ Una vez asignados los valores y situados dentro de la carpeta zebrand, procederemos a ejecutar los siguientes comandos para crear los contenedores y posteriormente levantarlos
+ Creando los contenedores
```
docker build -t zebrand:latest .
```
+ Al termino de la construcción de los contenedores, levantaremos los contenedores con el siguiente comando
```
docker-compose up -d
```
+ Una vez levantados los contenedores se tendrá que importar la base de datos con el siguiente comando:
```
cat <file.sql> | docker exec -i <container> /usr/bin/mysql -u <username> --password=<ps> <db>
```
+ Una vez levantados los contenedores e importada la base de datos, podemos proceder al consumo de los enpoints
+ La base de datos cuenta ya con un usuario admin (admin@outlook.com,zebrands) con el cual se podran dar de alta nuevos usuarios y productos
