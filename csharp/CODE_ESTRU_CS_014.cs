using System;
using System.Collections.Generic;

namespace ControlInventario
{
    class Program
    {
        static void Main()
        {
            List<int> cantidades = new List<int>();
            
            Console.WriteLine("Sistema de Control de Inventario");
            Console.Write("Ingrese el número de productos: ");
            int numProductos = int.Parse(Console.ReadLine());
            
            for (int i = 0; i < numProductos; i++)
            {
                Console.Write($"Cantidad del producto {i + 1}: ");
                int cantidad = int.Parse(Console.ReadLine());
                cantidades.Add(cantidad);
            }
            
            int total = 0;
            foreach (int cantidad in cantidades)
            {
                total += cantidad;
            }
            
            double promedioCantidad = (double)total / cantidades.Count;
            string estadoStock = promedioCantidad >= 50 ? "Stock Suficiente" : "Stock Bajo";
            
            Console.WriteLine($"Promedio de inventario: {promedioCantidad:F2}");
            Console.WriteLine($"Estado del inventario: {estadoStock}");
            
            if (promedioCantidad >= 100)
                Console.WriteLine("¡Inventario óptimo!");
            else if (promedioCantidad >= 50)
                Console.WriteLine("Inventario adecuado");
            else
                Console.WriteLine("Necesita reposición urgente");
        }
    }
}