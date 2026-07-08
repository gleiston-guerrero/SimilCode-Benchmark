using System;
using System.Collections.Generic;
using System.Linq;

namespace BibliotecaDigital
{
    public abstract class ItemBiblioteca
    {
        public string Titulo { get; set; }
        public string Autor { get; set; }
        public bool Disponible { get; set; } = true;
        
        public abstract void MostrarInfo();
    }
    
    public class Libro : ItemBiblioteca
    {
        public int Paginas { get; set; }
        
        public override void MostrarInfo()
        {
            Console.WriteLine($"Libro: {Titulo} - {Autor} ({Paginas} páginas) - {(Disponible ? "Disponible" : "Prestado")}");
        }
    }
    
    public class BibliotecaManager
    {
        private Dictionary<int, ItemBiblioteca> catalogo = new Dictionary<int, ItemBiblioteca>();
        private int nextId = 1;
        
        public void AgregarItem(ItemBiblioteca item)
        {
            catalogo[nextId++] = item;
        }
        
        public void MostrarCatalogo()
        {
            Console.WriteLine("\n=== CATÁLOGO COMPLETO ===");
            foreach (var kvp in catalogo)
            {
                Console.Write($"ID {kvp.Key}: ");
                kvp.Value.MostrarInfo();
            }
        }
        
        public bool PrestarItem(int id)
        {
            if (catalogo.ContainsKey(id) && catalogo[id].Disponible)
            {
                catalogo[id].Disponible = false;
                return true;
            }
            return false;
        }
    }
    
    class Program
    {
        static void Main(string[] args)
        {
            var biblioteca = new BibliotecaManager();
            bool continuar = true;
            
            // Datos iniciales
            biblioteca.AgregarItem(new Libro { Titulo = "Clean Code", Autor = "Robert Martin", Paginas = 464 });
            biblioteca.AgregarItem(new Libro { Titulo = "Design Patterns", Autor = "Gang of Four", Paginas = 395 });
            
            while (continuar)
            {
                Console.WriteLine("\n=== BIBLIOTECA DIGITAL ===");
                Console.WriteLine("1. Ver catálogo");
                Console.WriteLine("2. Prestar libro");
                Console.WriteLine("3. Agregar libro");
                Console.WriteLine("4. Salir");
                Console.Write("Opción: ");
                
                switch (Console.ReadLine())
                {
                    case "1":
                        biblioteca.MostrarCatalogo();
                        break;
                    case "2":
                        Console.Write("ID del libro a prestar: ");
                        if (int.TryParse(Console.ReadLine(), out int id))
                        {
                            if (biblioteca.PrestarItem(id))
                                Console.WriteLine("Libro prestado exitosamente");
                            else
                                Console.WriteLine("No se pudo prestar el libro");
                        }
                        break;
                    case "3":
                        Console.Write("Título: ");
                        string titulo = Console.ReadLine();
                        Console.Write("Autor: ");
                        string autor = Console.ReadLine();
                        Console.Write("Páginas: ");
                        if (int.TryParse(Console.ReadLine(), out int paginas))
                        {
                            biblioteca.AgregarItem(new Libro { Titulo = titulo, Autor = autor, Paginas = paginas });
                            Console.WriteLine("Libro agregado exitosamente");
                        }
                        break;
                    case "4":
                        continuar = false;
                        break;
                    default:
                        Console.WriteLine("Opción no válida");
                        break;
                }
            }
        }
    }
}