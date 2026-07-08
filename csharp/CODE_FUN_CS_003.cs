using System;

namespace GeometriaBasica
{
    class CalculadorGeometrica
    {
        static void Main(string[] args)
        {
            Console.WriteLine("=== Sistema de Cálculos Geométricos ===");
            
            double[] dimensiones = new double[2];
            string[] nombres = {"largo", "ancho"};
            
            for(int i = 0; i < 2; i++)
            {
                Console.Write($"Ingresa el {nombres[i]}: ");
                dimensiones[i] = double.Parse(Console.ReadLine());
            }
            
            double superficieTotal = dimensiones[0] * dimensiones[1];
            double contorno = (dimensiones[0] + dimensiones[1]) * 2;
            
            Console.WriteLine("Superficie calculada: " + superficieTotal.ToString("F2"));
            Console.WriteLine("Contorno calculado: " + contorno.ToString("F2"));
            
            string tamaño = (superficieTotal > 100) ? "GRANDE" : "PEQUEÑO";
            Console.WriteLine("Clasificación: " + tamaño);
                
            Console.ReadKey();
        }
    }
}