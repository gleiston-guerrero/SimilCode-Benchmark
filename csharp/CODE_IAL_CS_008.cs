using System;

namespace VotacionElectoral
{
    class AplicacionVoto
    {
        static void Main(string[] args)
        {
            Console.WriteLine("=== Sistema de Votación ===");
            
            int conteoVotoA = 0;
            int conteoVotoB = 0;
            int conteoVotoC = 0;
            int totalVotos = 0;
            
            Console.WriteLine("Candidatos disponibles:");
            Console.WriteLine("1 - Candidato A");
            Console.WriteLine("2 - Candidato B");
            Console.WriteLine("3 - Candidato C");
            Console.WriteLine("0 - Finalizar votación");
            
            while (true)
            {
                Console.Write("\nIngrese su voto: ");
                int seleccionVoto = Convert.ToInt32(Console.ReadLine());
                
                if (seleccionVoto == 0)
                    break;
                else if (seleccionVoto == 1)
                {
                    conteoVotoA++;
                    totalVotos++;
                }
                else if (seleccionVoto == 2)
                {
                    conteoVotoB++;
                    totalVotos++;
                }
                else if (seleccionVoto == 3)
                {
                    conteoVotoC++;
                    totalVotos++;
                }
                else
                {
                    Console.WriteLine("Voto inválido");
                }
            }
            
            Console.WriteLine("\n=== RESULTADOS ===");
            Console.WriteLine($"Candidato A: {conteoVotoA} votos");
            Console.WriteLine($"Candidato B: {conteoVotoB} votos");
            Console.WriteLine($"Candidato C: {conteoVotoC} votos");
            Console.WriteLine($"Total de votos: {totalVotos}");
            
            if (conteoVotoA > conteoVotoB && conteoVotoA > conteoVotoC)
                Console.WriteLine("¡Ganador: Candidato A!");
            else if (conteoVotoB > conteoVotoA && conteoVotoB > conteoVotoC)
                Console.WriteLine("¡Ganador: Candidato B!");
            else if (conteoVotoC > conteoVotoA && conteoVotoC > conteoVotoB)
                Console.WriteLine("¡Ganador: Candidato C!");
            else
                Console.WriteLine("Hay empate entre candidatos");
            
            Console.ReadKey();
        }
    }
}
