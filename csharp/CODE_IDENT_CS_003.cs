using System;

namespace CalculadoraArea
{
    class Program
    {
        static void Main(string[] args)
        {
            Console.WriteLine("=== Calculadora de Área ===");
            double largo, ancho;
            
            Console.Write("Ingrese el largo del rectángulo: ");
            largo = Convert.ToDouble(Console.ReadLine());
            
            Console.Write("Ingrese el ancho del rectángulo: ");
            ancho = Convert.ToDouble(Console.ReadLine());
            
            double area = largo * ancho;
            double perimetro = 2 * (largo + ancho);
            
            Console.WriteLine($"El área es: {area} unidades cuadradas");
            Console.WriteLine($"El perímetro es: {perimetro} unidades");
            
            if (area > 100)
            {
                Console.WriteLine("Rectángulo grande");
            }
            else
            {
                Console.WriteLine("Rectángulo pequeño");
            }
            
            Console.ReadKey();
        }
    }
}