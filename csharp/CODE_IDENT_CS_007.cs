using System;

namespace CalculadoraEdad
{
    class Program
    {
        static void Main(string[] args)
        {
            Console.WriteLine("=== Calculadora de Edad ===");
            
            Console.Write("Ingrese su año de nacimiento: ");
            int añoNacimiento = Convert.ToInt32(Console.ReadLine());
            
            Console.Write("Ingrese el año actual: ");
            int añoActual = Convert.ToInt32(Console.ReadLine());
            
            int edad = añoActual - añoNacimiento;
            
            Console.WriteLine($"Su edad es: {edad} años");
            
            string etapa;
            if (edad < 13)
                etapa = "Niño";
            else if (edad < 18)
                etapa = "Adolescente";
            else if (edad < 65)
                etapa = "Adulto";
            else
                etapa = "Adulto mayor";
            
            Console.WriteLine($"Etapa de vida: {etapa}");
            
            if (edad >= 18)
                Console.WriteLine("Puede votar");
            else
                Console.WriteLine("No puede votar aún");
            
            Console.ReadKey();
        }
    }
}