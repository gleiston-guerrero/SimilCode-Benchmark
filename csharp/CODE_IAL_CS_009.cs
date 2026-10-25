using System;
using System.Collections.Generic;

namespace AdministracionAlumnos
{
    class Gestor
    {
        static void Main(string[] args)
        {
            List<string> nombres = new List<string>();
            List<double> notas = new List<double>();
            
            Console.WriteLine("=== SISTEMA DE ALUMNOS ===");
            
            for (int i = 0; i < 3; i++)
            {
                Console.Write($"Ingrese nombre del alumno {i + 1}: ");
                string nombre = Console.ReadLine();
                nombres.Add(nombre);
                
                Console.Write($"Ingrese nota de {nombre}: ");
                double nota = Convert.ToDouble(Console.ReadLine());
                notas.Add(nota);
            }
            
            double total = 0;
            for (int i = 0; i < notas.Count; i++)
            {
                total += notas[i];
                Console.WriteLine($"{nombres[i]}: {notas[i]}");
            }
            
            double promedio = total / notas.Count;
            Console.WriteLine($"Promedio del grupo: {promedio:F2}");
            
            if (promedio >= 7.0)
                Console.WriteLine("Excelente rendimiento grupal");
            else
                Console.WriteLine("Necesita mejorar el grupo");
        }
    }
}
