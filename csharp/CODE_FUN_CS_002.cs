using System;

namespace EvaluacionEstudiante
{
    class SistemaNotas
    {
        static void Main(string[] args)
        {
            Console.WriteLine("=== Sistema de Calificaciones ===");
            
            double[] calificaciones = new double[3];
            string[] materias = {"Matemáticas", "Física", "Programación"};
            
            for(int i = 0; i < 3; i++)
            {
                Console.Write($"Nota de {materias[i]}: ");
                calificaciones[i] = double.Parse(Console.ReadLine());
            }
            
            double suma = 0;
            foreach(double nota in calificaciones)
            {
                suma += nota;
            }
            double promedioFinal = suma / calificaciones.Length;
            
            Console.WriteLine("Promedio obtenido: " + promedioFinal.ToString("F2"));
            
            string resultado = (promedioFinal >= 3.0) ? "APROBADO" : "REPROBADO";
            Console.WriteLine("Estado académico: " + resultado);
                
            Console.ReadKey();
        }
    }
}