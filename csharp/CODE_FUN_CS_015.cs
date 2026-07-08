using System;
using System.Linq;

namespace AnalizadorEstadistico
{
    public class EstadisticasCalculator
    {
        private int[] valores;
        private int totalElementos;
        
        public void EjecutarAnalisis()
        {
            Console.WriteLine("Procesador de Números");
            Console.Write("¿Cuántos números desea procesar? ");
            totalElementos = Convert.ToInt32(Console.ReadLine());
            valores = new int[totalElementos];
            
            CargarDatos();
            MostrarEstadisticas();
        }
        
        private void CargarDatos()
        {
            for (int index = 0; index < totalElementos; index++)
            {
                Console.Write($"Ingrese el número {index + 1}: ");
                valores[index] = Convert.ToInt32(Console.ReadLine());
            }
        }
        
        private void MostrarEstadisticas()
        {
            int sumaTotal = ObtenerSuma();
            double promedioValores = CalcularPromedio();
            int valorMaximo = ObtenerMaximo();
            int valorMinimo = ObtenerMinimo();
            int rangoValores = valorMaximo - valorMinimo;
            
            Console.WriteLine($"\nResultados:");
            Console.WriteLine($"Suma: {sumaTotal}");
            Console.WriteLine($"Promedio: {promedioValores:F2}");
            Console.WriteLine($"Máximo: {valorMaximo}");
            Console.WriteLine($"Mínimo: {valorMinimo}");
            Console.WriteLine($"Rango: {rangoValores}");
            
            MostrarTendencia(promedioValores);
        }
        
        private int ObtenerSuma() => valores.Sum();
        private double CalcularPromedio() => valores.Average();
        private int ObtenerMaximo() => valores.Max();
        private int ObtenerMinimo() => valores.Min();
        
        private void MostrarTendencia(double prom)
        {
            string tendencia = prom > 50 ? "Los números tienden a ser altos" : "Los números tienden a ser bajos";
            Console.WriteLine(tendencia);
        }
    }
    
    class Program
    {
        static void Main()
        {
            EstadisticasCalculator analizador = new EstadisticasCalculator();
            analizador.EjecutarAnalisis();
        }
    }
}