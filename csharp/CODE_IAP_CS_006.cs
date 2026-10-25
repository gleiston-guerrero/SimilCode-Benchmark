using System;

namespace ThermalUtility
{
    internal static class TemperatureInterpreter
    {
        private static readonly Func<double, double>[] ConversionPipeline =
        {
            c => c * 9.0 / 5.0 + 32.0,
            c => c + 273.15
        };

        private static readonly string[] ScaleAbbreviations = { "F", "K" };

        private static string DescribeThermalState(double level)
        {
            if (level > 100.0)
            {
                return "Temperatura alta";
            }

            if (level < 0.0)
            {
                return "Temperatura bajo cero";
            }

            return "Temperatura moderada";
        }

        private static void ProcessConversation()
        {
            Console.WriteLine("=== Conversor de Temperatura ===");

            Console.Write("Ingrese temperatura en Celsius: ");
            double initialDegree = Convert.ToDouble(Console.ReadLine());

            Console.Write("Convertir a (1-Fahrenheit, 2-Kelvin): ");
            int choice = Convert.ToInt32(Console.ReadLine());

            if (choice < 1 || choice > 2)
            {
                Console.WriteLine("Opción inválida");
                Console.ReadKey();
                return;
            }

            int selectedIndex = choice - 1;
            double finalDegree = ConversionPipeline[selectedIndex](initialDegree);
            string abbreviation = ScaleAbbreviations[selectedIndex];

            Console.WriteLine($"{initialDegree}°C = {finalDegree:F2}°{abbreviation}");
            Console.WriteLine(DescribeThermalState(finalDegree));

            Console.ReadKey();
        }

        public static void Main()
        {
            ProcessConversation();
        }
    }
}
