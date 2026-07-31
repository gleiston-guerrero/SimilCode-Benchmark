using System;

namespace ControlTemperatura
{
    class Program
    {
        static string Clasificar(double valor)
        {
            if (valor > 30)
                return "- CALOR";
            if (valor < 15)
                return "- FRÍO";
            return "- NORMAL";
        }

        static void Main(string[] args)
        {
            Console.WriteLine("=== CONTROL DE TEMPERATURA ===");

            Console.Write("¿Cuántas mediciones desea registrar? ");
            int n = int.Parse(Console.ReadLine());

            double[] lecturas = new double[n];
            for (int k = 0; k < n; k++)
            {
                Console.Write($"Temperatura {k + 1} (°C): ");
                lecturas[k] = double.Parse(Console.ReadLine());
            }

            double acumulado = 0;
            double mayor = lecturas[0];
            double menor = lecturas[0];

            for (int k = 0; k < lecturas.Length; k++)
            {
                double actual = lecturas[k];
                acumulado += actual;
                mayor = Math.Max(mayor, actual);
                menor = Math.Min(menor, actual);

                Console.Write($"{actual}°C ");
                Console.WriteLine(Clasificar(actual));
            }

            double media = acumulado / lecturas.Length;
            Console.WriteLine($"\nPromedio: {media:F1}°C");
            Console.WriteLine($"Máxima: {mayor}°C");
            Console.WriteLine($"Mínima: {menor}°C");
        }
    }
}
