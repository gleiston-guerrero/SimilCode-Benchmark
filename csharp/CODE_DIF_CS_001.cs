using System;

namespace CalculadoraMatematica
{
    public class Calculadora
    {
        private double resultado;
        
        public Calculadora()
        {
            resultado = 0.0;
        }
        
        public void Sumar(double numero)
        {
            resultado += numero;
            MostrarOperacion("suma", numero);
        }
        
        public void Restar(double numero)
        {
            resultado -= numero;
            MostrarOperacion("resta", numero);
        }
        
        public void Multiplicar(double numero)
        {
            resultado *= numero;
            MostrarOperacion("multiplicación", numero);
        }
        
        public void Dividir(double numero)
        {
            if (numero != 0)
            {
                resultado /= numero;
                MostrarOperacion("división", numero);
            }
            else
            {
                Console.WriteLine("Error: No se puede dividir por cero");
            }
        }
        
        private void MostrarOperacion(string operacion, double numero)
        {
            Console.WriteLine($"Realizando {operacion} con {numero}");
            Console.WriteLine($"Resultado actual: {resultado}");
        }
        
        public double ObtenerResultado()
        {
            return resultado;
        }
        
        public void Limpiar()
        {
            resultado = 0.0;
            Console.WriteLine("Calculadora reiniciada");
        }
        
        public double CalcularPotencia(double baseNum, double exponente)
        {
            double potencia = Math.Pow(baseNum, exponente);
            Console.WriteLine($"{baseNum} elevado a {exponente} = {potencia}");
            return potencia;
        }
    }
    
    public class ProgramaPrincipal
    {
        static void Main()
        {
            Calculadora calc = new Calculadora();
            
            Console.WriteLine("=== CALCULADORA MATEMÁTICA ===");
            
            // Operaciones básicas
            calc.Sumar(15.5);
            calc.Restar(3.2);
            calc.Multiplicar(2);
            calc.Dividir(4);
            
            Console.WriteLine($"\nResultado final: {calc.ObtenerResultado()}");
            
            // Operación de potencia independiente
            calc.CalcularPotencia(2, 8);
            calc.CalcularPotencia(5, 3);
            
            calc.Limpiar();
            
            Console.WriteLine("\nPresiona cualquier tecla para salir...");
            Console.ReadKey();
        }
    }
}