using System;
using System.Collections.Generic;

namespace RegistroCalificaciones
{
    class Program
    {
        static void Main(string[] args)
        {
            List<string> materias = new List<string>();
            List<int> notas = new List<int>();
            
            Console.WriteLine("=== REGISTRO DE CALIFICACIONES ===");
            
            for (int i = 0; i < 3; i++)
            {
                Console.Write($"Materia {i + 1}: ");
                string materia = Console.ReadLine();
                materias.Add(materia);
                
                Console.Write($"Calificación en {materia}: ");
                int nota = Convert.ToInt32(Console.ReadLine());
                notas.Add(nota);
            }
            
            int sumaNotas = 0;
            Console.WriteLine("\n=== REPORTE DE NOTAS ===");
            for (int i = 0; i < materias.Count; i++)
            {
                Console.WriteLine($"{materias[i]}: {notas[i]} puntos");
                sumaNotas += notas[i];
                
                if (notas[i] < 60)
                    Console.WriteLine("  ❌ Reprobado");
                else if (notas[i] > 90)
                    Console.WriteLine("  🏆 Excelente");
                else
                    Console.WriteLine("  ✓ Aprobado");
            }
            
            Console.WriteLine($"\nPromedio general: {sumaNotas / notas.Count}");
            
            if (sumaNotas / notas.Count < 70)
                Console.WriteLine("Rendimiento necesita mejorar");
            else
                Console.WriteLine("Buen rendimiento académico");
        }
    }
}