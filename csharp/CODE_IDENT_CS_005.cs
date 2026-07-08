using System;

namespace CalculadoraIMC
{
    class Program
    {
        static void Main(string[] args)
        {
            Console.WriteLine("=== Calculadora de IMC ===");
            
            Console.Write("Ingrese su peso (kg): ");
            double peso = Convert.ToDouble(Console.ReadLine());
            
            Console.Write("Ingrese su altura (m): ");
            double altura = Convert.ToDouble(Console.ReadLine());
            
            double imc = peso / (altura * altura);
            
            Console.WriteLine($"Su IMC es: {imc:F2}");
            
            string categoria;
            if (imc < 18.5)
                categoria = "Bajo peso";
            else if (imc < 25)
                categoria = "Peso normal";
            else if (imc < 30)
                categoria = "Sobrepeso";
            else
                categoria = "Obesidad";
            
            Console.WriteLine($"Categoría: {categoria}");
            Console.ReadKey();
        }
    }
}