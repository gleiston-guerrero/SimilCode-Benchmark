using System;

namespace AnalisisTermico
{
    internal static class AplicacionTermometro
    {
        private static double[] RecopilarTemperaturas(int totalRegistros)
        {
            double[] datos = new double[totalRegistros];
            int contador = 0;

            while (contador < totalRegistros)
            {
                Console.Write("Temperatura " + (contador + 1) + " (°C): ");
                datos[contador] = Convert.ToDouble(Console.ReadLine());
                contador = contador + 1;
            }

            return datos;
        }

        private static void ImprimirClasificacion(double valor)
        {
            Console.Write(valor + "°C ");

            if (valor > 30)
            {
                Console.WriteLine("- CALOR");
            }
            else if (valor < 15)
            {
                Console.WriteLine("- FRÍO");
            }
            else
            {
                Console.WriteLine("- NORMAL");
            }
        }

        private static void ProcesarTemperaturas(double[] datos)
        {
            double acumulador = 0;
            double maxima = datos[0];
            double minima = datos[0];

            for (int posicion = 0; posicion < datos.Length; posicion++)
            {
                double valorActual = datos[posicion];
                acumulador = acumulador + valorActual;

                if (valorActual > maxima) maxima = valorActual;
                if (valorActual < minima) minima = valorActual;

                ImprimirClasificacion(valorActual);
            }

            double media = acumulador / datos.Length;
            Console.WriteLine("\nPromedio: " + media.ToString("F1") + "°C");
            Console.WriteLine("Máxima: " + maxima + "°C");
            Console.WriteLine("Mínima: " + minima + "°C");
        }

        public static void Main(string[] argumentos)
        {
            Console.WriteLine("=== CONTROL DE TEMPERATURA ===");
            Console.Write("¿Cuántas mediciones desea registrar? ");
            var totalRegistros = Convert.ToInt32(Console.ReadLine());

            var registros = RecopilarTemperaturas(totalRegistros);
            ProcesarTemperaturas(registros);
        }
    }
}
