using System;

namespace VotacionApp
{
    class Votacion
    {
        static void Main(string[] args)
        {
            Console.WriteLine("=== Sistema de Votación ===");
            
            int contadorVotosA = 0;
            int contadorVotosB = 0;
            int contadorVotosC = 0;
            int sumaVotos = 0;
            
            Console.WriteLine("Candidatos disponibles:");
            Console.WriteLine("1 - Candidato A");
            Console.WriteLine("2 - Candidato B");
            Console.WriteLine("3 - Candidato C");
            Console.WriteLine("0 - Finalizar votación");
            
            bool seguirVotando = true;
            while (seguirVotando)
            {
                Console.Write("\nIngrese su voto: ");
                int eleccion = Convert.ToInt32(Console.ReadLine());
                
                if (eleccion == 0)
                    seguirVotando = false;
                else if (eleccion == 1)
                {
                    contadorVotosA++;
                    sumaVotos++;
                }
                else if (eleccion == 2)
                {
                    contadorVotosB++;
                    sumaVotos++;
                }
                else if (eleccion == 3)
                {
                    contadorVotosC++;
                    sumaVotos++;
                }
                else
                {
                    Console.WriteLine("Voto inválido");
                }
            }
            
            Console.WriteLine("\n=== RESULTADOS ===");
            Console.WriteLine($"Candidato A: {contadorVotosA} votos");
            Console.WriteLine($"Candidato B: {contadorVotosB} votos");
            Console.WriteLine($"Candidato C: {contadorVotosC} votos");
            Console.WriteLine($"Total de votos: {sumaVotos}");
            
            if (contadorVotosA > contadorVotosB && contadorVotosA > contadorVotosC)
                Console.WriteLine("¡Ganador: Candidato A!");
            else if (contadorVotosB > contadorVotosA && contadorVotosB > contadorVotosC)
                Console.WriteLine("¡Ganador: Candidato B!");
            else if (contadorVotosC > contadorVotosA && contadorVotosC > contadorVotosB)
                Console.WriteLine("¡Ganador: Candidato C!");
            else
                Console.WriteLine("Hay empate entre candidatos");
            
            Console.ReadKey();
        }
    }
}
