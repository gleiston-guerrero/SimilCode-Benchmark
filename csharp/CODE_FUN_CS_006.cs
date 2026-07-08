using System;

namespace ConversorTermico
{
    class CalculadoraTemp
    {
        static void Main(string[] args)
        {
            Console.WriteLine("=== Sistema de Conversión Térmica ===");
            
            var datosEntrada = ObtenerDatos();
            double temperaturaConvertida = RealizarConversion(datosEntrada.temperatura, datosEntrada.tipoConversion);
            string escalaDestino = ObtenerNombreEscala(datosEntrada.tipoConversion);
            
            MostrarResultado(datosEntrada.temperatura, temperaturaConvertida, escalaDestino);
            ClasificarTemperatura(temperaturaConvertida);
            
            Console.ReadKey();
        }
        
        static (double temperatura, int tipoConversion) ObtenerDatos()
        {
            Console.Write("Temperatura en grados Celsius: ");
            double temp = double.Parse(Console.ReadLine());
            
            Console.WriteLine("Seleccione conversión:");
            Console.WriteLine("1 → Fahrenheit");
            Console.WriteLine("2 → Kelvin");
            Console.Write("Opción: ");
            int tipo = int.Parse(Console.ReadLine());
            
            return (temp, tipo);
        }
        
        static double RealizarConversion(double celsius, int tipo)
        {
            return tipo switch
            {
                1 => celsius * 1.8 + 32,           // Fahrenheit
                2 => celsius + 273.15,             // Kelvin
                _ => throw new ArgumentException("Tipo de conversión inválido")
            };
        }
        
        static string ObtenerNombreEscala(int tipo) => tipo == 1 ? "Fahrenheit" : "Kelvin";
        
        static void MostrarResultado(double original, double convertida, string escala)
        {
            string simbolo = escala == "Fahrenheit" ? "F" : "K";
            Console.WriteLine($"Resultado: {original}°C = {convertida:F2}°{simbolo}");
        }
        
        static void ClasificarTemperatura(double temp)
        {
            string clasificacion = temp switch
            {
                > 100 => "Temperatura elevada",
                < 0 => "Temperatura bajo el punto de congelación",
                _ => "Rango de temperatura normal"
            };
            Console.WriteLine($"Clasificación: {clasificacion}");
        }
    }
}
