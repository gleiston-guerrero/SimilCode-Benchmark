using System;

namespace AnalizadorEdades
{
    class CalculadorVital
    {
        static void Main(string[] args)
        {
            Console.WriteLine("=== Analizador de Etapas Vitales ===");
            
            var fechasInfo = ObtenerInformacionFechas();
            int añosVividos = CalcularAñosTranscurridos(fechasInfo.nacimiento, fechasInfo.referencia);
            string categoriaVital = DeterminarEtapaVida(añosVividos);
            bool puedeEjercer = EvaluarDerechoVoto(añosVividos);
            
            PresentarResultados(añosVividos, categoriaVital, puedeEjercer);
            Console.ReadKey();
        }
        
        static (int nacimiento, int referencia) ObtenerInformacionFechas()
        {
            Console.Write("Año de su nacimiento: ");
            int nac = int.Parse(Console.ReadLine());
            
            Console.Write("Año de referencia: ");
            int refe = int.Parse(Console.ReadLine());
            
            return (nac, refe);
        }
        
        static int CalcularAñosTranscurridos(int añoNacimiento, int añoReferencia)
        {
            return Math.Max(0, añoReferencia - añoNacimiento);
        }
        
        static string DeterminarEtapaVida(int edad)
        {
            return edad switch
            {
                < 13 => "Infancia",
                < 18 => "Adolescencia", 
                < 65 => "Adultez",
                _ => "Tercera edad"
            };
        }
        
        static bool EvaluarDerechoVoto(int edad) => edad >= 18;
        
        static void PresentarResultados(int edad, string etapa, bool voto)
        {
            Console.WriteLine($"\nEdad calculada: {edad} años");
            Console.WriteLine($"Clasificación vital: {etapa}");
            Console.WriteLine($"Derecho al sufragio: {(voto ? "SÍ puede votar" : "NO puede votar")}");
        }
    }
}