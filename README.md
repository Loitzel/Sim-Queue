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
Evaluar la probabilidad de que un cliente no pueda ser atentido inmediatamente debido a la falta de capacidad del sistema (probabilidad de que el sistema esté saturado) para comprender la eficiencia del sistema en la gestión de la demanda y la asignación de recursos.
Estimar el tiempo promedio que un cliente en el sistema (en la cola y en el servidor)
Calcular la probabilidad de que el sistema tenga 0 clientes para poder determinar la eficiencia y capacidad del sistema.


### Variables que describen el problema

Cantidad de servidores: Representa el número de servidores disponibles en el sistema para atender a los clientes. 

Tiempo de servicio: Indica la duración total del servicio.

Distribución de llegada de clientes: Describe el patrón o la ley que sigue la llegada de nuevos clientes al sistema. 

Distribución de tiempo de servicio: Indica cómo se distribuyen los tiempos de servicio de los servidores al atender a los clientes. 

### Sistema Especifico y variables de interes:
#### Sistema Especifico:
Como ya se ha dicho en la introduccion, el sistema que se va a simular
es un sistema con n servidores en paralelo. Cada servidor puede seguir una distribucion distinta del tiempo de atencion.
El tiempo de llegada de los clientes tambien puede seguir una distribucion distinta.

Para facilitar el uso de nuestra implementacion, se han dejado ya implementadas las distribuciones de poisson, exponencial, normal y uniforme.


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
En esta simulacion, modelamos una cola M/M/c o de Erlang.

M: Indica que las llegadas de clientes siguen una distribución de Poisson (M), lo que significa que los intervalos de tiempo entre las llegadas sucesivas de clientes siguen una distribución exponencial.
M: También indica que los tiempos de servicio en el sistema siguen una distribución exponencial, lo que significa que la duración del servicio para cada cliente es independiente y sigue una distribución exponencial.
c: Representa el número de servidores en el sistema. En el sistema M/M/c, hay múltiples servidores disponibles para atender a los clientes que llegan a la cola.
El tamaño de la cola es infinito, lo que significa que no hay límite para la cantidad de clientes que pueden esperar en la cola.

Usamos estas distribuciones ya que en la literatura se ha demostrado que son las mas adecuadas para modelar sistemas de colas, y podremos usar los resultados de la teoria de cola para comparar con los resultados obtenidos en la simulacion.


### Formulas y comparaciones

> p: rho = λ / (c * μ) representa la utilización promedio del sistema, que es la fracción de tiempo que los servidores están ocupados. Si rho es mayor que 1, el sistema está sobrecargado y no puede manejar la tasa de llegada de clientes.
>
> c: representa el número de servidores en el sistema.
> 
> λ: representa la tasa de llegada promedio de los clientes al sistema siguiendo una distribución de Poisson.
> 
> μ: representa la tasa de servicio promedio de los servidores en el sistema siguiendo una distribución exponencial.


#### Probabilidad de que el cliente tenga que esperar en la cola
La probabilidad de que un cliente tenga que esperar en la cola se puede calcular utilizando la fórmula de Erlang C, que se define como:

![formula](/images/Screenshot 2024-02-23 233644.png)



#### Cantidad promedio de clientes en el sistema
La cantidad promedio de clientes en el sistema se puede calcular utilizando la siguiente formula:
    
![formula](/images/Screenshot%202024-02-23%20233707.png)


C(c, p): representa la formula de Erlang C, que se utiliza para calcular la probabilidad de que un cliente tenga que esperar en la cola.

#### Probabilidad de que el sistema tenga 0 clientes
La probabilidad de que el sistema tenga 0 clientes se puede calcular utilizando la siguiente formula:

![formula](/images/1.png)

#### Cantidad de personas promedio en la cola
La cantidad promedio de clientes en la cola se puede calcular utilizando la siguiente formula:

![formula](/images/Screenshot 2024-02-23 234855.png)

#### Tiempo promedio que un cliente pasa en la cola
El tiempo promedio que un cliente pasa en la cola se puede calcular utilizando la siguiente formula:

![formula](/images/2.png)

#### Tiempo promedio que un cliente pasa en el sistema
El tiempo promedio que un cliente pasa en el sistema se puede calcular utilizando la siguiente formula:

![formula](/images/Screenshot 2024-02-23 233553.png)

## Comparaciones
> Resultados de las metricas
> 
> ![foto](/images/Screenshot 2024-02-23 234029.png)

> Resultados obtenidos en la simulacion
> 
> ![foto](/images/Screenshot 2024-02-23 234015.png)

Como se puede observar, los resultados obtenidos de la simulación son consistentes con las fórmulas teóricas. Esto indica que el modelo de simulación implementado es preciso y puede utilizarse para comprender el comportamiento y el rendimiento del sistema M/M/c.


### Supuestos y restricciones
Movimiento instantáneo entre servidores: Se asume que el movimiento de clientes entre servidores es instantáneo, lo que significa que un cliente puede pasar de un servidor a otro sin demora alguna.

Distribución invariable de llegadas de clientes: Se supone que la distribución de llegadas de clientes no cambia con el tiempo. Esto implica que la tasa de llegada de clientes se mantiene constante durante toda la simulación.

Permanencia de clientes no atendidos: Se establece que un cliente que llega al sistema permanece en el sistema hasta que es atendido por un servidor o hasta que concluye el tiempo de servicio sin ser atendido. No se permite que un cliente abandone el sistema sin ser atendido, a menos que expire el tiempo de servicio.

