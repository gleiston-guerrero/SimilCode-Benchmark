using System;
using System.Collections.Generic;

namespace JuegoAdivinanza
{
    class JuegoNumeros
    {
        static void Main(string[] args)
        {
            Random generador = new Random();
            List<int> intentosRealizados = new List<int>();
            
            int numeroSecreto = generador.Next(1, 101);
            int maxIntentos = 7;
            bool juegoTerminado = false;
            
            Console.WriteLine("🎮 ¡JUEGO DE ADIVINANZA! 🎮");
            Console.WriteLine("He pensado un número entre 1 y 100");
            Console.WriteLine($"Tienes {maxIntentos} intentos para adivinarlo");
            
            while (!juegoTerminado && intentosRealizados.Count < maxIntentos)
            {
                Console.Write($"\nIntento {intentosRealizados.Count + 1}/{maxIntentos}: ");
                
                try
                {
                    int numeroUsuario = int.Parse(Console.ReadLine());
                    
                    if (intentosRealizados.Contains(numeroUsuario))
                    {
                        Console.WriteLine("⚠️  Ya probaste ese número antes!");
                        continue;
                    }
                    
                    intentosRealizados.Add(numeroUsuario);
                    
                    if (numeroUsuario == numeroSecreto)
                    {
                        Console.WriteLine("🎉 ¡FELICIDADES! ¡Adivinaste el número!");
                        Console.WriteLine($"Lo lograste en {intentosRealizados.Count} intentos");
                        juegoTerminado = true;
                    }
                    else if (Math.Abs(numeroUsuario - numeroSecreto) <= 5)
                    {
                        Console.WriteLine("🔥 ¡Muy cerca!");
                        if (numeroUsuario < numeroSecreto)
                            Console.WriteLine("📈 El número es un poco mayor");
                        else
                            Console.WriteLine("📉 El número es un poco menor");
                    }
                    else if (numeroUsuario < numeroSecreto)
                    {
                        Console.WriteLine("📈 El número es mayor");
                    }
                    else
                    {
                        Console.WriteLine("📉 El número es menor");
                    }
                }
                catch
                {
                    Console.WriteLine("❌ Ingresa un número válido");
                }
            }
            
            if (!juegoTerminado)
            {
                Console.WriteLine($"\n💔 Se acabaron los intentos. El número era: {numeroSecreto}");
            }
            
            Console.WriteLine("\nTus intentos fueron:");
            for(int i = 0; i < intentosRealizados.Count; i++)
            {
                Console.WriteLine($"{i + 1}. {intentosRealizados[i]}");
            }
            
            Console.WriteLine("\nPresiona cualquier tecla para salir...");
            Console.ReadKey();
        }
    }
}