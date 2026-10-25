using System;
using System.Collections.Generic;

namespace ControlExistencias
{
    public class RegistroStock
    {
        public string Denominacion { get; set; }
        public int NumeroUnidades { get; set; }

        public RegistroStock(string denominacion, int numeroUnidades)
        {
            Denominacion = denominacion;
            NumeroUnidades = numeroUnidades;
        }
    }

    public class AlmacenApp
    {
        public static void Main()
        {
            List<RegistroStock> listaArticulos = new List<RegistroStock>();

            Console.WriteLine("=== SISTEMA DE INVENTARIO ===");

            int contadorVueltas = 0;
            while (contadorVueltas < 3)
            {
                Console.Write($"Producto {contadorVueltas + 1}: ");
                string nombreLeido = Console.ReadLine();

                Console.Write($"Cantidad de {nombreLeido}: ");
                int cantidadLeida = Convert.ToInt32(Console.ReadLine());

                listaArticulos.Add(new RegistroStock(nombreLeido, cantidadLeida));
                contadorVueltas++;
            }

            int sumaTotal = 0;
            Console.WriteLine("\n=== INVENTARIO ACTUAL ===");

            foreach (RegistroStock itemActual in listaArticulos)
            {
                Console.WriteLine($"{itemActual.Denominacion}: {itemActual.NumeroUnidades} unidades");
                sumaTotal += itemActual.NumeroUnidades;

                if (itemActual.NumeroUnidades < 10)
                {
                    Console.WriteLine("  ⚠️ Stock bajo");
                }
                else if (itemActual.NumeroUnidades > 50)
                {
                    Console.WriteLine("  ✅ Stock alto");
                }
                else
                {
                    Console.WriteLine("  ➡️ Stock normal");
                }
            }

            Console.WriteLine($"\nTotal de artículos en inventario: {sumaTotal}");

            if (sumaTotal < 50)
            {
                Console.WriteLine("Inventario necesita reposición");
            }
            else
            {
                Console.WriteLine("Inventario en buen estado");
            }
        }
    }
}
