using System;
using System.Collections.Generic;

namespace AdministracionNotas
{
    class ManejadorNotas
    {
        static void Main()
        {
            List<double> notasEstudiantes = new List<double>();
            
            Console.WriteLine("Sistema de Calificaciones");
            Console.Write("Ingrese el número de estudiantes: ");
            int cantidadEstudiantes = int.Parse(Console.ReadLine());
            
            for (int indice = 0; indice < cantidadEstudiantes; indice++)
            {
                Console.Write($"Calificación del estudiante {indice + 1}: ");
                double nota = double.Parse(Console.ReadLine());
                notasEstudiantes.Add(nota);
            }
            
            double total = 0;
            foreach (double nota in notasEstudiantes)
            {
                total += nota;
            }
            
            double media = total / notasEstudiantes.Count;
            string resultado = media >= 7.0 ? "Aprobado" : "Reprobado";
            
            Console.WriteLine($"Promedio del grupo: {media:F2}");
            Console.WriteLine($"Estado del grupo: {resultado}");
            
            if (media >= 9.0)
                Console.WriteLine("¡Excelente rendimiento!");
            else if (media >= 7.0)
                Console.WriteLine("Buen rendimiento");
            else
                Console.WriteLine("Necesita mejorar");
        }
    }
}
