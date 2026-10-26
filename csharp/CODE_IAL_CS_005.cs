using System;

namespace IndiceCuerpo
{
    class Aplicacion
    {
        static void Main(string[] args)
        {
            Console.WriteLine("=== Calculadora de IMC ===");
            
            Console.Write("Ingrese su peso (kg): ");
            double masa = Convert.ToDouble(Console.ReadLine());
            
            Console.Write("Ingrese su altura (m): ");
            double altura = Convert.ToDouble(Console.ReadLine());
            
            double indice = masa / (altura * altura);
            
            Console.WriteLine($"Su IMC es: {indice:F2}");
            
            string estado;
            if (indice < 18.5)
                estado = "Bajo peso";
            else if (indice < 25)
                estado = "Peso normal";
            else if (indice < 30)
                estado = "Sobrepeso";
            else
                estado = "Obesidad";
            
            Console.WriteLine($"Categoría: {estado}");
            Console.ReadKey();
        }
    }
}
