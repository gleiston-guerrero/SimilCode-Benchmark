using System;

namespace NotaPromedio
{
    class Evaluador
    {
        static void Main(string[] args)
        {
            Console.WriteLine("=== Calculadora de Promedio ===");
            double calificacion1, calificacion2, calificacion3;
            
            Console.Write("Ingrese la primera nota: ");
            calificacion1 = Convert.ToDouble(Console.ReadLine());
            
            Console.Write("Ingrese la segunda nota: ");
            calificacion2 = Convert.ToDouble(Console.ReadLine());
            
            Console.Write("Ingrese la tercera nota: ");
            calificacion3 = Convert.ToDouble(Console.ReadLine());
            
            double promedio = (calificacion1 + calificacion2 + calificacion3) / 3;
            
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
