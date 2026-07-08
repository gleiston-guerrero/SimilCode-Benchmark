using System;

namespace ControlVentas
{
    class Program
    {
        static void Main(string[] args)
        {
            Console.WriteLine("=== Control de Ventas Diarias ===");
            
            int ventasManana = 0;
            int ventasTarde = 0;
            int ventasNoche = 0;
            int totalVentas = 0;
            
            Console.WriteLine("Registrar ventas por turno:");
            Console.WriteLine("1 - Turno Mañana");
            Console.WriteLine("2 - Turno Tarde");
            Console.WriteLine("3 - Turno Noche");
            Console.WriteLine("0 - Cerrar registro");
            
            while (true)
            {
                Console.Write("\nRegistrar venta en turno: ");
                int turno = Convert.ToInt32(Console.ReadLine());
                
                if (turno == 0)
                    break;
                else if (turno == 1)
                {
                    ventasManana++;
                    totalVentas++;
                }
                else if (turno == 2)
                {
                    ventasTarde++;
                    totalVentas++;
                }
                else if (turno == 3)
                {
                    ventasNoche++;
                    totalVentas++;
                }
                else
                {
                    Console.WriteLine("Turno inválido");
                }
            }
            
            Console.WriteLine("\n=== REPORTE DE VENTAS ===");
            Console.WriteLine($"Ventas Mañana: {ventasManana}");
            Console.WriteLine($"Ventas Tarde: {ventasTarde}");
            Console.WriteLine($"Ventas Noche: {ventasNoche}");
            Console.WriteLine($"Total del día: {totalVentas}");
            
            if (ventasManana > ventasTarde && ventasManana > ventasNoche)
                Console.WriteLine("Turno más productivo: Mañana");
            else if (ventasTarde > ventasManana && ventasTarde > ventasNoche)
                Console.WriteLine("Turno más productivo: Tarde");
            else if (ventasNoche > ventasManana && ventasNoche > ventasTarde)
                Console.WriteLine("Turno más productivo: Noche");
            else
                Console.WriteLine("Hay empate en productividad");
            
            Console.ReadKey();
        }
    }
}