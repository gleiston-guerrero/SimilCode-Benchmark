using System;

namespace InventarioTienda
{
    class ControlStock
    {
        static void Main(string[] args)
        {
            Console.WriteLine("=== Gestión de Inventario ===");
            
            int producto1, producto2, producto3;
            
            Console.Write("Cantidad de laptops: ");
            producto1 = int.Parse(Console.ReadLine());
            
            Console.Write("Cantidad de tablets: ");
            producto2 = int.Parse(Console.ReadLine());
            
            Console.Write("Cantidad de celulares: ");
            producto3 = int.Parse(Console.ReadLine());
            
            int totalProductos = producto1 + producto2 + producto3;
            
            Console.WriteLine($"Total de productos: {totalProductos}");
            
            if (totalProductos > 200)
            {
                Console.WriteLine("Nivel de stock: ALTO");
            }
            else if (totalProductos > 100)
            {
                Console.WriteLine("Nivel de stock: MEDIO");
            }
            else
            {
                Console.WriteLine("Nivel de stock: BAJO - Reabastecer");
            }
            
            Console.ReadKey();
        }
    }
}