using System;
using System.Collections.Generic;
using System.Linq;

namespace GestionEstudiantes
{
    public class Estudiante
    {
        public int Id { get; set; }
        public string Nombre { get; set; }
        public string Apellido { get; set; }
        public List<double> Calificaciones { get; set; }
        public string Carrera { get; set; }
        
        public Estudiante(int id, string nombre, string apellido, string carrera)
        {
            Id = id;
            Nombre = nombre;
            Apellido = apellido;
            Carrera = carrera;
            Calificaciones = new List<double>();
        }
        
        public void AgregarCalificacion(double calificacion)
        {
            if (calificacion >= 0 && calificacion <= 5)
            {
                Calificaciones.Add(calificacion);
            }
        }
        
        public double CalcularPromedio()
        {
            return Calificaciones.Count > 0 ? Calificaciones.Average() : 0;
        }
        
        public string ObtenerEstado()
        {
            double promedio = CalcularPromedio();
            if (promedio >= 3.5) return "Excelente";
            if (promedio >= 3.0) return "Aprobado";
            return "Reprobado";
        }
        
        public override string ToString()
        {
            return $"{Id} - {Nombre} {Apellido} ({Carrera}) - Promedio: {CalcularPromedio():F2}";
        }
    }
    
    public class GestorEstudiantes
    {
        private List<Estudiante> estudiantes;
        
        public GestorEstudiantes()
        {
            estudiantes = new List<Estudiante>();
        }
        
        public void AgregarEstudiante(Estudiante estudiante)
        {
            estudiantes.Add(estudiante);
        }
        
        public Estudiante BuscarEstudiante(int id)
        {
            return estudiantes.FirstOrDefault(e => e.Id == id);
        }
        
        public void MostrarTodosLosEstudiantes()
        {
            foreach (var estudiante in estudiantes)
            {
                Console.WriteLine(estudiante.ToString());
            }
        }
        
        public List<Estudiante> EstudiantesAprobados()
        {
            return estudiantes.Where(e => e.CalcularPromedio() >= 3.0).ToList();
        }
    }
    
    class Program
    {
        static void Main(string[] args)
        {
            GestorEstudiantes gestor = new GestorEstudiantes();
            
            // Agregar estudiantes de ejemplo
            var estudiante1 = new Estudiante(1, "Juan", "Pérez", "Ingeniería de Software");
            estudiante1.AgregarCalificacion(4.2);
            estudiante1.AgregarCalificacion(3.8);
            estudiante1.AgregarCalificacion(4.5);
            
            var estudiante2 = new Estudiante(2, "María", "García", "Ingeniería de Sistemas");
            estudiante2.AgregarCalificacion(3.1);
            estudiante2.AgregarCalificacion(2.8);
            estudiante2.AgregarCalificacion(3.4);
            
            gestor.AgregarEstudiante(estudiante1);
            gestor.AgregarEstudiante(estudiante2);
            
            Console.WriteLine("=== SISTEMA DE GESTIÓN DE ESTUDIANTES ===");
            gestor.MostrarTodosLosEstudiantes();
            
            Console.WriteLine("\n=== ESTUDIANTES APROBADOS ===");
            var aprobados = gestor.EstudiantesAprobados();
            foreach (var est in aprobados)
            {
                Console.WriteLine($"{est.Nombre} {est.Apellido} - Estado: {est.ObtenerEstado()}");
            }
            
            Console.ReadKey();
        }
    }
}