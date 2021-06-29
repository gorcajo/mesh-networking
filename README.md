# Mesh Networking Experiment

Este proyecto es para experimentar con redes malladas, simulando una red de nodos de que se comunican por radiofrecuencia.

Existen dos tipos de redes malladas:

- **Flooding**: Los mensajes se transmiten por inundación en la red hasta llegar a su destino. Los nodos pueden implementar algún tipo de filtrado de mensajes (por descarte de mensajes con tiempo de vida agotado o por descarte de mensajes duplicados) para evitar colapsar la red si ésta presenta bucles.

- **Routing**: Los mensajes se transmiten sólo a través de la ruta más óptima hasta llegar al nodo de destino. Los nodos deben implementar un complejo protocolo que provea a ésta de funcionalidades de self-forming y self-healing, de modo que los nodos conozcan de forma autónoma qué rutas deben seguir los mensajes en caso de caídas o reconexiones.

Las flooding networks son más ineficientes que las routing networks ya que pueden provocar una gran congestión, a cambio son más mucho fáciles de implementar.

Los nodos tienen los siguientes atributos:

- ID: La identificación única del nodo.
- Posición: Coordenadas X e Y del nodo.
- Potencia: La distancia a la que es capaz de transmitir un mensaje a otros nodos. No influye en la capacidad de recepción.
- Tipo: Flooding o routing.

Los únicos módulos que son necesarios para implementar el core del experimentos son `node.py` y `message.py`. Lo demás es código de infraestructura de la simulación o para el control de la misma.

## To Do

- Generador procedural de redes.
- Routing Mesh Network protocol.
