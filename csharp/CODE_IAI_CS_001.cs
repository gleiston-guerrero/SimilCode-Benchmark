using System;
using System.Collections.Generic;

namespace AdministracionAlumnos
{
    public class Alumno
    {
        public string Nombre { get; set; }
        public int Edad { get; set; }
        public double Calificacion { get; set; }
        
        public Alumno(string nombre, int edad, double calificacion)
        {
            this.Nombre = nombre;
            this.Edad = edad;
            this.Calificacion = calificacion;
        }
        
        public void MostrarDetalles()
        {
            Console.WriteLine("Nombre: " + this.Nombre);
            Console.WriteLine("Edad: " + this.Edad);
            Console.WriteLine("Promedio: " + this.Calificacion);
        }
        
        public bool EstaAprobado()
        {
            return this.Calificacion >= 3.0;
        }
    }
    
    public class Principal
    {
        public static void Main(string[] args)
        {
            List<Alumno> listaAlumnos = new List<Alumno>();
            
            listaAlumnos.Add(new Alumno("Juan Pérez", 20, 3.5));
            listaAlumnos.Add(new Alumno("María García", 19, 2.8));
            listaAlumnos.Add(new Alumno("Carlos López", 21, 4.2));
            
            Console.WriteLine("=== INFORMACIÓN DE ESTUDIANTES ===");
            
            foreach (Alumno alumno in listaAlumnos)
            {
                alumno.MostrarDetalles();
                
                if (alumno.EstaAprobado())
                {
                    Console.WriteLine("Estado: APROBADO");
                }
                else
                {
                    Console.WriteLine("Estado: REPROBADO");
                }
                
                Console.WriteLine("------------------------");
            }
            
            Console.ReadKey();
        }
    }
}
