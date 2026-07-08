using System;
using System.Collections.Generic;
using System.Linq;

namespace SistemaEstudiantes
{
    public class Student
    {
        private string _nombre;
        private int _edad;
        private double _promedio;
        
        public string Nombre 
        { 
            get => _nombre; 
            set => _nombre = value; 
        }
        
        public int Edad 
        { 
            get => _edad; 
            set => _edad = value; 
        }
        
        public double Promedio 
        { 
            get => _promedio; 
            set => _promedio = value; 
        }
        
        public Student(string name, int age, double average)
        {
            Nombre = name;
            Edad = age;
            Promedio = average;
        }
        
        public void DisplayInfo()
        {
            Console.WriteLine($"Nombre: {Nombre}");
            Console.WriteLine($"Edad: {Edad}");
            Console.WriteLine($"Promedio: {Promedio:F1}");
        }
        
        public bool IsApproved() => Promedio >= 3.0;
    }
    
    class Application
    {
        static void Main()
        {
            var listStudents = new List<Student>
            {
                new Student("Juan Pérez", 20, 3.5),
                new Student("María García", 19, 2.8),
                new Student("Carlos López", 21, 4.2)
            };
            
            Console.WriteLine("=== INFORMACIÓN DE ESTUDIANTES ===");
            
            listStudents.ForEach(student =>
            {
                student.DisplayInfo();
                Console.WriteLine($"Estado: {(student.IsApproved() ? "APROBADO" : "REPROBADO")}");
                Console.WriteLine("------------------------");
            });
            
            Console.ReadKey();
        }
    }
}