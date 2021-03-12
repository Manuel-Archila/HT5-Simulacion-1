# Universidad del Valle de Guatemala
# Algoritmos y Estrucutura de Datos - Sección 10
# Christopher García 20541
# Alejandro Archila 161250
# Referencias tomadas del módulo de Simpy

#imports
import simpy
import random
import statistics

#Atributos iniciales

#Velocidad (Atiende esta cantidad de procesos en unidades de tiempo)
VelocidadCPU = 1
#Instrucciones por unidad de tiempo
TiempoIns = 6
# Total de procesos que llegan
Total_P = 10
#Cantidad de procesos que realizará 
Canti_Pro = 200
#Lista que tendra los tiempos de los procesos, esto permitirá calcular 
#la desviación estándar con stadistics
tiempos = []
#Cantidad de RAM Total
RAM_Tot = 100
#Tiempo total, contador
TiempoTotal = 0

#Los %letras son usos del String Interpolation
#Referencias de: https://stackabuse.com/python-string-interpolation-with-the-percent-operator/

#Funcion que controla todo el proceso de un SO
def SistemaOperativoSO(nombre, env, RAM_Total, RAM_Process, InstruccionesTot, ProcesosT, VelocidadIns):

  #Variables globales para guardar los tiempos del programa (Referencia ejemplo gasolinera)
  global TiempoTotal
  global tiempos

  #Simular la llegada de nuevos procesos que esperaran su asignación de memoria RAM (Parte 1: New)
  yield env.timeout(ProcesosT)
  print('(Nuevo ingreso) --> %s) Ingresa y solicita %d de RAM' % (nombre, RAM_Process))
  T_Ingreso = env.now

  #Simulacion de solicitud de RAM y espera que lo acepten, luego se realizan las instrucciones (Parte 2: Ready)
  yield RAM_Capacity.get(RAM_Process)
  print('(Aceptado) --> %s) Se acepta su solicitud de %d de RAM' % (nombre, RAM_Process))

  #Instrucciones terminadas (Contador)
  InstruccionesTer = 0

  while (InstruccionesTer < InstruccionesTot):
    #Ahora se dirigen, los procesos, al CPU
    #Si está ocupado deben de esperar su turno
    with CPU.request() as turno:
      yield turno

      #Si el numero de instrucciones totales - las instrucciones terminadas es
      #mayor a la velocidad permitida del CPU se restringe a la velocidad del CPU
      #De lo contrario se toma la resta como las instrucciones pendientes o restantes
      if (InstruccionesTot - InstruccionesTer) >= VelocidadIns:
        InstruccionesP = VelocidadIns
      else:
        InstruccionesP = (InstruccionesTot - InstruccionesTer)
      
      print('(Ready) --> %s) El CPU trabajara con %d instrucciones' % (nombre, InstruccionesP))
      
      #Tiempo en que las instrucciones se realizan/ejecutan
      yield env.timeout(InstruccionesP/VelocidadIns)

      #Se realiza la suma al contador de Instrucciones terminadas
      InstruccionesTer += InstruccionesP
      print('(En ejecucion) --> %s) Instrucciones finalizadas: %d de %d' % (nombre, InstruccionesTer, InstruccionesTot)) 

      #Se decide que pasará, si el proceso se dirige a Ready nuevamente o entra a IO operations
      WaitingNumber = random.randint(1,2)
      if(WaitingNumber == 1 and InstruccionesTer < InstruccionesTot):

        #Situación para Waiting (I/O operations)
        with IO_Operations.request() as turnoIO:
          yield turnoIO
          yield env.timeout(1)
          print('(Waiting) --> %s) Operaciones I/O realizadas' % (nombre))

  #Mientras se pueda tener memoria RAM se ejecuta todo el proceso
  yield RAM_Capacity.put(MemRam)
  print('(Terminated) --> %s) Utilizo de memoria RAM: %d' % (nombre, MemRam))
  #Se agrega al contador del tiempo total cada tiempo
  TiempoTotal += (env.now - T_Ingreso)
  #Se agrega a una lista cada tiempo para poder sacar la desviación estandar con stadistics posteriormente
  tiempos.append(env.now - T_Ingreso)

#Ambiente

env = simpy.Environment()
#Parámetros de la simulación
IO_Operations = simpy.Resource(env, capacity = 2) #2, 1 por entrada y otro para salida
RAM_Capacity = simpy.Container(env, RAM_Tot, RAM_Tot)
CPU = simpy.Resource(env, capacity = 1)

#Semilla que utilizará la simulación
random.seed(300)

#Se coloca dentro del paréntesis la cantidad de procesos
for i in range(Canti_Pro):
  # Número de instrucciones que realizaran los procesos
  Total_I = random.randint(1,10)
  # Solicitud de memoria RAM para cada proceso
  MemRam = random.randint(1, 10)
  # Creación de procesos
  CreationPro = random.expovariate(1.0/Total_P)
  #Se llama a la función que controla todo
  env.process(SistemaOperativoSO('Operacion %d' %i, env, RAM_Capacity, MemRam, Total_I, CreationPro, VelocidadCPU * TiempoIns))

#Se inicia la simulación, se detendrá hasta que se acaben los procesos
env.run()

#Finaliza la simulación, se hacen cálculos y se imprimen resultados
print()

#Calculo del promedio de tiempo de los procesos
PromedioT = (TiempoTotal/Canti_Pro)
PromedioT = round(PromedioT, 3)
print("El promedio de tiempo en los procesos fue de: ", PromedioT, " unidades de tiempo")

#Calculo de la desviacion estandar del tiempo
desviacion = statistics.stdev(tiempos)
desviacion = round(desviacion, 3)
print("La desviacion estandar del tiempo promedio fue de: " + str(desviacion) + " unidades de tiempo")