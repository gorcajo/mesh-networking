# Mesh Networking Experiment

Este proyecto es un experimento de redes malladas mediante la simulación de nodos que se comunican por radiofrecuencia.

Se simula una red formada por `N` nodos con IDs consecutivas empezando por el `0`. El objetivo del experimento es transmitir un mensaje desde el nodo `0` hasta el nodo `N`, para cualquier tipo de red.

## 1. Tipos de redes malladas

Existen dos tipos de redes malladas:

- **Flooding**: Los mensajes se transmiten por inundación hasta llegar a su destino. Los nodos pueden implementar algún tipo de filtrado de mensajes (por descarte de mensajes con tiempo de vida agotado o por descarte de mensajes duplicados) para evitar colapsar la red, especialmente si ésta presenta bucles.

- **Routing**: Los mensajes se transmiten sólo a través de la ruta más óptima hasta llegar al nodo de destino. Los nodos deben implementar un complejo protocolo que provea a ésta de funcionalidades de self-forming y self-healing, de modo que los nodos conozcan de forma autónoma qué rutas deben seguir los mensajes en caso de caídas o reconexiones.

Las flooding networks son más ineficientes que las routing networks ya que provocan alta congestión, a cambio son más mucho fáciles de implementar.

## 2. Nodos

Los nodos tienen como mínimo los siguientes atributos:

- **ID**: La identificación única del nodo.
- **Posición**: Coordenadas X e Y del nodo.
- **Potencia**: La distancia a la que es capaz de transmitir un mensaje a otros nodos. No influye en la capacidad de recepción.
- **Tipo**: Flooding o routing.
- **Estado**: Online u offline.

Según el tipo de red que se desee implementar los nodos pueden incorporar atributos extra.

Consideraciones:

- La cantidad, distribución y atributos de los nodos viene dada por la simulación.
- Todos los nodos saben cuántos nodos hay en la red.
- Ningún nodo conoce a priori qué nodos tiene en dentro de su alcance ni los atributos de los demás nodos. Para ello debe haber intercambio de mensajes.
- Los nodos emiten mensajes en todas direcciones. Todos los nodos que se encuentren dentro del alcance de un nodo emisor recibirán sus mensajes.
- Cuando un nodo se encuentra en estado offline no puede recibir, procesar ni emitir mensajes.
- Cuando un nodo pasa a estado offline toda su memoria es reseteada.

## 3. Mensajes

Los mensajes tienen como mínimo los siguientes atributos:

- **ID**: La identificación única del mensaje.
- **Payload**: Contenido, de tipo `string`.

Según el tipo de red que se desee implementar los mensajes pueden incorporar atributos extra.

Consideraciones:

- Las IDs de los mensajes deben ser únicas, el nodo `0` es responsable de ello ya que es el productor de mensajes.
- La simulación se ejecuta paso a paso, en cada paso se transmite un mensaje de la cola de salida de todos los nodos.
- Los nodos sólo pueden procesar un mensaje por cada paso de la simulación, consumiéndolos de la cola de entrada.
- Los mensajes no tienen límite de tamaño y se transmiten instantáneamenta en cada paso de la simulación.

## 4. Notas de implementación

Los únicos módulos necesarios para implementar las redes malladas en sí son `node.py` y `message.py`. Lo demás es código de infraestructura de la simulación o del control de la misma.

Los nodos deben implementar lógica y pueden tener memoria. Los mensajes no deben implementar lógica.

## 5. To-do list

- Estado de los nodos:
  - Implementar la pérdida de memoria al pasar al estado offline. Impedir que un nodo haga nada cuando está offline.
  - Al pinchar en un nodo se hace toggle entre offline y online.
  - El estado inicial de los nodos (online/offline) se almacena en el YAML, aunque los nodos 0 y N siempre deberían estar online.
- Retocar el YAML para tener la red de pruebas definitiva, con un buen tamaño y nodos de diferentes potencias (lo que provoará enlaces unidireccionales).
- Routing Mesh Network protocol.
- Broadcast messages.

## 6. Notas

Aprovechando el visor de la red y la forma de crear la malla a partir de la posición de los nodos y sus potencias puede salir un buen algoritmo de generación procedural de grafos.
