using System;
using System.Collections.Generic;

namespace ControlTemperatura
{
    class Program
    {
        static void Main(string[] args)
        {
            List<double> temperaturas = new List<double>();
            Console.WriteLine("=== CONTROL DE TEMPERATURA ===");
            
            Console.Write("¿Cuántas mediciones desea registrar? ");
            int cantidad = Convert.ToInt32(Console.ReadLine());
            
            for (int i = 0; i < cantidad; i++)
            {
                Console.Write($"Temperatura {i + 1} (°C): ");
                double temp = Convert.ToDouble(Console.ReadLine());
                temperaturas.Add(temp);
            }
            
            double suma = 0;
            double maxima = temperaturas[0];
            double minima = temperaturas[0];
            
            foreach (double temp in temperaturas)
            {
                suma += temp;
                if (temp > maxima) maxima = temp;
                if (temp < minima) minima = temp;
                
                Console.Write($"{temp}°C ");
                if (temp > 30)
                    Console.WriteLine("- CALOR");
                else if (temp < 15)
                    Console.WriteLine("- FRÍO");
                else
                    Console.WriteLine("- NORMAL");
            }
            
            double promedio = suma / temperaturas.Count;
            Console.WriteLine($"\nPromedio: {promedio:F1}°C");
            Console.WriteLine($"Máxima: {maxima}°C");
            Console.WriteLine($"Mínima: {minima}°C");
        }
    }
}