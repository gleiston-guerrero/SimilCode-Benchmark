using System;
using System.Collections.Generic;

namespace ControlTemperaturas
{
    class Program
    {
        static void Main()
        {
            List<double> temperaturas = new List<double>();
            
            Console.WriteLine("Monitor de Temperaturas");
            Console.Write("¿Cuántas mediciones desea registrar? ");
            int mediciones = int.Parse(Console.ReadLine());
            
            for (int i = 0; i < mediciones; i++)
            {
                Console.Write($"Temperatura {i + 1} (°C): ");
                double temp = double.Parse(Console.ReadLine());
                temperaturas.Add(temp);
            }
            
            double suma = 0;
            double maxTemp = temperaturas[0];
            double minTemp = temperaturas[0];
            
            foreach (double temp in temperaturas)
            {
                suma += temp;
                if (temp > maxTemp) maxTemp = temp;
                if (temp < minTemp) minTemp = temp;
            }
            
            double promedio = suma / temperaturas.Count;
            
            Console.WriteLine($"\nAnálisis climático:");
            Console.WriteLine($"Suma total: {suma:F1}°C");
            Console.WriteLine($"Temperatura promedio: {promedio:F2}°C");
            Console.WriteLine($"Temperatura máxima: {maxTemp:F1}°C");
            Console.WriteLine($"Temperatura mínima: {minTemp:F1}°C");
            Console.WriteLine($"Variación: {maxTemp - minTemp:F1}°C");
            
            if (promedio > 25)
                Console.WriteLine("Clima cálido registrado");
            else
                Console.WriteLine("Clima fresco registrado");
        }
    }
}
