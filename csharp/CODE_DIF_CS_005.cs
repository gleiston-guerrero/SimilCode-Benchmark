using System;
using System.Collections.Generic;
using System.Linq;

namespace SistemaRecomendaciones
{
    class RecomendadorPeliculas
    {
        static List<string> peliculasAccion = new List<string> 
        { "Avengers", "Matrix", "John Wick", "Fast & Furious", "Mission Impossible" };
        
        static List<string> peliculasComedia = new List<string> 
        { "Deadpool", "Superbad", "The Hangover", "Anchorman", "Step Brothers" };
        
        static List<string> peliculasDrama = new List<string> 
        { "The Shawshank Redemption", "Forrest Gump", "Titanic", "The Godfather", "Casablanca" };
        
        static Random random = new Random();
        
        static void Main(string[] args)
        {
            Console.WriteLine("🎬 SISTEMA INTELIGENTE DE RECOMENDACIONES 🎬");
            
            bool continuar = true;
            List<string> historialVisto = new List<string>();
            
            while (continuar)
            {
                MostrarMenu();
                string opcion = Console.ReadLine();
                
                switch (opcion)
                {
                    case "1":
                        RecomendarPelicula("Acción", peliculasAccion, historialVisto);
                        break;
                    case "2":
                        RecomendarPelicula("Comedia", peliculasComedia, historialVisto);
                        break;
                    case "3":
                        RecomendarPelicula("Drama", peliculasDrama, historialVisto);
                        break;
                    case "4":
                        MostrarHistorial(historialVisto);
                        break;
                    case "5":
                        LimpiarHistorial(historialVisto);
                        break;
                    case "6":
                        continuar = false;
                        Console.WriteLine("¡Gracias por usar nuestro sistema!");
                        break;
                    default:
                        Console.WriteLine("Opción no válida");
                        break;
                }
                
                if (continuar)
                {
                    Console.WriteLine("\nPresiona Enter para continuar...");
                    Console.ReadLine();
                    Console.Clear();
                }
            }
        }
        
        static void MostrarMenu()
        {
            Console.WriteLine("\n=== ¿QUÉ TE APETECE VER HOY? ===");
            Console.WriteLine("1. 🎯 Películas de Acción");
            Console.WriteLine("2. 😂 Películas de Comedia");
            Console.WriteLine("3. 🎭 Películas de Drama");
            Console.WriteLine("4. 📋 Ver mi historial");
            Console.WriteLine("5. 🗑️ Limpiar historial");
            Console.WriteLine("6. 🚪 Salir");
            Console.Write("\nSelecciona una opción: ");
        }
        
        static void RecomendarPelicula(string genero, List<string> listaPeliculas, List<string> historial)
        {
            var peliculasDisponibles = listaPeliculas.Where(p => !historial.Contains(p)).ToList();
            
            if (peliculasDisponibles.Count == 0)
            {
                Console.WriteLine($"¡Ya has visto todas las películas de {genero}!");
                return;
            }
            
            string peliculaRecomendada = peliculasDisponibles[random.Next(peliculasDisponibles.Count)];
            historial.Add(peliculaRecomendada);
            
            Console.WriteLine($"\n🎬 Te recomendamos: '{peliculaRecomendada}' ({genero})");
            Console.WriteLine($"📊 Películas vistas: {historial.Count}");
        }
        
        static void MostrarHistorial(List<string> historial)
        {
            Console.WriteLine("\n=== TU HISTORIAL DE PELÍCULAS ===");
            if (historial.Count == 0)
            {
                Console.WriteLine("No has visto ninguna película aún.");
            }
            else
            {
                for (int i = 0; i < historial.Count; i++)
                {
                    Console.WriteLine($"{i + 1}. {historial[i]}");
                }
            }
        }
        
        static void LimpiarHistorial(List<string> historial)
        {
            historial.Clear();
            Console.WriteLine("✅ Historial limpiado correctamente.");
        }
    }
}