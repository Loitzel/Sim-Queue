# Proyecto de Simulacion

> Autores:
> - [Loitzel C412]()
> - [Karen C411]()

## Introduccion:
En este proyecto pretendemos simular el comportamiento de una cola ante un servicio que posee n servidores en paralelo. Cuando un cliente llega, se une a la cola si todos los servidores están ocupados. Si algun servidor libre, el cliente entrara al primer servidor (del 1 al n) que este libre.

Cuando un cliente completa el servicio con un servidor (no importa cuál), ese cliente luego abandona el sistema. El cliente que ha estado en la cola durante más tiempo (si hay clientes en la cola) entra en servicio.


### Objetivos y Metas:
El objetivo principal del proyecto es simular el sistema descrito anteriormente para comprender su comportamiento y desempeño bajo diferentes condiciones y distribuciones de arribos y servicio. Las metas específicas incluyen:

Analizar el tiempo de espera promedio de los clientes en la cola para evaluar la eficiencia del sistema en la atención de los clientes.
Determinar el tiempo de espera máximo experimentado por un cliente en la cola para identificar posibles casos extremos de espera.
Calcular la cantidad total de clientes atendidos durante la simulación para entender la capacidad de procesamiento del sistema.
Estimar la cantidad de clientes que no se llegan a atender debido a la falta de capacidad del sistema.
Evaluar la probabilidad de que un cliente no pueda ser atentido inmediatamente debido a la falta de capacidad del sistema.

### Variables que describen el problema

Cantidad de servidores: Representa el número de servidores disponibles en el sistema para atender a los clientes. 

Tiempo de servicio: Indica la duración total del servicio.

Distribución de llegada de clientes: Describe el patrón o la ley que sigue la llegada de nuevos clientes al sistema. 

Distribución de tiempo de servicio: Indica cómo se distribuyen los tiempos de servicio de los servidores al atender a los clientes. 

### Sistema Especifico y variables de interes:
#### Sistema Especifico:
M/M/c

M: Indica que las llegadas de clientes siguen una distribución de Poisson (M), lo que significa que los intervalos de tiempo entre las llegadas sucesivas de clientes siguen una distribución exponencial.
M: También indica que los tiempos de servicio en el sistema siguen una distribución exponencial, lo que significa que la duración del servicio para cada cliente es independiente y sigue una distribución exponencial.
c: Representa el número de servidores en el sistema. En el sistema M/M/c, hay múltiples servidores disponibles para atender a los clientes que llegan a la cola.

#### Variables de interes:
Tiempo de espera promedio de los clientes en la cola:
Descripción: Representa el tiempo promedio que un cliente pasa esperando en la cola antes de ser atendido.

Promedio del tiempo de espera máximo experimentado por un cliente en la cola:
Descripción: Indica el tiempo máximo que un cliente ha esperado en la cola antes de ser atendido. Este valor ayuda a identificar casos extremos de espera.

Promedio de la cantidad total de clientes atendidos durante la simulación:
Descripción: Representa el número total de clientes que han sido atendidos y han completado su servicio en el sistema durante la simulación.

Promedio de la cantidad de clientes que no se llegan a atender debido a la falta de capacidad del sistema:
Descripción: Indica la cantidad de clientes que no han sido atendidos debido a que el sistema no tiene la capacidad suficiente para procesarlos.

Probabilidad de que un cliente no pueda ser atendido inmediatamente debido a la falta de capacidad del sistema:
Descripción: Representa la probabilidad de que un cliente que llega al sistema no pueda ser atendido de inmediato debido a la falta de capacidad del sistema. Esta probabilidad es una medida de la eficacia del sistema en la gestión de la demanda y la asignación de recursos.

## Detalles de Implementacion
### Lenguaje de Programacion:
- Python

### Pasos seguidos para la implementacion:
1. Modelar distintos tipos de distribuciones
2. Crear las clases StatisticsHolder, StateVariables y Sim para mantener una estructura limpia en el codigo
3. Implementar el algoritmo de simulacion teniendo en cuenta las diferentes distribuciones y almacenando los datos necesarios para el analisis
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
### Descripcion del modelo de simulacion

### Supuestos y restricciones
Movimiento instantáneo entre servidores: Se asume que el movimiento de clientes entre servidores es instantáneo, lo que significa que un cliente puede pasar de un servidor a otro sin demora alguna.

Distribución invariable de llegadas de clientes: Se supone que la distribución de llegadas de clientes no cambia con el tiempo. Esto implica que la tasa de llegada de clientes se mantiene constante durante toda la simulación.

Permanencia de clientes no atendidos: Se establece que un cliente que llega al sistema permanece en el sistema hasta que es atendido por un servidor o hasta que concluye el tiempo de servicio sin ser atendido. No se permite que un cliente abandone el sistema sin ser atendido, a menos que expire el tiempo de servicio.
