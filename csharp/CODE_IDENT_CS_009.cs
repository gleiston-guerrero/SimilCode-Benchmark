using System;
using System.Collections.Generic;

namespace GestionEstudiantes
{
    class Program
    {
        static void Main(string[] args)
        {
            List<string> estudiantes = new List<string>();
            List<double> calificaciones = new List<double>();
            
            Console.WriteLine("=== SISTEMA DE ESTUDIANTES ===");
            
            for (int i = 0; i < 3; i++)
            {
                Console.Write($"Ingrese nombre del estudiante {i + 1}: ");
                string nombre = Console.ReadLine();
                estudiantes.Add(nombre);
                
                Console.Write($"Ingrese calificación de {nombre}: ");
                double calificacion = Convert.ToDouble(Console.ReadLine());
                calificaciones.Add(calificacion);
            }
            
            double suma = 0;
            for (int i = 0; i < calificaciones.Count; i++)
            {
                suma += calificaciones[i];
                Console.WriteLine($"{estudiantes[i]}: {calificaciones[i]}");
            }
            
            double promedio = suma / calificaciones.Count;
            Console.WriteLine($"Promedio del grupo: {promedio:F2}");
            
            if (promedio >= 7.0)
                Console.WriteLine("Excelente rendimiento grupal");
            else
                Console.WriteLine("Necesita mejorar el grupo");
        }
    }
}