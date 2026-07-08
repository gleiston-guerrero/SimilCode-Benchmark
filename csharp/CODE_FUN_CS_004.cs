using System;
using System.Collections.Generic;
using System.Linq;

namespace SistemaAcademico
{
    public abstract class Persona
    {
        public int Codigo { get; protected set; }
        public string NombreCompleto { get; protected set; }
        public string Email { get; protected set; }
        
        protected Persona(int codigo, string nombre, string email)
        {
            Codigo = codigo;
            NombreCompleto = nombre;
            Email = email;
        }
        
        public abstract void MostrarInformacion();
    }
    
    public class Alumno : Persona
    {
        public string ProgramaAcademico { get; private set; }
        public Dictionary<string, double> NotasPorMateria { get; private set; }
        
        public Alumno(int codigo, string nombre, string email, string programa) 
            : base(codigo, nombre, email)
        {
            ProgramaAcademico = programa;
            NotasPorMateria = new Dictionary<string, double>();
        }
        
        public void RegistrarNota(string materia, double nota)
        {
            if (nota >= 0.0 && nota <= 5.0)
            {
                NotasPorMateria[materia] = nota;
            }
        }
        
        public double PromedioGeneral => NotasPorMateria.Count > 0 ? NotasPorMateria.Values.Average() : 0.0;
        
        public string EstadoAcademico
        {
            get
            {
                var promedio = PromedioGeneral;
                return promedio >= 4.0 ? "SOBRESALIENTE" : 
                       promedio >= 3.0 ? "SATISFACTORIO" : "INSUFICIENTE";
            }
        }
        
        public override void MostrarInformacion()
        {
            Console.WriteLine($"Alumno: {NombreCompleto} | Código: {Codigo} | Programa: {ProgramaAcademico}");
            Console.WriteLine($"Promedio: {PromedioGeneral:F2} | Estado: {EstadoAcademico}");
        }
    }
    
    public class RegistroAcademico
    {
        private Dictionary<int, Alumno> baseDatos;
        
        public RegistroAcademico()
        {
            baseDatos = new Dictionary<int, Alumno>();
        }
        
        public bool MatricularAlumno(Alumno nuevoAlumno)
        {
            if (!baseDatos.ContainsKey(nuevoAlumno.Codigo))
            {
                baseDatos[nuevoAlumno.Codigo] = nuevoAlumno;
                return true;
            }
            return false;
        }
        
        public Alumno ConsultarAlumno(int codigo) => baseDatos.GetValueOrDefault(codigo);
        
        public IEnumerable<Alumno> ListarAlumnosAprobados() => 
            baseDatos.Values.Where(alumno => alumno.PromedioGeneral >= 3.0);
        
        public void GenerarReporte()
        {
            Console.WriteLine("=== REPORTE ACADÉMICO GENERAL ===");
            foreach (var alumno in baseDatos.Values.OrderByDescending(a => a.PromedioGeneral))
            {
                alumno.MostrarInformacion();
                Console.WriteLine();
            }
        }
    }
    
    class Program
    {
        static void Main(string[] args)
        {
            RegistroAcademico registro = new RegistroAcademico();
            
            var alumno1 = new Alumno(2023001, "Ana Sofia Rodriguez", "ana.rodriguez@universidad.edu", "Ingeniería de Software");
            alumno1.RegistrarNota("Programación I", 4.1);
            alumno1.RegistrarNota("Matemáticas", 3.7);
            alumno1.RegistrarNota("Física", 4.3);
            
            var alumno2 = new Alumno(2023002, "Carlos Mendoza", "carlos.mendoza@universidad.edu", "Ingeniería de Sistemas");
            alumno2.RegistrarNota("Algoritmos", 2.9);
            alumno2.RegistrarNota("Bases de Datos", 3.2);
            alumno2.RegistrarNota("Redes", 2.8);
            
            registro.MatricularAlumno(alumno1);
            registro.MatricularAlumno(alumno2);
            
            Console.WriteLine("🎓 SISTEMA ACADÉMICO UNIVERSITARIO 🎓\n");
            registro.GenerarReporte();
            
            Console.WriteLine("=== ALUMNOS CON RENDIMIENTO SATISFACTORIO ===");
            foreach (var alumno in registro.ListarAlumnosAprobados())
            {
                Console.WriteLine($"✅ {alumno.NombreCompleto} - {alumno.PromedioGeneral:F2}");
            }
            
            Console.ReadKey();
        }
    }
}