using System;
using System.Collections.Generic;
using System.Linq;

namespace SistemaBiblioteca
{
    public class Libro
    {
        public string Titulo { get; set; }
        public string Autor { get; set; }
        public bool Disponible { get; set; }
        public DateTime FechaPrestamo { get; set; }
        
        public Libro(string titulo, string autor)
        {
            Titulo = titulo;
            Autor = autor;
            Disponible = true;
        }
    }
    
    public class BibliotecaManager
    {
        private Dictionary<int, Libro> catalogo;
        private Queue<string> solicitudesPendientes;
        
        public BibliotecaManager()
        {
            catalogo = new Dictionary<int, Libro>();
            solicitudesPendientes = new Queue<string>();
            InicializarCatalogo();
        }
        
        private void InicializarCatalogo()
        {
            catalogo.Add(1, new Libro("El Quijote", "Cervantes"));
            catalogo.Add(2, new Libro("Cien años de soledad", "García Márquez"));
            catalogo.Add(3, new Libro("1984", "Orwell"));
        }
        
        public void MostrarMenu()
        {
            bool continuar = true;
            while (continuar)
            {
                Console.Clear();
                Console.WriteLine("=== SISTEMA DE BIBLIOTECA ===");
                Console.WriteLine("1. Ver catálogo");
                Console.WriteLine("2. Prestar libro");
                Console.WriteLine("3. Devolver libro");
                Console.WriteLine("4. Reportes");
                Console.WriteLine("5. Salir");
                Console.Write("Seleccione opción: ");
                
                string opcion = Console.ReadLine();
                
                switch (opcion)
                {
                    case "1":
                        MostrarCatalogo();
                        break;
                    case "2":
                        ProcesarPrestamo();
                        break;
                    case "3":
                        ProcesarDevolucion();
                        break;
                    case "4":
                        GenerarReportes();
                        break;
                    case "5":
                        continuar = false;
                        break;
                    default:
                        Console.WriteLine("Opción inválida");
                        break;
                }
                
                if (continuar)
                {
                    Console.WriteLine("\nPresione cualquier tecla para continuar...");
                    Console.ReadKey();
                }
            }
        }
        
        private void MostrarCatalogo()
        {
            Console.WriteLine("\n=== CATÁLOGO ===");
            foreach (var item in catalogo)
            {
                var libro = item.Value;
                string estado = libro.Disponible ? "Disponible" : $"Prestado desde {libro.FechaPrestamo:dd/MM/yyyy}";
                Console.WriteLine($"{item.Key}. {libro.Titulo} - {libro.Autor} ({estado})");
            }
        }
        
        private void ProcesarPrestamo()
        {
            Console.Write("ID del libro a prestar: ");
            if (int.TryParse(Console.ReadLine(), out int id) && catalogo.ContainsKey(id))
            {
                if (catalogo[id].Disponible)
                {
                    catalogo[id].Disponible = false;
                    catalogo[id].FechaPrestamo = DateTime.Now;
                    Console.WriteLine($"Libro '{catalogo[id].Titulo}' prestado exitosamente");
                }
                else
                {
                    Console.WriteLine("El libro no está disponible");
                }
            }
            else
            {
                Console.WriteLine("ID inválido");
            }
        }
        
        private void ProcesarDevolucion()
        {
            Console.Write("ID del libro a devolver: ");
            if (int.TryParse(Console.ReadLine(), out int id) && catalogo.ContainsKey(id))
            {
                if (!catalogo[id].Disponible)
                {
                    catalogo[id].Disponible = true;
                    TimeSpan diasPrestado = DateTime.Now - catalogo[id].FechaPrestamo;
                    Console.WriteLine($"Libro devuelto. Estuvo prestado {diasPrestado.Days} días");
                }
                else
                {
                    Console.WriteLine("Este libro no estaba prestado");
                }
            }
            else
            {
                Console.WriteLine("ID inválido");
            }
        }
        
        private void GenerarReportes()
        {
            var librosDisponibles = catalogo.Values.Count(l => l.Disponible);
            var librosPrestados = catalogo.Values.Count(l => !l.Disponible);
            var porcentajeDisponibilidad = (double)librosDisponibles / catalogo.Count * 100;
            
            Console.WriteLine("\n=== REPORTES ===");
            Console.WriteLine($"Total de libros: {catalogo.Count}");
            Console.WriteLine($"Libros disponibles: {librosDisponibles}");
            Console.WriteLine($"Libros prestados: {librosPrestados}");
            Console.WriteLine($"Porcentaje de disponibilidad: {porcentajeDisponibilidad:F1}%");
        }
    }
    
    class Program
    {
        static void Main()
        {
            BibliotecaManager biblioteca = new BibliotecaManager();
            biblioteca.MostrarMenu();
        }
    }
}