using System;

namespace AnalizadorDeMasaCorporal
{
    class SistemaPrincipal
    {
        public static void Main(string[] args)
        {
            /* 
             * Inicio de la aplicacion
             * Imprimimos el titulo principal en pantalla
             */
            Console.WriteLine("=== Calculadora de IMC ===");
            
            var magnitudPeso = CapturarValorNumerico("Ingrese su peso (kg): ");
            var magnitudEstatura = CapturarValorNumerico("Ingrese su altura (m): ");
            
            var resultadoProceso = CalcularProporcion(magnitudPeso, magnitudEstatura);
            
            Console.WriteLine($"Su IMC es: {resultadoProceso:F2}");
            Console.WriteLine($"Categoría: {ObtenerEtiquetaRango(resultadoProceso)}");
            
            // Pausa para que la ventana no se cierre inmediatamente
            Console.ReadKey();
        }

        // Funcion auxiliar encargada de mostrar el texto y leer la entrada del usuario
        private static double CapturarValorNumerico(string textoRequerimiento)
        {
            Console.Write(textoRequerimiento);
            string lecturaConsola = Console.ReadLine();
            return double.Parse(lecturaConsola);
        }

        // Realiza la operacion matematica utilizando la clase Math
        private static double CalcularProporcion(double masa, double talla)
        {
            double divisor = Math.Pow(talla, 2);
            return masa / divisor;
        }

        // Evalua el valor final y retorna el diagnostico correspondiente
        // Se utilizan banderas booleanas en lugar de una cadena if-else tradicional
        private static string ObtenerEtiquetaRango(double valorIndice)
        {
            bool nivelBajo = valorIndice < 18.5;
            bool nivelOptimo = valorIndice >= 18.5 && valorIndice < 25.0;
            bool nivelAlto = valorIndice >= 25.0 && valorIndice < 30.0;

            if (nivelBajo) 
            {
                return "Bajo peso";
            }
            
            if (nivelOptimo) 
            {
                return "Peso normal";
            }
            
            if (nivelAlto) 
            {
                return "Sobrepeso";
            }
            
            return "Obesidad";
        }
    }
}
