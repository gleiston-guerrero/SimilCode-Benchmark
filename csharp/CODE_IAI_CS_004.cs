using System;
using System.Collections.Generic;
using System.Linq;

namespace AdministracionAlumnos
{
    public class Alumno
    {
        public int Identificador { get; set; }
        public string Nombre { get; set; }
        public string Apellido { get; set; }
        public List<double> Notas { get; set; }
        public string Programa { get; set; }
        
        public Alumno(int id, string nombre, string apellido, string programa)
        {
            Identificador = id;
            Nombre = nombre;
            Apellido = apellido;
            Programa = programa;
            Notas = new List<double>();
        }
        
        public void IngresarNota(double nota)
        {
            if (nota >= 0 && nota <= 5)
            {
                Notas.Add(nota);
            }
        }
        
        public double CalcularPromedio()
        {
            return Notas.Count > 0 ? Notas.Average() : 0;
        }
        
        public string ObtenerCondicion()
        {
            double promedio = CalcularPromedio();
            if (promedio >= 3.5) return "Excelente";
            if (promedio >= 3.0) return "Aprobado";
            return "Reprobado";
        }
        
        public override string ToString()
        {
            return $"{Identificador} - {Nombre} {Apellido} ({Programa}) - Promedio: {CalcularPromedio():F2}";
        }
    }
    
    public class AdministradorAlumnos
    {
        private List<Alumno> alumnos;
        
        public AdministradorAlumnos()
        {
            alumnos = new List<Alumno>();
        }
        
        public void AgregarAlumno(Alumno alumno)
        {
            alumnos.Add(alumno);
        }
        
        public Alumno BuscarAlumno(int id)
        {
            return alumnos.FirstOrDefault(a => a.Identificador == id);
        }
        
        public void ListarTodosLosAlumnos()
        {
            foreach (var alumno in alumnos)
            {
                Console.WriteLine(alumno.ToString());
            }
        }
        
        public List<Alumno> AlumnosConAprobado()
        {
            return alumnos.Where(a => a.CalcularPromedio() >= 3.0).ToList();
        }
    }
    
    class ProgramaPrincipal
    {
        static void Main(string[] args)
        {
            AdministradorAlumnos admin = new AdministradorAlumnos();
            
            // Agregar alumnos de ejemplo
            var alumno1 = new Alumno(1, "Juan", "Pérez", "Ingeniería de Software");
            alumno1.IngresarNota(4.2);
            alumno1.IngresarNota(3.8);
            alumno1.IngresarNota(4.5);
            
            var alumno2 = new Alumno(2, "María", "García", "Ingeniería de Sistemas");
            alumno2.IngresarNota(3.1);
            alumno2.IngresarNota(2.8);
            alumno2.IngresarNota(3.4);
            
            admin.AgregarAlumno(alumno1);
            admin.AgregarAlumno(alumno2);
            
            Console.WriteLine("=== SISTEMA DE GESTIÓN DE ESTUDIANTES ===");
            admin.ListarTodosLosAlumnos();
            
            Console.WriteLine("\n=== ESTUDIANTES APROBADOS ===");
            var aprobados = admin.AlumnosConAprobado();
            foreach (var al in aprobados)
            {
                Console.WriteLine($"{al.Nombre} {al.Apellido} - Estado: {al.ObtenerCondicion()}");
            }
            
            Console.ReadKey();
        }
    }
}
