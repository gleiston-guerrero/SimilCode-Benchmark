using System;
using System.Collections.Generic;

namespace GestionEmpleados
{
    
    public class Empleado
    {
        public string Nombre { get; set; }
        public int Edad { get; set; }
        public double Salario { get; set; }
        public string Departamento { get; set; }
        
        public Empleado(string nombre, int edad, double salario, string departamento)
        {
            this.Nombre = nombre;
            this.Edad = edad;
            this.Salario = salario;
            this.Departamento = departamento;
        }
        
        public void MostrarDatos()
        {
            Console.WriteLine("Empleado: " + this.Nombre);
            Console.WriteLine("Edad: " + this.Edad + " años");
            Console.WriteLine("Salario: $" + this.Salario);
            Console.WriteLine("Departamento: " + this.Departamento);
        }
        
        public double CalcularBono()
        {
            if (this.Salario > 50000)
            {
                return this.Salario * 0.15;  // 15% de bono
            }
            else
            {
                return this.Salario * 0.10;  // 10% de bono
            }
        }
        
        public bool EsJubilable()
        {
            return this.Edad >= 65;
        }
    }
    
    public class MainProgram
    {
        public static void Main(string[] args)
        {
            List<Empleado> empleados = new List<Empleado>();
            
            empleados.Add(new Empleado("Ana Rodríguez", 45, 60000, "Ventas"));
            empleados.Add(new Empleado("Pedro Martín", 67, 75000, "Gerencia"));
            empleados.Add(new Empleado("Laura Sánchez", 32, 45000, "Marketing"));
            
            Console.WriteLine("=== REPORTE DE EMPLEADOS ===");
            
            foreach (Empleado emp in empleados)
            {
                emp.MostrarDatos();
                Console.WriteLine("Bono anual: $" + emp.CalcularBono());
                
                if (emp.EsJubilable())
                {
                    Console.WriteLine("Estatus: PUEDE JUBILARSE");
                }
                else
                {
                    Console.WriteLine("Estatus: EN ACTIVO");
                }
                
                Console.WriteLine("======================");
            }
            
            Console.ReadLine();
        }
    }
}