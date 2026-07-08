using System;

namespace ConversorUnidades
{
    class Program
    {
        static void Main(string[] args)
        {
            Console.WriteLine("=== CONVERSOR DE UNIDADES ===");
            Console.WriteLine("1. Metros a Pies");
            Console.WriteLine("2. Celsius a Fahrenheit");
            Console.WriteLine("3. Kilogramos a Libras");
            Console.Write("Seleccione conversión: ");
            
            int opcion = Convert.ToInt32(Console.ReadLine());
            double resultado = 0;
            
            if (opcion == 1)
            {
                Console.Write("Ingrese metros: ");
                double metros = Convert.ToDouble(Console.ReadLine());
                resultado = metros * 3.28084;
                Console.WriteLine($"{metros} metros = {resultado:F2} pies");
            }
            else if (opcion == 2)
            {
                Console.Write("Ingrese grados Celsius: ");
                double celsius = Convert.ToDouble(Console.ReadLine());
                resultado = (celsius * 9/5) + 32;
                Console.WriteLine($"{celsius}°C = {resultado:F2}°F");
            }
            else if (opcion == 3)
            {
                Console.Write("Ingrese kilogramos: ");
                double kg = Convert.ToDouble(Console.ReadLine());
                resultado = kg * 2.20462;
                Console.WriteLine($"{kg} kg = {resultado:F2} libras");
            }
            
            if (resultado > 100)
                Console.WriteLine("Valor convertido alto");
            else
                Console.WriteLine("Valor convertido normal");
        }
    }
}
