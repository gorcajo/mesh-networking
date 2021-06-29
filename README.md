# Mesh Networking Experiment

Este proyecto es para experimentar con redes malladas mediante la simulación de nodos que se comunican por radiofrecuencia.

## 1. Tipos de redes malladas

Existen dos tipos de redes malladas:

- **Flooding**: Los mensajes se transmiten por inundación hasta llegar a su destino. Los nodos pueden implementar algún tipo de filtrado de mensajes (por descarte de mensajes con tiempo de vida agotado o por descarte de mensajes duplicados) para evitar colapsar la red, especialmente si ésta presenta bucles.

- **Routing**: Los mensajes se transmiten sólo a través de la ruta más óptima hasta llegar al nodo de destino. Los nodos deben implementar un complejo protocolo que provea a ésta de funcionalidades de self-forming y self-healing, de modo que los nodos conozcan de forma autónoma qué rutas deben seguir los mensajes en caso de caídas o reconexiones.

Las flooding networks son más ineficientes que las routing networks ya que provocan alta congestión, a cambio son más mucho fáciles de implementar.

## 2. Nodos

Los nodos tienen los siguientes atributos como mínimo:

- **ID**: La identificación única del nodo.
- **Posición**: Coordenadas X e Y del nodo.
- **Potencia**: La distancia a la que es capaz de transmitir un mensaje a otros nodos. No influye en la capacidad de recepción.
- **Tipo**: Flooding o routing.

Según el tipo de red que se desee implementar los nodos pueden incorporar atributos extra.

Consideraciones:

- Los nodos emiten mensajes en todas direcciones. Todos los nodos que se encuentren dentro del alcance de un nodo emisor recibirán sus mensajes.
- Ningún nodo conoce a priori qué nodos tiene en dentro de su alcance. Para ello deben producirse intercambios de mensajes.
- La cantidad, distribución y características de los nodos viene dada por la simulación.

## 3. Mensajes

Los mensajes tienen los siguientes atributos como mínimo:

- **ID**: La identificación única del mensaje.
- **Payload**: Contenido, de tipo `string`.

Según el tipo de red que se desee implementar los mensajes pueden incorporar atributos extra.

## 4. Notas de implementación

Los únicos módulos necesarios para implementar las redes malladas en sí son `node.py` y `message.py`. Lo demás es código de infraestructura de la simulación o del control de la misma.

## 5. To-do list

- Generador procedural de redes.
- Routing Mesh Network protocol.
