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

RAM:  La calidad original del video y su tamaño video estarán directamente relacionados al consumo de memoria RAM al ser procesados.

#### Ancho de banda (BW). 
La utilizacion del acho de banda podría ser un cuello de botella si se trata de obtener un video de larga duracion y de alta calidad.

#### Tiempo de servicio.
El tiempo de servicio será la variable que estudiaremos mendiante las pruebas de carga realizadas durante esta práctica. Para medir estos tiempos de servicio, y ademas,
escalar el número de peticiones, utilizaremos JMETER.

Tal y como puede verse, este directorio contiene 3 carpetas, en la cual, cada componente de este grupo incluira el detalle de las pruebas realizadas. Este detalle podrá
encontrarse dentro del Readme.md que tiene cada subdirectorio.

#### Almacenamiento (HDD y SSD). 

El almacenamiento HDD y/o SDD tambien podría ser un cuello de botella, ya que, los usuarios podrian demandar distintos formatos y calidades para uno o varios videos.


### Analizar la complejidad de los procesos de forma teórica.

## 2. Selección de Herramientas para Pruebas de Carga
Para las pruebas de carga, se ha considerado utilizar la herramienta JMETER, ya que el funcionamiento de esta se adecua a las pruebas de ecesitamos realizar. Mediante
esta herramienta, podremos configurar peticiones GET personalizadas que se ajusten a las que necesitemos según la solucion o estudio realizado.

## 3. Mediciones Prácticas en un Único Nodo
- Realizar pruebas en un solo nodo para obtener mediciones precisas.

### 3.1 Definición de Peticiones
- Definir las peticiones necesarias para las pruebas o realizar un *recording* de las mismas.

### 3.2 Variación de Parámetros
- Variar el número de usuarios y el tiempo durante las pruebas para evaluar el rendimiento bajo diferentes condiciones.

### 3.3 Análisis del Lado del Cliente y del Servidor
- Considerar y analizar el rendimiento desde ambas perspectivas: cliente y servidor.
