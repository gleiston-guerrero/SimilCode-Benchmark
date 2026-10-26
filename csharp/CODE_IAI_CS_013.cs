using System;

namespace UnitConverter
{
    class ConversionApp
    {
        static void Main(string[] args)
        {
            Console.WriteLine("=== CONVERSOR DE UNIDADES ===");
            Console.WriteLine("1. Metros a Pies");
            Console.WriteLine("2. Celsius a Fahrenheit");
            Console.WriteLine("3. Kilogramos a Libras");
            Console.Write("Seleccione conversión: ");
            
            int choice = Convert.ToInt32(Console.ReadLine());
            double result = 0;
            
            if (choice == 1)
            {
                Console.Write("Ingrese metros: ");
                double meters = Convert.ToDouble(Console.ReadLine());
                result = meters * 3.28084;
                Console.WriteLine($"{meters} metros = {result:F2} pies");
            }
            else if (choice == 2)
            {
                Console.Write("Ingrese grados Celsius: ");
                double celsius = Convert.ToDouble(Console.ReadLine());
                result = (celsius * 9/5) + 32;
                Console.WriteLine($"{celsius}°C = {result:F2}°F");
            }
            else if (choice == 3)
            {
                Console.Write("Ingrese kilogramos: ");
                double kilograms = Convert.ToDouble(Console.ReadLine());
                result = kilograms * 2.20462;
                Console.WriteLine($"{kilograms} kg = {result:F2} libras");
            }
            
            if (result > 100)
                Console.WriteLine("Valor convertido alto");
            else
                Console.WriteLine("Valor convertido normal");
        }
    }
}
