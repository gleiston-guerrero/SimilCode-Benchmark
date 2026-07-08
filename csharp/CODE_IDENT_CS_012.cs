using System;
using System.Collections.Generic;

namespace InventarioBasico
{
    class Program
    {
        static void Main(string[] args)
        {
            List<string> productos = new List<string>();
            List<int> cantidades = new List<int>();
            
            Console.WriteLine("=== SISTEMA DE INVENTARIO ===");
            
            for (int i = 0; i < 3; i++)
            {
                Console.Write($"Producto {i + 1}: ");
                string producto = Console.ReadLine();
                productos.Add(producto);
                
                Console.Write($"Cantidad de {producto}: ");
                int cantidad = Convert.ToInt32(Console.ReadLine());
                cantidades.Add(cantidad);
            }
            
            int totalItems = 0;
            Console.WriteLine("\n=== INVENTARIO ACTUAL ===");
            for (int i = 0; i < productos.Count; i++)
            {
                Console.WriteLine($"{productos[i]}: {cantidades[i]} unidades");
                totalItems += cantidades[i];
                
                if (cantidades[i] < 10)
                    Console.WriteLine("  ⚠️ Stock bajo");
                else if (cantidades[i] > 50)
                    Console.WriteLine("  ✅ Stock alto");
                else
                    Console.WriteLine("  ➡️ Stock normal");
            }
            
            Console.WriteLine($"\nTotal de artículos en inventario: {totalItems}");
            
            if (totalItems < 50)
                Console.WriteLine("Inventario necesita reposición");
            else
                Console.WriteLine("Inventario en buen estado");
        }
    }
}
