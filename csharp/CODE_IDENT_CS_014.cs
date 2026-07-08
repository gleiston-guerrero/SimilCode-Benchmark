using System;
using System.Collections.Generic;

namespace GestionEstudiantes
{
    class Program
    {
        static void Main()
        {
            List<double> calificaciones = new List<double>();
            
            Console.WriteLine("Sistema de Calificaciones");
            Console.Write("Ingrese el número de estudiantes: ");
            int numEstudiantes = int.Parse(Console.ReadLine());
            
            for (int i = 0; i < numEstudiantes; i++)
            {
                Console.Write($"Calificación del estudiante {i + 1}: ");
                double nota = double.Parse(Console.ReadLine());
                calificaciones.Add(nota);
            }
            
            double suma = 0;
            foreach (double nota in calificaciones)
            {
                suma += nota;
            }
            
            double promedio = suma / calificaciones.Count;
            string estado = promedio >= 7.0 ? "Aprobado" : "Reprobado";
            
            Console.WriteLine($"Promedio del grupo: {promedio:F2}");
            Console.WriteLine($"Estado del grupo: {estado}");
            
            if (promedio >= 9.0)
                Console.WriteLine("¡Excelente rendimiento!");
            else if (promedio >= 7.0)
                Console.WriteLine("Buen rendimiento");
            else
                Console.WriteLine("Necesita mejorar");
        }
    }
}