using System;

namespace CalculadoraNotas
{
    class Program
    {
        static void Main(string[] args)
        {
            Console.WriteLine("=== Calculadora de Promedio ===");
            double nota1, nota2, nota3;
            
            Console.Write("Ingrese la primera nota: ");
            nota1 = Convert.ToDouble(Console.ReadLine());
            
            Console.Write("Ingrese la segunda nota: ");
            nota2 = Convert.ToDouble(Console.ReadLine());
            
            Console.Write("Ingrese la tercera nota: ");
            nota3 = Convert.ToDouble(Console.ReadLine());
            
            double promedio = (nota1 + nota2 + nota3) / 3;
            
            Console.WriteLine($"El promedio es: {promedio:F2}");
            
            if (promedio >= 3.0)
            {
                Console.WriteLine("¡Aprobado!");
            }
            else
            {
                Console.WriteLine("Reprobado");
            }
            
            Console.ReadKey();
        }
    }
}