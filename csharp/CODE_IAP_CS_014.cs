using System;

namespace ControlAcademico
{
    internal static class Iniciador
    {
        private static int LeerCantidad(string mensaje)
        {
            Console.Write(mensaje);
            return int.Parse(Console.ReadLine());
        }

        private static double LeerNota(string mensaje)
        {
            Console.Write(mensaje);
            return double.Parse(Console.ReadLine());
        }

        private static double[] ObtenerNotas(int cantidad)
        {
            int capacidad = cantidad > 0 ? cantidad : 0;
            double[] notas = new double[capacidad];
            int indice = 0;

            while (indice < capacidad)
            {
                string texto = string.Format("Calificación del estudiante {0}: ", indice + 1);
                notas[indice] = LeerNota(texto);
                indice++;
            }

            return notas;
        }

        private static double Promediar(double[] notas)
        {
            double acumulado = 0.0;

            foreach (double valor in notas)
            {
                acumulado += valor;
            }

            return acumulado / notas.Length;
        }

        private static string Clasificar(double promedio)
        {
            return promedio >= 7.0 ? "Aprobado" : "Reprobado";
        }

        private static void ImprimirRendimiento(double promedio)
        {
            if (promedio >= 9.0)
            {
                Console.WriteLine("¡Excelente rendimiento!");
            }
            else if (promedio >= 7.0)
            {
                Console.WriteLine("Buen rendimiento");
            }
            else
            {
                Console.WriteLine("Necesita mejorar");
            }
        }

        private static void Ejecutar()
        {
            Console.WriteLine("Sistema de Calificaciones");

            int cantidad = LeerCantidad("Ingrese el número de estudiantes: ");
            double[] notas = ObtenerNotas(cantidad);
            double promedio = Promediar(notas);
            string estado = Clasificar(promedio);

            Console.WriteLine(string.Format("Promedio del grupo: {0:F2}", promedio));
            Console.WriteLine(string.Format("Estado del grupo: {0}", estado));

            ImprimirRendimiento(promedio);
        }

        static void Main()
        {
            Ejecutar();
        }
    }
}
