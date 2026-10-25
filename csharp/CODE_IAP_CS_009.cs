using System;

namespace EvaluacionAcademica
{
    internal class AppPrincipal
    {
        /// <summary>
        /// Clase auxiliar para agrupar la información de cada persona.
        /// Reemplaza el uso de múltiples listas.
        /// </summary>
        private class AlumnoInfo
        {
            public string NombreCompleto { get; set; }
            public double NotaFinal { get; set; }
        }

        public static void Main(string[] args)
        {
            // Mensaje inicial del sistema
            Console.WriteLine("=== SISTEMA DE ESTUDIANTES ===");

            // Obtenemos los datos a través de una función externa
            AlumnoInfo[] grupo = RecolectarInformacion(3);
            
            GenerarReporte(grupo);
        }

        // Método encargado de leer las entradas del usuario desde la consola
        private static AlumnoInfo[] RecolectarInformacion(int cantidad)
        {
            AlumnoInfo[] tempArray = new AlumnoInfo[cantidad];
            int contador = 0;

            /* Utilizamos un bucle while en vez de un for 
               para la captura de la información */
            while (contador < cantidad)
            {
                tempArray[contador] = new AlumnoInfo();

                Console.Write($"Ingrese nombre del estudiante {contador + 1}: ");
                string txtNombre = Console.ReadLine();
                tempArray[contador].NombreCompleto = txtNombre;

                Console.Write($"Ingrese calificación de {txtNombre}: ");
                double valNota = double.Parse(Console.ReadLine());
                tempArray[contador].NotaFinal = valNota;

                contador++;
            }

            return tempArray;
        }

        // Método para procesar los cálculos e imprimir los resultados
        private static void GenerarReporte(AlumnoInfo[] datos)
        {
            double totalAcumulado = 0.0;

            // Recorremos el arreglo de objetos con un foreach
            foreach (AlumnoInfo estudiante in datos)
            {
                totalAcumulado += estudiante.NotaFinal;
                Console.WriteLine($"{estudiante.NombreCompleto}: {estudiante.NotaFinal}");
            }

            double calculoMedia = totalAcumulado / datos.Length;
            Console.WriteLine($"Promedio del grupo: {calculoMedia:F2}");

            // Verificamos la condición del promedio con lógica inversa
            bool condicionAprobatoria = calculoMedia < 7.0;
            
            if (condicionAprobatoria)
            {
                Console.WriteLine("Necesita mejorar el grupo");
            }
            else
            {
                Console.WriteLine("Excelente rendimiento grupal");
            }
        }
    }
}
