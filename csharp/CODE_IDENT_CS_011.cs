using System;

namespace CalculadoraAreas
{
    class Program
    {
        static void Main(string[] args)
        {
            Console.WriteLine("=== CALCULADORA DE ÁREAS ===");
            Console.WriteLine("1. Círculo");
            Console.WriteLine("2. Rectángulo");
            Console.WriteLine("3. Triángulo");
            Console.Write("Seleccione figura: ");
            int opcion = Convert.ToInt32(Console.ReadLine());
            
            double area = 0;
            
            if (opcion == 1)
            {
                Console.Write("Ingrese radio: ");
                double radio = Convert.ToDouble(Console.ReadLine());
                area = 3.14159 * radio * radio;
                Console.WriteLine($"Área del círculo: {area:F2}");
            }
            else if (opcion == 2)
            {
                Console.Write("Ingrese base: ");
                double baseRect = Convert.ToDouble(Console.ReadLine());
                Console.Write("Ingrese altura: ");
                double altura = Convert.ToDouble(Console.ReadLine());
                area = baseRect * altura;
                Console.WriteLine($"Área del rectángulo: {area:F2}");
            }
            else if (opcion == 3)
            {
                Console.Write("Ingrese base: ");
                double baseTri = Convert.ToDouble(Console.ReadLine());
                Console.Write("Ingrese altura: ");
                double alturaTri = Convert.ToDouble(Console.ReadLine());
                area = (baseTri * alturaTri) / 2;
                Console.WriteLine($"Área del triángulo: {area:F2}");
            }
            
            if (area > 100)
                Console.WriteLine("Figura de área grande");
            else
                Console.WriteLine("Figura de área pequeña");
        }
    }
}
