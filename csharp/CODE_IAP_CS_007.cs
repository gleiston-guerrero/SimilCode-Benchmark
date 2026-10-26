using System;

namespace SistemaValidacionPersonal
{
    internal class Principal
    {
        static void Main(string[] args)
        {
            // Imprimir cabecera del sistema
            Console.WriteLine("=== Calculadora de Edad ===");
            
            // Captura de datos separada en un metodo auxiliar
            int anioNac = SolicitarValor("Ingrese su año de nacimiento: ");
            int anioHoy = SolicitarValor("Ingrese el año actual: ");
            
            // Calculo principal
            int calculoTotal = anioHoy - anioNac;
            
            // Mostrar resultado numerico
            Console.WriteLine($"Su edad es: {calculoTotal} años");
            
            // Obtener y mostrar la etapa
            string clasificacion = DeterminarCategoria(calculoTotal);
            Console.WriteLine($"Etapa de vida: {clasificacion}");
            
            // Validar sufragio
            MostrarDisponibilidadVoto(calculoTotal);
            
            // Esperar interaccion para cerrar
            Console.ReadKey();
        }

        // Metodo para leer y convertir la entrada de consola
        private static int SolicitarValor(string textoPeticion)
        {
            Console.Write(textoPeticion);
            string captura = Console.ReadLine();
            return int.Parse(captura);
        }

        // Logica de clasificacion invertida para cambiar la estructura original
        private static string DeterminarCategoria(int v)
        {
            if (v >= 65) 
            {
                return "Adulto mayor";
            }
            
            if (v >= 18) 
            {
                return "Adulto";
            }
            
            if (v >= 13) 
            {
                return "Adolescente";
            }
            
            return "Niño";
        }

        // Subrutina para verificar el estado de votacion
        private static void MostrarDisponibilidadVoto(int valorEdad)
        {
            bool esMayor = valorEdad > 17;
            
            if (esMayor)
            {
                Console.WriteLine("Puede votar");
            }
            else
            {
                Console.WriteLine("No puede votar aún");
            }
        }
    }
}
