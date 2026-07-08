using System;
using System.Collections.Generic;
using System.Linq;

namespace EleccionesDigitales
{
    class SistemaElectoral
    {
        static Dictionary<string, int> conteoVotos = new Dictionary<string, int>
        {
            {"Candidato Alpha", 0},
            {"Candidato Beta", 0},
            {"Candidato Gamma", 0}
        };
        
        static void Main(string[] args)
        {
            Console.WriteLine("=== Sistema Electoral Digital ===");
            
            MostrarCandidatos();
            ProcesarVotacion();
            MostrarResultadosFinales();
            DeterminarGanador();
            
            Console.ReadKey();
        }
        
        static void MostrarCandidatos()
        {
            Console.WriteLine("Opciones de votación:");
            var candidatos = conteoVotos.Keys.ToArray();
            for (int i = 0; i < candidatos.Length; i++)
            {
                Console.WriteLine($"{i + 1} → {candidatos[i]}");
            }
            Console.WriteLine("0 → Terminar proceso electoral");
        }
        
        static void ProcesarVotacion()
        {
            bool votacionActiva = true;
            var nombresCandidatos = conteoVotos.Keys.ToArray();
            
            while (votacionActiva)
            {
                Console.Write("\nSeleccione su opción de voto: ");
                
                try
                {
                    int seleccion = int.Parse(Console.ReadLine());
                    
                    if (seleccion == 0)
                    {
                        votacionActiva = false;
                    }
                    else if (seleccion >= 1 && seleccion <= nombresCandidatos.Length)
                    {
                        string candidatoSeleccionado = nombresCandidatos[seleccion - 1];
                        conteoVotos[candidatoSeleccionado]++;
                        Console.WriteLine($"✓ Voto registrado para {candidatoSeleccionado}");
                    }
                    else
                    {
                        Console.WriteLine("⚠ Opción no válida");
                    }
                }
                catch
                {
                    Console.WriteLine("⚠ Entrada inválida");
                }
            }
        }
        
        static void MostrarResultadosFinales()
        {
            Console.WriteLine("\n=== ESCRUTINIO FINAL ===");
            int totalGeneral = conteoVotos.Values.Sum();
            
            foreach (var candidato in conteoVotos.OrderByDescending(x => x.Value))
            {
                double porcentaje = totalGeneral > 0 ? (candidato.Value * 100.0 / totalGeneral) : 0;
                Console.WriteLine($"{candidato.Key}: {candidato.Value} votos ({porcentaje:F1}%)");
            }
            
            Console.WriteLine($"Participación total: {totalGeneral} electores");
        }
        
        static void DeterminarGanador()
        {
            var ganador = conteoVotos.OrderByDescending(x => x.Value).First();
            var segundoLugar = conteoVotos.OrderByDescending(x => x.Value).Skip(1).First();
            
            if (ganador.Value > segundoLugar.Value)
            {
                Console.WriteLine($"\n🏆 GANADOR ELECTO: {ganador.Key}");
            }
            else
            {
                Console.WriteLine("\n⚖ RESULTADO: Empate técnico entre candidatos");
            }
        }
    }
}