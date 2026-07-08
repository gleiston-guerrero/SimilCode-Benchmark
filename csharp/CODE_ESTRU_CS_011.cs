using System;

namespace CalculadoraSalarios
{
    class Program
    {
        static void Main(string[] args)
        {
            Console.WriteLine("=== CALCULADORA DE SALARIOS ===");
            Console.WriteLine("1. Empleado base");
            Console.WriteLine("2. Supervisor");
            Console.WriteLine("3. Gerente");
            Console.Write("Seleccione tipo: ");
            int opcion = Convert.ToInt32(Console.ReadLine());
            
            double salario = 0;
            
            if (opcion == 1)
            {
                Console.Write("Ingrese horas trabajadas: ");
                double horas = Convert.ToDouble(Console.ReadLine());
                salario = horas * 15.50;
                Console.WriteLine($"Salario empleado base: ${salario:F2}");
            }
            else if (opcion == 2)
            {
                Console.Write("Ingrese horas trabajadas: ");
                double horas = Convert.ToDouble(Console.ReadLine());
                Console.Write("Ingrese bono por supervisión: ");
                double bono = Convert.ToDouble(Console.ReadLine());
                salario = (horas * 22.00) + bono;
                Console.WriteLine($"Salario supervisor: ${salario:F2}");
            }
            else if (opcion == 3)
            {
                Console.Write("Ingrese salario fijo: ");
                double fijo = Convert.ToDouble(Console.ReadLine());
                Console.Write("Ingrese comisión: ");
                double comision = Convert.ToDouble(Console.ReadLine());
                salario = fijo + (comision * 0.05);
                Console.WriteLine($"Salario gerente: ${salario:F2}");
            }
            
            if (salario > 2000)
                Console.WriteLine("Salario alto");
            else
                Console.WriteLine("Salario estándar");
        }
    }
}
