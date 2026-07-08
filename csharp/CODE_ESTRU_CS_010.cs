using System;
using System.Collections.Generic;

namespace ControlVelocidad
{
    class Program
    {
        static void Main(string[] args)
        {
            List<double> velocidades = new List<double>();
            Console.WriteLine("=== CONTROL DE VELOCIDAD ===");
            
            Console.Write("¿Cuántos vehículos desea registrar? ");
            int cantidad = Convert.ToInt32(Console.ReadLine());
            
            for (int i = 0; i < cantidad; i++)
            {
                Console.Write($"Velocidad del vehículo {i + 1} (km/h): ");
                double velocidad = Convert.ToDouble(Console.ReadLine());
                velocidades.Add(velocidad);
            }
            
            double suma = 0;
            double maxima = velocidades[0];
            double minima = velocidades[0];
            
            foreach (double vel in velocidades)
            {
                suma += vel;
                if (vel > maxima) maxima = vel;
                if (vel < minima) minima = vel;
                
                Console.Write($"{vel} km/h ");
                if (vel > 80)
                    Console.WriteLine("- EXCESO");
                else if (vel < 40)
                    Console.WriteLine("- LENTO");
                else
                    Console.WriteLine("- NORMAL");
            }
            
            double promedio = suma / velocidades.Count;
            Console.WriteLine($"\nVelocidad promedio: {promedio:F1} km/h");
            Console.WriteLine($"Velocidad máxima: {maxima} km/h");
            Console.WriteLine($"Velocidad mínima: {minima} km/h");
        }
    }
}