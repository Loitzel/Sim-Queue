# Proyecto de Simulacion

> Autores:
> - [Loitzel C412]()
> - [Karen C411]()

## Introduccion:
El proyecto consiste en la simulación de un sistema de colas con n servidores en paralelo, en el cual se 
simula el comportamiento de los clientes, los tiempos de llegada y los tiempos 
de servicio de cada servidor.
Los clientes que requieren un servicio se generan en el tiempo en una fuente de entrada.
Luego, entran al sistema y se unen a una cola. En determinado momento se selecciona
un miembro de la cola para proporcionarle el servicio y este es atendido por un servidor vacio.
Una vez transcurrido el tiempo de servicio, el cliente sale del sistema y se libera el servidor.


### Objetivos y Metas:
- Simular el comportamiento de un sistema de colas.
- Analizar el comportamiento del sistema de colas.
- Comparar los resultados obtenidos con los resultados teóricos.


### Sistema Especifico y variables de interes:
#### Sistema Especifico:
El sistema especifico a simular es un sistema de colas con n servidores en paralelo, donde 
los clientes llegan de acuerdo a una distribucion arbitraria y son atendidos por un servidor; cada servidor tiene un
tiempo de servicio que sigue una distribucion arbitraria.

La cola implementada es de tamaño infinito, es decir, no hay restricciones en la cantidad de clientes que pueden estar en la cola. 
Y ademas, la cola es de disciplina FIFO, es decir, el primer cliente en llegar es el primero en ser atendido.

En la teoria, lo mas usual es que los arrivos usen una distribucion de Poissson y los tiempos de servicio una distribucion exponencial.

#### Variables de interes:
- Tiempo de espera promedio.
- Tiempo de espera máximo.
- Cantidad de clientes atendidos.
- Cantidad de clientes que quedan encolados una vez culmina el tiempo.
- Tiempo total en el que el sistema esta vacio.
- Probabilidad de que un cliente nuevo tenga que esperar en la cola.

## Detalles de Implementacion
### Lenguaje de Programacion:
- Python

### Pasos seguidos para la implementacion:
1. Crear las variables aleatorias con las distribuciones definidas.
2. Crear la logica de la simulacion, simulando los eventos de llegada y salida de clientes una vez han sido atendidos.
3. Realizar la simulacion con un tiempo de simulacion definido.
4. Repetir la simulacion un numero de veces para obtener resultados mas confiables.

## Resultados y Experimentos
### Hallazgos de la simulacion
Insertar 

### Interpretacion de los reusltados
Insertar

### Necesidad de realizar el analisis estadistico a la simulacion
Insertar

### Analisis de parada de la simulacion
Insertar

## Modelo Matematico
### Descricion del modelo de simulacion
En la teoria de colas, las distruciones mas comunes para este tipo de simulaciones son las
distribuciones de Poisson para la llegada de los clientes y Exponencial para la atencion a estos mismos.

Tomemos c como la cantidad de servidores, lambda como la tasa de llegada de los clientes y mu como la tasa de servicio de los servidores.
Sea la utilizacion de los servidores como rho, que es igual a lambda/mu*c. 
En nuestra simulacion, rho < 1, es decir, la tasa de llegada de los clientes es menor a la tasa de servicio de los servidores; por lo tanto se considera que el sistema es estable.

En un sistema estable: se tienen varias metricas:
- Tiempo de servicio: 1/mu
- Utilizacion promedio del sistema: lambda/mu
- Factor de utilizacion: rho
- y mas https://www.estadistica.net/IO/7-3-TEORIA-COLAS.pdf
- ahi estan todas las medidas, que solo quedaria implementarlas y ver q correspondan

### Supuestos y restricciones
