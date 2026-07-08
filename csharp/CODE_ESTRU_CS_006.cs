using System;

namespace CalculadoraDescuentos
{
    class Program
    {
        static void Main(string[] args)
        {
            Console.WriteLine("=== Calculadora de Descuentos ===");
            
            Console.Write("Ingrese el precio original: $");
            double precio = Convert.ToDouble(Console.ReadLine());
            
            Console.Write("Tipo de cliente (1-Regular, 2-VIP): ");
            int tipoCliente = Convert.ToInt32(Console.ReadLine());
            
            double descuento = 0;
            string categoria = "";
            
            if (tipoCliente == 1)
            {
                descuento = precio * 0.05;  // 5% descuento regular
                categoria = "Cliente Regular";
            }
            else if (tipoCliente == 2)
            {
                descuento = precio * 0.15;  // 15% descuento VIP
                categoria = "Cliente VIP";
            }
            else
            {
                Console.WriteLine("Tipo de cliente inválido");
                Console.ReadKey();
                return;
            }
            
            double precioFinal = precio - descuento;
            Console.WriteLine($"Precio original: ${precio:F2}");
            Console.WriteLine($"Descuento ({categoria}): ${descuento:F2}");
            Console.WriteLine($"Precio final: ${precioFinal:F2}");
            
            if (precioFinal > 500000)
                Console.WriteLine("Compra de alto valor");
            else if (precioFinal < 50000)
                Console.WriteLine("Compra económica");
            else
                Console.WriteLine("Compra estándar");
            
            Console.ReadKey();
        }
    }
}