using System;
using System.Collections.Generic;

namespace GestionEstudiantes
{
    public class Estudiante
    {
        public string Nombre { get; set; }
        public int Edad { get; set; }
        public double Promedio { get; set; }
        
        public Estudiante(string nombre, int edad, double promedio)
        {
            this.Nombre = nombre;
            this.Edad = edad;
            this.Promedio = promedio;
        }
        
        public void MostrarInformacion()
        {
            Console.WriteLine("Nombre: " + this.Nombre);
            Console.WriteLine("Edad: " + this.Edad);
            Console.WriteLine("Promedio: " + this.Promedio);
        }
        
        public bool EsAprobado()
        {
            if (this.Promedio >= 3.0)
            {
                return true;
            }
            else
            {
                return false;
            }
        }
    }
    
    public class Program
    {
        public static void Main(string[] args)
        {
            List<Estudiante> estudiantes = new List<Estudiante>();
            
            estudiantes.Add(new Estudiante("Juan Pérez", 20, 3.5));
            estudiantes.Add(new Estudiante("María García", 19, 2.8));
            estudiantes.Add(new Estudiante("Carlos López", 21, 4.2));
            
            Console.WriteLine("=== INFORMACIÓN DE ESTUDIANTES ===");
            
            foreach (Estudiante est in estudiantes)
            {
                est.MostrarInformacion();
                
                if (est.EsAprobado())
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
