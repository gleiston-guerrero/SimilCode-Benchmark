using System;
using System.Collections.Generic;

namespace GestionVentas
{
    class Program
    {
        static void Main(string[] args)
        {
            List<string> productos = new List<string>();
            List<double> precios = new List<double>();
            
            Console.WriteLine("=== SISTEMA DE VENTAS ===");
            
            for (int i = 0; i < 3; i++)
            {
                Console.Write($"Ingrese nombre del producto {i + 1}: ");
                string producto = Console.ReadLine();
                productos.Add(producto);
                
                Console.Write($"Ingrese precio de {producto}: ");
                double precio = Convert.ToDouble(Console.ReadLine());
                precios.Add(precio);
            }
            
            double total = 0;
            for (int i = 0; i < precios.Count; i++)
            {
                total += precios[i];
                Console.WriteLine($"{productos[i]}: ${precios[i]}");
            }
            
            double promedio = total / precios.Count;
            Console.WriteLine($"Precio promedio: ${promedio:F2}");
            
            if (promedio >= 100.0)
                Console.WriteLine("Productos de alta gama");
            else
                Console.WriteLine("Productos económicos");
        }
    }
}