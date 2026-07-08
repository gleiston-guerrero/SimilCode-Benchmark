using System;

namespace EvaluadorIMC
{
    class AnalizadorSalud
    {
        static void Main(string[] args)
        {
            Console.WriteLine("=== Evaluador de Índice de Masa Corporal ===");
            
            var datos = ObtenerDatosPersona();
            double indiceMasaCorporal = CalcularIMC(datos.peso, datos.altura);
            string clasificacion = DeterminarCategoria(indiceMasaCorporal);
            
            MostrarResultados(indiceMasaCorporal, clasificacion);
            Console.ReadKey();
        }
        
        static (double peso, double altura) ObtenerDatosPersona()
        {
            Console.Write("Digite su peso corporal (kg): ");
            double p = double.Parse(Console.ReadLine());
            
            Console.Write("Digite su estatura (metros): ");
            double a = double.Parse(Console.ReadLine());
            
            return (p, a);
        }
        
        static double CalcularIMC(double peso, double altura)
        {
            return peso / Math.Pow(altura, 2);
        }
        
        static string DeterminarCategoria(double imc)
        {
            return imc switch
            {
                < 18.5 => "Insuficiencia ponderal",
                < 25.0 => "Rango normal",
                < 30.0 => "Exceso de peso",
                _ => "Obesidad"
            };
        }
        
        static void MostrarResultados(double imc, string categoria)
        {
            Console.WriteLine($"Índice de Masa Corporal: {imc:F2}");
            Console.WriteLine($"Estado nutricional: {categoria}");
        }
    }
}
