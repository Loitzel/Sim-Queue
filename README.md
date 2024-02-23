# Proyecto de Simulacion

> Autores:
> - [Loitzel C412]()
> - [Karen C411]()

## Introduccion:
En este proyecto pretendemos simular el comportamiento de una cola ante un servicio que posee n servidores en paralelo. Cuando un cliente llega, se une a la cola si todos los servidores están ocupados. Si algun servidor libre, el cliente entrara al primer servidor (del 1 al n) que este libre.

Cuando un cliente completa el servicio con un servidor (no importa cuál), ese cliente luego abandona el sistema. El cliente que ha estado en la cola durante más tiempo (si hay clientes en la cola) entra en servicio.


### Objetivos y Metas:
El objetivo principal del proyecto es simular el sistema descrito anteriormente para comprender su comportamiento y desempeño bajo diferentes condiciones y distribuciones de arribos y servicio. Las metas específicas incluyen:

-Analizar la utilización de los servidores en función del número de servidores y las distribuciones de arribos y servicio.
-Evaluar la longitud promedio de la cola y los tiempos de espera de los clientes en la cola.
-Estudiar el impacto de variar el número de servidores en el rendimiento del sistema.
Identificar posibles cuellos de botella y áreas de mejora en el diseño del sistema.

### Sistema Especifico y variables de interes:
#### Sistema Especifico:
M/M/c
#### Variables de interes:
El objetivo principal del proyecto es simular el sistema descrito anteriormente para comprender su comportamiento y desempeño bajo diferentes condiciones y distribuciones de arribos y servicio. Las metas específicas incluyen:

Analizar el tiempo de espera promedio de los clientes en la cola para evaluar la eficiencia del sistema en la atención de los clientes.
Determinar el tiempo de espera máximo experimentado por un cliente en la cola para identificar posibles casos extremos de espera.
Calcular la cantidad total de clientes atendidos durante la simulación para entender la capacidad de procesamiento del sistema.
Estimar la cantidad de clientes que no se llegan a atender debido a la falta de capacidad del sistema.

## Detalles de Implementacion
### Lenguaje de Programacion:
- Python

### Pasos seguidos para la implementacion:
1. Modelar las clases necesarias para el sistema de colas.
2. Modelar el comportamiento de los clientes.
3. Modelar el comportamiento del servidor.
4. Modelar el comportamiento del sistema de colas.
5. Realizar pruebas de los modelos implementados.

## Resultados y Experimentos
### Hallazgos de la simulacion
Insertar 

### Interpretacion de los resultados
Insertar

### Necesidad de realizar el analisis estadistico a la simulacion
Insertar

### Analisis de parada de la simulacion
Insertar

## Modelo Matematico
### Descricion del modelo de simulacion

### Supuestos y restricciones
