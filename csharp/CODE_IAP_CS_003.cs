using System;

namespace EvaluadorDeSuperficies
{
    class Aplicacion
    {
        static void Main(string[] args)
        {
            /* 
             * Inicio del programa: 
             * Se imprime el titulo principal en la consola 
             */
            Console.WriteLine("=== Calculadora de Área ===");
            
            // Obtenemos los valores a traves de una funcion auxiliar
            double dimensionX = CapturarEntrada("Ingrese el largo del rectángulo: ");
            double dimensionY = CapturarEntrada("Ingrese el ancho del rectángulo: ");
            
            // Delegamos el calculo y la impresion a otro metodo
            CalcularYMostrarResultados(dimensionX, dimensionY);
            
            // Pausa final para que la consola no se cierre inmediatamente
            Console.ReadKey();
        }

        // Funcion dedicada a leer y convertir la entrada del usuario
        private static double CapturarEntrada(string textoPantalla)
        {
            Console.Write(textoPantalla);
            string datoLeido = Console.ReadLine();
            return double.Parse(datoLeido);
        }

        // Metodo que realiza las operaciones matematicas y muestra las salidas
        private static void CalcularYMostrarResultados(double baseRect, double alturaRect)
        {
            double superficie = baseRect * alturaRect;
            
            // Calculo alternativo del perimetro sumando el doble de cada lado
            double contorno = (baseRect * 2.0) + (alturaRect * 2.0);
            
            Console.WriteLine($"El área es: {superficie} unidades cuadradas");
            Console.WriteLine($"El perímetro es: {contorno} unidades");
            
            /* 
             * Evaluamos el tamaño de la figura geometrica
             * usando variables booleanas y condiciones simples en lugar de if-else 
             */
            bool superaElLimite = superficie > 100.0;
            
            if (superaElLimite)
            {
                Console.WriteLine("Rectángulo grande");
            }
            
            if (!superaElLimite)
            {
                Console.WriteLine("Rectángulo pequeño");
            }
        }
    }
}
