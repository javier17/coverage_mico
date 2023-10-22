# Gestión de usuarios
El microservicio de gestión de usuarios permite crear usuarios y validar la identidad de un usuario por medio de tokens.

**Entidad**

Un usuario consta de:

|**Campo**|**tipo de dato**|**descripción**|
| :- | :- | :- |
|id|número|identificador del usuario|
|username|cadena de caracteres sin espacios y caracteres especiales|nombre de usuario|
|email|cadena de caracteres en formato de correo electrónico|dirección de correo electrónico del usuario|
|password|cadena de caracteres|password cifrado del usuario|
|salt|cadena de caracteres|sal para el cifrado del password [leer](https://auth0.com/blog/adding-salt-to-hashing-a-better-way-to-store-passwords/)|
|token|cadena de caracteres|Token actual del usuario|
|expireAt|datetime|fecha y hora de vencimiento del token|
|createdAt|datetime|fecha de creación del usuario|
**API**

**Creación de usuarios**

- **Descripción**

Crea un usuario con los datos brindados, el nombre del usuario debe ser único, así como el correo.

|||
| :- | :-: |
|Método|POST|
|Ruta|/users/|
|Parámetros|N/A|
|Cuerpo|{"username": nombre de usuario, "password": contraseña del usuario, "email": correo electrónico del usuario}|
- **Respuestas**

|**Código**|**Cuerpo**|**Descripción**|
| :-: | :-: | :-: |
|400||En el caso que alguno de los campos no esté presente en la solicitud.|
|412||En el caso que el usuario con el username o el correo ya exista.|
|201|{"id": id del usuario, "createdAt": fecha de creación del usuario en formato ISO}|En el caso que el usuario se haya creado con éxito.|
**Generación de token**

- **Descripción**

Genera un nuevo Token para el usuario al que le corresponde el username y la contraseña.

|||
| :- | :-: |
|Método|POST|
|Ruta|/users/auth|
|Parámetros|N/A|
|Cuerpo|{"username": nombre de usuario, "password": contraseña del usuario}|
- **Respuestas**

|**Código**|**Cuerpo**|**Descripción**|
| :-: | :-: | :-: |
|400||En el caso que alguno de los campos no esté presente en la solicitud.|
|404||En el caso que el usuario con username y password no exista.|
|200|{"id": id del usuario, "token": Token generado para la sesión del usuario, "expireAt": fecha y hora de vencimiento del token en formato ISO}|Si el usuario es válido.|
**Consultar información del usuario**

- **Descripción**

Retorna los datos del usuario al que pertenece el token.

|||
| :- | :-: |
|Método|GET|
|Ruta|/users/me|
|Parámetros|N/A|
|Encabezados|Authorization: Bearer token|
- **Respuestas**

|**Código**|**Cuerpo**|**Descripción**|
| :-: | :-: | :-: |
|401||El token no es válido o está vencido.|
|400||El token no está en el encabezado de la solicitud.|
|200|{"id": identificador del usuario, "username": nombre de usuario, "email": correo electrónico del usuario}|En el caso que el token sea válido|
**Consulta de salud del servicio**

- **Descripción**

Usado para verificar el estado de la aplicación.

|||
| :- | :-: |
|Método|GET|
|Descripción|Retorna dato básico solo para indicar que la aplicación está arriba.|
|Ruta|/users/ping|
- **Respuestas**

|**Código**|**Cuerpo**|**Descripción**|
| :-: | :-: | :-: |
|200|pong|Solo para confirmar que el servicio está arriba.|

