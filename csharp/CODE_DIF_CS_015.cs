using System;
using System.Collections.Generic;
using System.Threading;
using System.Threading.Tasks;

namespace JuegoAdivinaNumero
{
    public class ConfiguracionJuego
    {
        public int NumeroSecreto { get; set; }
        public int IntentosMaximos { get; set; }
        public int PuntuacionInicial { get; set; }
        public string NivelDificultad { get; set; }
    }
    
    public class JuegoAdivinanza
    {
        private Random generador;
        private ConfiguracionJuego config;
        private List<string> historialJugadores;
        private Dictionary<string, int> ranking;
        
        public JuegoAdivinanza()
        {
            generador = new Random();
            historialJugadores = new List<string>();
            ranking = new Dictionary<string, int>();
            InicializarJuego();
        }
        
        private void InicializarJuego()
        {
            Console.WriteLine("🎯 JUEGO: ADIVINA EL NÚMERO 🎯");
            Console.WriteLine("================================");
            
            config = new ConfiguracionJuego();
            ElegirDificultad();
            config.NumeroSecreto = generador.Next(1, GetRangoMaximo() + 1);
        }
        
        private void ElegirDificultad()
        {
            Console.WriteLine("Seleccione dificultad:");
            Console.WriteLine("1. Fácil (1-50, 10 intentos, 1000 puntos)");
            Console.WriteLine("2. Medio (1-100, 7 intentos, 1500 puntos)");
            Console.WriteLine("3. Difícil (1-200, 5 intentos, 2000 puntos)");
            Console.Write("Opción: ");
            
            string opcion = Console.ReadLine();
            switch (opcion)
            {
                case "1":
                    config.NivelDificultad = "Fácil";
                    config.IntentosMaximos = 10;
                    config.PuntuacionInicial = 1000;
                    break;
                case "2":
                    config.NivelDificultad = "Medio";
                    config.IntentosMaximos = 7;
                    config.PuntuacionInicial = 1500;
                    break;
                case "3":
                    config.NivelDificultad = "Difícil";
                    config.IntentosMaximos = 5;
                    config.PuntuacionInicial = 2000;
                    break;
                default:
                    config.NivelDificultad = "Medio";
                    config.IntentosMaximos = 7;
                    config.PuntuacionInicial = 1500;
                    break;
            }
        }
        
        private int GetRangoMaximo()
        {
            return config.NivelDificultad switch
            {
                "Fácil" => 50,
                "Medio" => 100,
                "Difícil" => 200,
                _ => 100
            };
        }
        
        public async Task IniciarPartida()
        {
            Console.Write("Ingrese su nombre: ");
            string nombreJugador = Console.ReadLine();
            historialJugadores.Add(nombreJugador);
            
            Console.WriteLine($"\n¡Hola {nombreJugador}! 👋");
            Console.WriteLine($"Dificultad: {config.NivelDificultad}");
            Console.WriteLine($"Adivina el número entre 1 y {GetRangoMaximo()}");
            Console.WriteLine($"Tienes {config.IntentosMaximos} intentos");
            Console.WriteLine($"Puntuación inicial: {config.PuntuacionInicial} puntos\n");
            
            int intentosUsados = 0;
            int puntuacionActual = config.PuntuacionInicial;
            bool numeroAdivinado = false;
            
            while (intentosUsados < config.IntentosMaximos && !numeroAdivinado)
            {
                await MostrarProgreso(intentosUsados);
                
                Console.Write($"Intento {intentosUsados + 1}/{config.IntentosMaximos}: ");
                
                if (int.TryParse(Console.ReadLine(), out int intento))
                {
                    intentosUsados++;
                    
                    if (intento == config.NumeroSecreto)
                    {
                        numeroAdivinado = true;
                        Console.WriteLine("🎉 ¡CORRECTO! ¡Has ganado!");
                        puntuacionActual = CalcularPuntuacionFinal(intentosUsados);
                        Console.WriteLine($"Puntuación final: {puntuacionActual} puntos");
                        ranking[nombreJugador] = puntuacionActual;
                    }
                    else if (intento < config.NumeroSecreto)
                    {
                        Console.WriteLine("📈 El número es MAYOR");
                        puntuacionActual -= 50;
                    }
                    else
                    {
                        Console.WriteLine("📉 El número es MENOR");
                        puntuacionActual -= 50;
                    }
                    
                    Console.WriteLine($"Puntuación actual: {Math.Max(0, puntuacionActual)} puntos");
                }
                else
                {
                    Console.WriteLine("❌ Ingrese un número válido");
                }
            }
            
            if (!numeroAdivinado)
            {
                Console.WriteLine($"\n💀 ¡Game Over! El número era: {config.NumeroSecreto}");
                ranking[nombreJugador] = 0;
            }
            
            MostrarRanking();
            await PreguntarNuevaPartida();
        }
        
        private async Task MostrarProgreso(int intentos)
        {
            Console.Write("Pensando");
            for (int i = 0; i < 3; i++)
            {
                await Task.Delay(200);
                Console.Write(".");
            }
            Console.WriteLine();
        }
        
        private int CalcularPuntuacionFinal(int intentosUsados)
        {
            double multiplicador = (double)(config.IntentosMaximos - intentosUsados + 1) / config.IntentosMaximos;
            return (int)(config.PuntuacionInicial * multiplicador);
        }
        
        private void MostrarRanking()
        {
            Console.WriteLine("\n🏆 RANKING DE JUGADORES 🏆");
            Console.WriteLine("==========================");
            
            var rankingOrdenado = ranking.OrderByDescending(x => x.Value);
            int posicion = 1;
            
            foreach (var jugador in rankingOrdenado)
            {
                string medalla = posicion switch
                {
                    1 => "🥇",
                    2 => "🥈",
                    3 => "🥉",
                    _ => $"{posicion}."
                };
                
                Console.WriteLine($"{medalla} {jugador.Key}: {jugador.Value} puntos");
                posicion++;
            }
        }
        
        private async Task PreguntarNuevaPartida()
        {
            Console.WriteLine("\n¿Desea jugar otra partida? (s/n): ");
            string respuesta = Console.ReadLine();
            
            if (respuesta?.ToLower() == "s" || respuesta?.ToLower() == "si")
            {
                Console.Clear();
                InicializarJuego();
                await IniciarPartida();
            }
            else
            {
                Console.WriteLine("¡Gracias por jugar! 👋");
                Environment.Exit(0);
            }
        }
    }
    
    class Program
    {
        static async Task Main()
        {
            JuegoAdivinanza juego = new JuegoAdivinanza();
            await juego.IniciarPartida();
        }
    }
}