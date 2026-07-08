using System;

namespace SistemaPayroll
{
    class CalculadoraSalario
    {
        static void Main(string[] args)
        {
            Console.WriteLine("=== Calculadora de Salario Mensual ===");
            
            int horasNormales, horasExtra, horasNocturnas;
            
            Console.Write("Horas normales trabajadas: ");
            horasNormales = int.Parse(Console.ReadLine());
            
            Console.Write("Horas extra trabajadas: ");
            horasExtra = int.Parse(Console.ReadLine());
            
            Console.Write("Horas nocturnas trabajadas: ");
            horasNocturnas = int.Parse(Console.ReadLine());
            
            double salarioBase = horasNormales * 15000;
            double pagoExtra = horasExtra * 22500;
            double pagoNocturno = horasNocturnas * 18000;
            double salarioTotal = salarioBase + pagoExtra + pagoNocturno;
            
            Console.WriteLine($"Salario total: ${salarioTotal:N0} COP");
            
            if (salarioTotal >= 2000000)
            {
                Console.WriteLine("Salario alto - Descuento tributario");
            }
            else if (salarioTotal >= 1200000)
            {
                Console.WriteLine("Salario medio - Revisión fiscal");
            }
            else
            {
                Console.WriteLine("Salario básico - Sin descuentos");
            }
            
            Console.ReadKey();
        }
    }
}