using System;
using System.Collections.Generic;

namespace MonitoreoClimatico
{
    class SistemaMonitoreo
    {
        static void Main(string[] args)
        {
            List<double> valoresTemperatura = new List<double>();
            Console.WriteLine("=== MONITOREO CLIMÁTICO ===");
            
            Console.Write("¿Cuántas lecturas desea registrar? ");
            int numeroLecturas = Convert.ToInt32(Console.ReadLine());
            
            for (int i = 0; i < numeroLecturas; i++)
            {
                Console.Write($"Temperatura {i + 1} (°C): ");
                double valor = Convert.ToDouble(Console.ReadLine());
                valoresTemperatura.Add(valor);
            }
            
            double total = 0;
            double mayor = valoresTemperatura[0];
            double menor = valoresTemperatura[0];
            
            foreach (double temp in valoresTemperatura)
            {
                total += temp;
                if (temp > mayor) mayor = temp;
                if (temp < menor) menor = temp;
                
                Console.Write($"{temp}°C ");
                if (temp > 30)
                    Console.WriteLine("- CALOR");
                else if (temp < 15)
                    Console.WriteLine("- FRÍO");
                else
                    Console.WriteLine("- NORMAL");
            }
            
            double promedio = total / valoresTemperatura.Count;
            Console.WriteLine($"\nPromedio: {promedio:F1}°C");
            Console.WriteLine($"Máxima: {mayor}°C");
            Console.WriteLine($"Mínima: {menor}°C");
        }
    }
}
