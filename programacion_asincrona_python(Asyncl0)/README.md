Las corrutinas son como los threads; la diferencia es que podemos decidir cuando se deja de ejecutar una corrutina, para ejecutar otra.

Se ejecutan sobre un unico hilo.

Vamos a hacer que parezcan que se ejecutan "concurrentemente"

Corrutina ==> Funcion que tiene la capacidad de ponerse en pausa para permitir que otras corrutinas empiecen a ejecutarse.

Cada vez que tengo que invocar una corrutina, tengo que poner un "await" delante.

asyncio.run(corrutina()) ==> Para iniciar una corrutina.

No podemos utilizarla si ya tenemos un event loop corriendo en el mismo hilo.

"gather()" ==> esperar a que las corrutinas que hayan en marcha, pasadas por parametros, terminen. Si no estan terminadas, no continua con la ejecucion.

EXAMEN

tipo test y respuestas cortas. 