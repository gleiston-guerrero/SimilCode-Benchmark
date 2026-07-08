using System;

namespace CalculadoraMetabolismo
{
    class Program
    {
        static void Main(string[] args)
        {
            Console.WriteLine("=== Calculadora Metabólica ===");
            
            Console.Write("Ingrese su edad (años): ");
            int edad = Convert.ToInt32(Console.ReadLine());
            
            Console.Write("Ingrese su peso (kg): ");
            double peso = Convert.ToDouble(Console.ReadLine());
            
            Console.Write("Ingrese su altura (cm): ");
            double altura = Convert.ToDouble(Console.ReadLine());
            
            // Fórmula Harris-Benedict simplificada para hombres
            double tmb = 88.362 + (13.397 * peso) + (4.799 * altura) - (5.677 * edad);
            
            Console.WriteLine($"Su TMB es: {tmb:F0} calorías/día");
            
            string nivelActividad;
            if (tmb < 1500)
                nivelActividad = "Metabolismo bajo";
            else if (tmb < 1800)
                nivelActividad = "Metabolismo normal";
            else if (tmb < 2200)
                nivelActividad = "Metabolismo alto";
            else
                nivelActividad = "Metabolismo muy alto";
            
            Console.WriteLine($"Clasificación: {nivelActividad}");
            Console.ReadKey();
        }
    }
}
