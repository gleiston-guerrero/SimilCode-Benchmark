using System;
using System.Collections.Generic;

namespace AdministraMercado
{
    class GestorInventario
    {
        static void Main(string[] args)
        {
            List<string> items = new List<string>();
            List<int> existencias = new List<int>();
            
            Console.WriteLine("=== SISTEMA DE INVENTARIO ===");
            
            for (int i = 0; i < 3; i++)
            {
                Console.Write($"Producto {i + 1}: ");
                string item = Console.ReadLine();
                items.Add(item);
                
                Console.Write($"Cantidad de {item}: ");
                int cantidad = Convert.ToInt32(Console.ReadLine());
                existencias.Add(cantidad);
            }
            
            int sumaTotal = 0;
            Console.WriteLine("\n=== INVENTARIO ACTUAL ===");
            for (int i = 0; i < items.Count; i++)
            {
                Console.WriteLine($"{items[i]}: {existencias[i]} unidades");
                sumaTotal += existencias[i];
                
                if (existencias[i] < 10)
                    Console.WriteLine("  ⚠️ Stock bajo");
                else if (existencias[i] > 50)
                    Console.WriteLine("  ✅ Stock alto");
                else
                    Console.WriteLine("  ➡️ Stock normal");
            }
            
            Console.WriteLine($"\nTotal de artículos en inventario: {sumaTotal}");
            
            if (sumaTotal < 50)
                Console.WriteLine("Inventario necesita reposición");
            else
                Console.WriteLine("Inventario en buen estado");
        }
    }
}
