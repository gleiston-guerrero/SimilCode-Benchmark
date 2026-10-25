using System;
using System.Collections.Generic;

namespace EvaluadorDeSuperficies
{
    class Principal
    {
        // Punto de entrada de la aplicación
        static void Main(string[] args)
        {
            DesplegarMenu();
            
            int eleccionUsuario = Convert.ToInt32(Console.ReadLine());
            double resultadoFinal = 0.0;

            // Uso de switch en lugar de múltiples if-else
            switch (eleccionUsuario)
            {
                case 1:
                    resultadoFinal = ProcesarCirculo();
                    break;
                case 2:
                    resultadoFinal = ProcesarRectangulo();
                    break;
                case 3:
                    resultadoFinal = ProcesarTriangulo();
                    break;
            }

            DeterminarMagnitud(resultadoFinal);
        }

        /// <summary>
        /// Muestra las opciones disponibles utilizando una lista y un bucle.
        /// </summary>
        private static void DesplegarMenu()
        {
            List<string> elementosMenu = new List<string>
            {
                "=== CALCULADORA DE ÁREAS ===",
                "1. Círculo",
                "2. Rectángulo",
                "3. Triángulo"
            };

            foreach (string item in elementosMenu)
            {
                Console.WriteLine(item);
            }
            
            Console.Write("Seleccione figura: ");
        }

        private static double ProcesarCirculo()
        {
            Console.Write("Ingrese radio: ");
            double medidaR = Convert.ToDouble(Console.ReadLine());
            
            // Cálculo del área circular
            double valorSuperficie = 3.14159 * medidaR * medidaR;
            Console.WriteLine($"Área del círculo: {valorSuperficie:F2}");
            
            return valorSuperficie;
        }

        private static double ProcesarRectangulo()
        {
            double ancho = ObtenerDato("Ingrese base: ");
            double alto = ObtenerDato("Ingrese altura: ");
            
            double valorSuperficie = ancho * alto;
            Console.WriteLine($"Área del rectángulo: {valorSuperficie:F2}");
            
            return valorSuperficie;
        }

        private static double ProcesarTriangulo()
        {
            double baseFig = ObtenerDato("Ingrese base: ");
            double alturaFig = ObtenerDato("Ingrese altura: ");
            
            double valorSuperficie = (baseFig * alturaFig) / 2.0;
            Console.WriteLine($"Área del triángulo: {valorSuperficie:F2}");
            
            return valorSuperficie;
        }

        // Método auxiliar para no repetir la lógica de pedir datos por consola
        private static double ObtenerDato(string mensajePantalla)
        {
            Console.Write(mensajePantalla);
            string lectura = Console.ReadLine();
            return Convert.ToDouble(lectura);
        }

        private static void DeterminarMagnitud(double tamañoCalculado)
        {
            // Se reemplaza el if tradicional por un operador ternario
            string textoSalida = (tamañoCalculado > 100) 
                ? "Figura de área grande" 
                : "Figura de área pequeña";
                
            Console.WriteLine(textoSalida);
        }
    }
}
