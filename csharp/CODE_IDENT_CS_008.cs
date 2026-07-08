using System;

namespace SistemaVotacion
{
    class Program
    {
        static void Main(string[] args)
        {
            Console.WriteLine("=== Sistema de Votación ===");
            
            int votosCandidatoA = 0;
            int votosCandidatoB = 0;
            int votosCandidatoC = 0;
            int totalVotos = 0;
            
            Console.WriteLine("Candidatos disponibles:");
            Console.WriteLine("1 - Candidato A");
            Console.WriteLine("2 - Candidato B");
            Console.WriteLine("3 - Candidato C");
            Console.WriteLine("0 - Finalizar votación");
            
            while (true)
            {
                Console.Write("\nIngrese su voto: ");
                int voto = Convert.ToInt32(Console.ReadLine());
                
                if (voto == 0)
                    break;
                else if (voto == 1)
                {
                    votosCandidatoA++;
                    totalVotos++;
                }
                else if (voto == 2)
                {
                    votosCandidatoB++;
                    totalVotos++;
                }
                else if (voto == 3)
                {
                    votosCandidatoC++;
                    totalVotos++;
                }
                else
                {
                    Console.WriteLine("Voto inválido");
                }
            }
            
            Console.WriteLine("\n=== RESULTADOS ===");
            Console.WriteLine($"Candidato A: {votosCandidatoA} votos");
            Console.WriteLine($"Candidato B: {votosCandidatoB} votos");
            Console.WriteLine($"Candidato C: {votosCandidatoC} votos");
            Console.WriteLine($"Total de votos: {totalVotos}");
            
            if (votosCandidatoA > votosCandidatoB && votosCandidatoA > votosCandidatoC)
                Console.WriteLine("¡Ganador: Candidato A!");
            else if (votosCandidatoB > votosCandidatoA && votosCandidatoB > votosCandidatoC)
                Console.WriteLine("¡Ganador: Candidato B!");
            else if (votosCandidatoC > votosCandidatoA && votosCandidatoC > votosCandidatoB)
                Console.WriteLine("¡Ganador: Candidato C!");
            else
                Console.WriteLine("Hay empate entre candidatos");
            
            Console.ReadKey();
        }
    }
}