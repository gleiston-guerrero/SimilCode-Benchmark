using System;

namespace GeometriaCalculator
{
    public class CalculadorGeometrica
    {
        private const double PI = Math.PI;
        
        static void Main(string[] args)
        {
            var calculadora = new CalculadorGeometrica();
            calculadora.EjecutarPrograma();
        }
        
        public void EjecutarPrograma()
        {
            MostrarMenu();
            int seleccion = ObtenerSeleccion();
            double resultado = ProcesarCalculo(seleccion);
            ClasificarTamano(resultado);
        }
        
        private void MostrarMenu()
        {
            Console.WriteLine("=== CALCULADOR GEOMÉTRICO ===");
            string[] opciones = { "Círculo", "Rectángulo", "Triángulo" };
            for (int i = 0; i < opciones.Length; i++)
            {
                Console.WriteLine($"{i + 1}. {opciones[i]}");
            }
            Console.Write("Seleccione figura: ");
        }
        
        private int ObtenerSeleccion()
        {
            return int.Parse(Console.ReadLine());
        }
        
        private double ProcesarCalculo(int tipo)
        {
            return tipo switch
            {
                1 => CalcularCirculo(),
                2 => CalcularRectangulo(),
                3 => CalcularTriangulo(),
                _ => 0
            };
        }
        
        private double CalcularCirculo()
        {
            Console.Write("Ingrese radio: ");
            double r = double.Parse(Console.ReadLine());
            double superficie = PI * Math.Pow(r, 2);
            Console.WriteLine($"Área del círculo: {superficie:F2}");
            return superficie;
        }
        
        private double CalcularRectangulo()
        {
            Console.Write("Ingrese base: ");
            double b = double.Parse(Console.ReadLine());
            Console.Write("Ingrese altura: ");
            double h = double.Parse(Console.ReadLine());
            double superficie = b * h;
            Console.WriteLine($"Área del rectángulo: {superficie:F2}");
            return superficie;
        }
        
        private double CalcularTriangulo()
        {
            Console.Write("Ingrese base: ");
            double b = double.Parse(Console.ReadLine());
            Console.Write("Ingrese altura: ");
            double h = double.Parse(Console.ReadLine());
            double superficie = (b * h) / 2.0;
            Console.WriteLine($"Área del triángulo: {superficie:F2}");
            return superficie;
        }
        
        private void ClasificarTamano(double valor)
        {
            string clasificacion = valor > 100 ? "Figura de área grande" : "Figura de área pequeña";
            Console.WriteLine(clasificacion);
        }
    }
}