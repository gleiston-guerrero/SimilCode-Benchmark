using System;
using System.Collections.Generic;

namespace ProcesadorNumeros
{
    class Program
    {
        static void Main()
        {
            List<int> numeros = new List<int>();
            
            Console.WriteLine("Procesador de Números");
            Console.Write("¿Cuántos números desea procesar? ");
            int cantidad = int.Parse(Console.ReadLine());
            
            for (int i = 0; i < cantidad; i++)
            {
                Console.Write($"Ingrese el número {i + 1}: ");
                int numero = int.Parse(Console.ReadLine());
                numeros.Add(numero);
            }
            
            int suma = 0;
            int maximo = numeros[0];
            int minimo = numeros[0];
            
            foreach (int num in numeros)
            {
                suma += num;
                if (num > maximo) maximo = num;
                if (num < minimo) minimo = num;
            }
            
            double promedio = (double)suma / numeros.Count;
            
            Console.WriteLine($"\nResultados:");
            Console.WriteLine($"Suma: {suma}");
            Console.WriteLine($"Promedio: {promedio:F2}");
            Console.WriteLine($"Máximo: {maximo}");
            Console.WriteLine($"Mínimo: {minimo}");
            Console.WriteLine($"Rango: {maximo - minimo}");
            
            if (promedio > 50)
                Console.WriteLine("Los números tienden a ser altos");
            else
                Console.WriteLine("Los números tienden a ser bajos");
        }
    }
}