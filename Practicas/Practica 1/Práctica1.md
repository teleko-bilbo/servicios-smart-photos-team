# Análisis de Cuellos de Botella y Pruebas de Carga

## 1. Identificación de Cuellos de Botella

### Reflexionar sobre los principales cuellos de botella en el sistema.
Los principales cuellos de botella relacionados a la utilización del servicio "Smart Photos" son los siguientes:

  #### CPU, GPU, RAM, bateria/corriente. 
      El consumo de CPU, GPU, RAM y bateria y/o potencia de corriente puede ser un cuello de botella en caso de que haya varios
      usuarios demandando servicios de conversion de calidad/formato para sus videos.

      CPU: transcodificar imagenes / video requiere una alta capacidad de procesamiento ya que es necesario decodificar, procesar
      y recodificar en un nuevo formato.

      GPU: para acelerar el proceso de transcodificación de videos, a veces se utiliza GPU. Esto, tiene su impacto en el consumo
      de corriente.

      RAM:  La calidad original del video y su tamaño video, el consumo de memoria RAM será mayo¡r o menos


  #### Ancho de banda (BW). 


  #### Tiempo de servicio.


  #### Almacenamiento (HDD y SSD). 


### Analizar la complejidad de los procesos de forma teórica.

## 2. Selección de Herramientas para Pruebas de Carga
- Evaluar y elegir entre las siguientes herramientas:
  - JMeter
  - Gatling
  - Locust
  - k6
  - Otras herramientas relevantes

## 3. Mediciones Prácticas en un Único Nodo
- Realizar pruebas en un solo nodo para obtener mediciones precisas.

### 3.1 Definición de Peticiones
- Definir las peticiones necesarias para las pruebas o realizar un *recording* de las mismas.

### 3.2 Variación de Parámetros
- Variar el número de usuarios y el tiempo durante las pruebas para evaluar el rendimiento bajo diferentes condiciones.

### 3.3 Análisis del Lado del Cliente y del Servidor
- Considerar y analizar el rendimiento desde ambas perspectivas: cliente y servidor.
