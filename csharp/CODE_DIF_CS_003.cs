using System;
using System.Collections.Generic;

namespace BibliotecaDigital
{
    class SistemaBiblioteca
    {
        static List<string> librosDisponibles = new List<string>();
        static List<string> librosPrestados = new List<string>();
        
        static void Main(string[] args)
        {
            InicializarBiblioteca();
            bool sistemaActivo = true;
            
            Console.WriteLine("📚 SISTEMA DE BIBLIOTECA DIGITAL 📚");
            
            while (sistemaActivo)
            {
                MostrarMenu();
                
                try
                {
                    int opcion = int.Parse(Console.ReadLine());
                    
                    switch (opcion)
                    {
                        case 1:
                            MostrarLibrosDisponibles();
                            break;
                        case 2:
                            PrestarLibro();
                            break;
                        case 3:
                            DevolverLibro();
                            break;
                        case 4:
                            AgregarNuevoLibro();
                            break;
                        case 5:
                            MostrarEstadisticas();
                            break;
                        case 6:
                            sistemaActivo = false;
                            Console.WriteLine("👋 ¡Gracias por usar nuestro sistema!");
                            break;
                        default:
                            Console.WriteLine("❌ Opción no válida");
                            break;
                    }
                }
                catch (Exception)
                {
                    Console.WriteLine("❌ Por favor ingresa un número válido");
                }
                
                if (sistemaActivo)
                {
                    Console.WriteLine("\nPresiona Enter para continuar...");
                    Console.ReadLine();
                    Console.Clear();
                }
            }
        }
        
        static void InicializarBiblioteca()
        {
            librosDisponibles.Add("Cien Años de Soledad");
            librosDisponibles.Add("Don Quijote de la Mancha");
            librosDisponibles.Add("El Principito");
            librosDisponibles.Add("1984");
            librosDisponibles.Add("Programación en C#");
        }
        
        static void MostrarMenu()
        {
            Console.WriteLine("\n=== MENÚ PRINCIPAL ===");
            Console.WriteLine("1. Ver libros disponibles");
            Console.WriteLine("2. Prestar libro");
            Console.WriteLine("3. Devolver libro");
            Console.WriteLine("4. Agregar nuevo libro");
            Console.WriteLine("5. Ver estadísticas");
            Console.WriteLine("6. Salir del sistema");
            Console.Write("\nSelecciona una opción: ");
        }
        
        static void MostrarLibrosDisponibles()
        {
            Console.WriteLine("\n📖 LIBROS DISPONIBLES:");
            if (librosDisponibles.Count == 0)
            {
                Console.WriteLine("No hay libros disponibles actualmente");
            }
            else
            {
                for (int i = 0; i < librosDisponibles.Count; i++)
                {
                    Console.WriteLine($"{i + 1}. {librosDisponibles[i]}");
                }
            }
        }
        
        static void PrestarLibro()
        {
            if (librosDisponibles.Count == 0)
            {
                Console.WriteLine("❌ No hay libros disponibles para préstamo");
                return;
            }
            
            MostrarLibrosDisponibles();
            Console.Write("\nIngresa el número del libro a prestar: ");
            
            try
            {
                int indice = int.Parse(Console.ReadLine()) - 1;
                
                if (indice >= 0 && indice < librosDisponibles.Count)
                {
                    string libroSeleccionado = librosDisponibles[indice];
                    librosDisponibles.RemoveAt(indice);
                    librosPrestados.Add(libroSeleccionado);
                    Console.WriteLine($"✅ Libro '{libroSeleccionado}' prestado exitosamente");
                }
                else
                {
                    Console.WriteLine("❌ Número de libro no válido");
                }
            }
            catch
            {
                Console.WriteLine("❌ Ingresa un número válido");
            }
        }
        
        static void DevolverLibro()
        {
            if (librosPrestados.Count == 0)
            {
                Console.WriteLine("❌ No hay libros prestados para devolver");
                return;
            }
            
            Console.WriteLine("\n📚 LIBROS PRESTADOS:");
            for (int i = 0; i < librosPrestados.Count; i++)
            {
                Console.WriteLine($"{i + 1}. {librosPrestados[i]}");
            }
            
            Console.Write("\nIngresa el número del libro a devolver: ");
            
            try
            {
                int indice = int.Parse(Console.ReadLine()) - 1;
                
                if (indice >= 0 && indice < librosPrestados.Count)
                {
                    string libroDevuelto = librosPrestados[indice];
                    librosPrestados.RemoveAt(indice);
                    librosDisponibles.Add(libroDevuelto);
                    Console.WriteLine($"✅ Libro '{libroDevuelto}' devuelto exitosamente");
                }
                else
                {
                    Console.WriteLine("❌ Número de libro no válido");
                }
            }
            catch
            {
                Console.WriteLine("❌ Ingresa un número válido");
            }
        }
        
        static void AgregarNuevoLibro()
        {
            Console.Write("Ingresa el título del nuevo libro: ");
            string nuevoLibro = Console.ReadLine();
            
            if (!string.IsNullOrWhiteSpace(nuevoLibro))
            {
                librosDisponibles.Add(nuevoLibro);
                Console.WriteLine($"✅ Libro '{nuevoLibro}' agregado a la biblioteca");
            }
            else
            {
                Console.WriteLine("❌ El título no puede estar vacío");
            }
        }
        
        static void MostrarEstadisticas()
        {
            Console.WriteLine("\n📊 ESTADÍSTICAS DE LA BIBLIOTECA:");
            Console.WriteLine($"📖 Libros disponibles: {librosDisponibles.Count}");
            Console.WriteLine($"📚 Libros prestados: {librosPrestados.Count}");
            Console.WriteLine($"📋 Total de libros: {librosDisponibles.Count + librosPrestados.Count}");
            
            double porcentajePrestado = librosPrestados.Count > 0 ? 
                (double)librosPrestados.Count / (librosDisponibles.Count + librosPrestados.Count) * 100 : 0;
            Console.WriteLine($"📈 Porcentaje de préstamos: {porcentajePrestado:F1}%");
        }
    }
}