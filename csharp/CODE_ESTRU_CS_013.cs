using System;

namespace CalculadoraDescuentos
{
    class Program
    {
        static void Main(string[] args)
        {
            Console.WriteLine("=== CALCULADORA DE DESCUENTOS ===");
            Console.WriteLine("1. Descuento Estudiante (10%)");
            Console.WriteLine("2. Descuento Tercera Edad (15%)");
            Console.WriteLine("3. Descuento VIP (25%)");
            Console.Write("Seleccione descuento: ");
            
            int opcion = Convert.ToInt32(Console.ReadLine());
            double precioFinal = 0;
            
            if (opcion == 1)
            {
                Console.Write("Ingrese precio original: ");
                double precio = Convert.ToDouble(Console.ReadLine());
                precioFinal = precio * 0.90;
                Console.WriteLine($"Precio con descuento estudiante: ${precioFinal:F2}");
            }
            else if (opcion == 2)
            {
                Console.Write("Ingrese precio original: ");
                double precio = Convert.ToDouble(Console.ReadLine());
                precioFinal = precio * 0.85;
                Console.WriteLine($"Precio con descuento tercera edad: ${precioFinal:F2}");
            }
            else if (opcion == 3)
            {
                Console.Write("Ingrese precio original: ");
                double precio = Convert.ToDouble(Console.ReadLine());
                precioFinal = precio * 0.75;
                Console.WriteLine($"Precio con descuento VIP: ${precioFinal:F2}");
            }
            
            if (precioFinal > 500)
                Console.WriteLine("Compra de alto valor");
            else
                Console.WriteLine("Compra estándar");
        }
    }
}
