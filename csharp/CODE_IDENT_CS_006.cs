using System;

namespace ConvertirTemperatura
{
    class Program
    {
        static void Main(string[] args)
        {
            Console.WriteLine("=== Conversor de Temperatura ===");
            
            Console.Write("Ingrese temperatura en Celsius: ");
            double celsius = Convert.ToDouble(Console.ReadLine());
            
            Console.Write("Convertir a (1-Fahrenheit, 2-Kelvin): ");
            int opcion = Convert.ToInt32(Console.ReadLine());
            
            double resultado = 0;
            string unidad = "";
            
            if (opcion == 1)
            {
                resultado = (celsius * 9 / 5) + 32;
                unidad = "Fahrenheit";
            }
            else if (opcion == 2)
            {
                resultado = celsius + 273.15;
                unidad = "Kelvin";
            }
            else
            {
                Console.WriteLine("Opción inválida");
                Console.ReadKey();
                return;
            }
            
            Console.WriteLine($"{celsius}°C = {resultado:F2}°{(opcion == 1 ? "F" : "K")}");
            
            if (resultado > 100)
                Console.WriteLine("Temperatura alta");
            else if (resultado < 0)
                Console.WriteLine("Temperatura bajo cero");
            else
                Console.WriteLine("Temperatura moderada");
            
            Console.ReadKey();
        }
    }
}