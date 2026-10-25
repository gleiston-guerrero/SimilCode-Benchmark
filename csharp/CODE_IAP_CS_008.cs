using System;

namespace PlataformaElectoral
{
    class ProcesoElectoral
    {
        static void Main(string[] args)
        {
            new ProcesoElectoral().Ejecutar();
        }

        void Ejecutar()
        {
            Console.WriteLine("=== Sistema de Votación ===");
            int[] conteoPorCandidato = new int[3];
            int votosTotalesEmitidos = 0;

            ImprimirCatalogoCandidatos();

            for (;;)
            {
                Console.Write("\nIngrese su voto: ");
                int opcionRecibida = Convert.ToInt32(Console.ReadLine());

                if (opcionRecibida == 0)
                {
                    break;
                }

                if (opcionRecibida >= 1 && opcionRecibida <= 3)
                {
                    conteoPorCandidato[opcionRecibida - 1]++;
                    votosTotalesEmitidos++;
                }
                else
                {
                    Console.WriteLine("Voto inválido");
                }
            }

            ImprimirResumenResultados(conteoPorCandidato, votosTotalesEmitidos);
            ImprimirGanador(conteoPorCandidato);

            Console.ReadKey();
        }

        void ImprimirCatalogoCandidatos()
        {
            Console.WriteLine("Candidatos disponibles:");
            Console.WriteLine("1 - Candidato A");
            Console.WriteLine("2 - Candidato B");
            Console.WriteLine("3 - Candidato C");
            Console.WriteLine("0 - Finalizar votación");
        }

        void ImprimirResumenResultados(int[] votosAcumulados, int votosTotalesEmitidos)
        {
            Console.WriteLine("\n=== RESULTADOS ===");
            string[] nombreCandidatos = { "Candidato A", "Candidato B", "Candidato C" };

            for (int indiceCandidato = 0; indiceCandidato < nombreCandidatos.Length; indiceCandidato++)
            {
                Console.WriteLine(nombreCandidatos[indiceCandidato] + ": " + votosAcumulados[indiceCandidato] + " votos");
            }

            Console.WriteLine("Total de votos: " + votosTotalesEmitidos);
        }

        void ImprimirGanador(int[] votosAcumulados)
        {
            int maximoVotosActual = votosAcumulados[0];
            int indiceLider = 0;
            int aspirantesAlLiderato = 1;

            for (int indiceCandidato = 1; indiceCandidato < votosAcumulados.Length; indiceCandidato++)
            {
                if (votosAcumulados[indiceCandidato] > maximoVotosActual)
                {
                    maximoVotosActual = votosAcumulados[indiceCandidato];
                    indiceLider = indiceCandidato;
                    aspirantesAlLiderato = 1;
                }
                else if (votosAcumulados[indiceCandidato] == maximoVotosActual)
                {
                    aspirantesAlLiderato++;
                }
            }

            if (aspirantesAlLiderato > 1)
            {
                Console.WriteLine("Hay empate entre candidatos");
                return;
            }

            if (indiceLider == 0)
            {
                Console.WriteLine("¡Ganador: Candidato A!");
            }
            else if (indiceLider == 1)
            {
                Console.WriteLine("¡Ganador: Candidato B!");
            }
            else if (indiceLider == 2)
            {
                Console.WriteLine("¡Ganador: Candidato C!");
            }
        }
    }
}
