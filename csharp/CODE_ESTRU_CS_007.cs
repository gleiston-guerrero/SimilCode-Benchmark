using System;

namespace CalculadoraAntiguedad
{
    class Program
    {
        static void Main(string[] args)
        {
            Console.WriteLine("=== Calculadora de Antigüedad Laboral ===");
            
            Console.Write("Ingrese año de ingreso a la empresa: ");
            int añoIngreso = Convert.ToInt32(Console.ReadLine());
            
            Console.Write("Ingrese el año actual: ");
            int añoActual = Convert.ToInt32(Console.ReadLine());
            
            int antiguedad = añoActual - añoIngreso;
            
            Console.WriteLine($"Antigüedad laboral: {antiguedad} años");
            
            string categoria;
            if (antiguedad < 2)
                categoria = "Empleado nuevo";
            else if (antiguedad < 5)
                categoria = "Empleado junior";
            else if (antiguedad < 15)
                categoria = "Empleado senior";
            else
                categoria = "Empleado veterano";
            
            Console.WriteLine($"Categoría: {categoria}");
            
            if (antiguedad >= 5)
                Console.WriteLine("Tiene derecho a vacaciones extendidas");
            else
                Console.WriteLine("Vacaciones estándar");
            
            Console.ReadKey();
        }
    }
}