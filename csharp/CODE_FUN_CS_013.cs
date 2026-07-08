using System;

namespace ConvertidorMedidas
{
    public class Convertidor
    {
        private readonly double METROS_A_PIES = 3.28084;
        private readonly double KG_A_LIBRAS = 2.20462;
        
        static void Main(string[] args)
        {
            var convertidor = new Convertidor();
            convertidor.IniciarConversion();
        }
        
        public void IniciarConversion()
        {
            MostrarOpciones();
            int seleccion = ObtenerSeleccion();
            double valorConvertido = RealizarConversion(seleccion);
            CategorizeResult(valorConvertido);
        }
        
        private void MostrarOpciones()
        {
            Console.WriteLine("=== CONVERTIDOR DE MEDIDAS ===");
            string[] conversiones = { "Metros a Pies", "Celsius a Fahrenheit", "Kilogramos a Libras" };
            for (int i = 0; i < conversiones.Length; i++)
            {
                Console.WriteLine($"{i + 1}. {conversiones[i]}");
            }
            Console.Write("Seleccione conversión: ");
        }
        
        private int ObtenerSeleccion()
        {
            return int.Parse(Console.ReadLine());
        }
        
        private double RealizarConversion(int tipo)
        {
            return tipo switch
            {
                1 => ConvertirMetrosAPies(),
                2 => ConvertirCelsiusAFahrenheit(),
                3 => ConvertirKgALibras(),
                _ => 0
            };
        }
        
        private double ConvertirMetrosAPies()
        {
            Console.Write("Ingrese metros: ");
            double m = double.Parse(Console.ReadLine());
            double pies = m * METROS_A_PIES;
            Console.WriteLine($"{m} metros = {pies:F2} pies");
            return pies;
        }
        
        private double ConvertirCelsiusAFahrenheit()
        {
            Console.Write("Ingrese grados Celsius: ");
            double c = double.Parse(Console.ReadLine());
            double fahrenheit = (c * 9.0/5.0) + 32;
            Console.WriteLine($"{c}°C = {fahrenheit:F2}°F");
            return fahrenheit;
        }
        
        private double ConvertirKgALibras()
        {
            Console.Write("Ingrese kilogramos: ");
            double kilogramos = double.Parse(Console.ReadLine());
            double libras = kilogramos * KG_A_LIBRAS;
            Console.WriteLine($"{kilogramos} kg = {libras:F2} libras");
            return libras;
        }
        
        private void CategorizeResult(double valor)
        {
            string categoria = valor > 100 ? "Valor convertido alto" : "Valor convertido normal";
            Console.WriteLine(categoria);
        }
    }
}