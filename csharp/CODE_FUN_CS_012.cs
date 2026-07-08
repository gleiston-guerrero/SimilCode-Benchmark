using System;
using System.Linq;

namespace GestionStock
{
    public class ControladorInventario
    {
        private string[] nombresArticulos;
        private int[] stockArticulos;
        private const int CANTIDAD_PRODUCTOS = 3;
        
        static void Main(string[] args)
        {
            var controlador = new ControladorInventario();
            controlador.GestionarInventario();
        }
        
        public void GestionarInventario()
        {
            Console.WriteLine("=== GESTIÓN DE STOCK ===");
            InicializarArrays();
            CapturarInformacion();
            GenerarReporte();
            EvaluarEstadoGeneral();
        }
        
        private void InicializarArrays()
        {
            nombresArticulos = new string[CANTIDAD_PRODUCTOS];
            stockArticulos = new int[CANTIDAD_PRODUCTOS];
        }
        
        private void CapturarInformacion()
        {
            for (int indice = 0; indice < CANTIDAD_PRODUCTOS; indice++)
            {
                Console.Write($"Artículo {indice + 1}: ");
                nombresArticulos[indice] = Console.ReadLine();
                
                Console.Write($"Stock de {nombresArticulos[indice]}: ");
                stockArticulos[indice] = int.Parse(Console.ReadLine());
            }
        }
        
        private void GenerarReporte()
        {
            Console.WriteLine("\n=== REPORTE DE STOCK ===");
            for (int i = 0; i < CANTIDAD_PRODUCTOS; i++)
            {
                Console.WriteLine($"{nombresArticulos[i]}: {stockArticulos[i]} unidades");
                MostrarEstadoStock(stockArticulos[i]);
            }
            
            int sumaTotal = stockArticulos.Sum();
            Console.WriteLine($"\nTotal de artículos en stock: {sumaTotal}");
        }
        
        private void MostrarEstadoStock(int cantidad)
        {
            string estado = cantidad switch
            {
                < 10 => "  ⚠️ Stock bajo",
                > 50 => "  ✅ Stock alto",
                _ => "  ➡️ Stock normal"
            };
            Console.WriteLine(estado);
        }
        
        private void EvaluarEstadoGeneral()
        {
            int totalUnidades = stockArticulos.Sum();
            string mensaje = totalUnidades < 50 ? 
                "Inventario necesita reposición" : 
                "Inventario en buen estado";
            Console.WriteLine(mensaje);
        }
    }
}