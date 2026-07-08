using System;
using System.Collections.Generic;
using System.Linq;

namespace JuegoAdivinanza
{
    class JuegoPreguntas
    {
        static List<Pregunta> preguntas = new List<Pregunta>
        {
            new Pregunta("¿Cuál es la capital de Colombia?", new[] {"Bogotá", "Medellín", "Cali", "Cartagena"}, 0),
            new Pregunta("¿En qué año llegó el hombre a la luna?", new[] {"1967", "1969", "1971", "1975"}, 1),
            new Pregunta("¿Cuál es el planeta más grande del sistema solar?", new[] {"Tierra", "Júpiter", "Saturno", "Neptuno"}, 1),
            new Pregunta("¿Quién escribió 'Cien años de soledad'?", new[] {"Borges", "Cortázar", "García Márquez", "Vargas Llosa"}, 2),
            new Pregunta("¿Cuál es el océano más grande?", new[] {"Atlántico", "Pacífico", "Índico", "Ártico"}, 1)
        };
        
        static Random random = new Random();
        static int puntuacionTotal = 0;
        
        static void Main(string[] args)
        {
            Console.WriteLine("🧠 QUIZ INTERACTIVO DE CULTURA GENERAL 🧠");
            
            var preguntasSeleccionadas = preguntas.OrderBy(x => random.Next()).Take(3).ToList();
            
            for (int i = 0; i < preguntasSeleccionadas.Count; i++)
            {
                Console.WriteLine($"\n=== PREGUNTA {i + 1}/3 ===");
                bool respuestaCorrecta = HacerPregunta(preguntasSeleccionadas[i]);
                
                if (respuestaCorrecta)
                {
                    puntuacionTotal += 10;
                    Console.WriteLine("✅ ¡Correcto! +10 puntos");
                }
                else
                {
                    Console.WriteLine("❌ Incorrecto. +0 puntos");
                    Console.WriteLine($"La respuesta correcta era: {preguntasSeleccionadas[i].Opciones[preguntasSeleccionadas[i].RespuestaCorrecta]}");
                }
                
                Console.WriteLine($"Puntuación actual: {puntuacionTotal}/30");
                
                if (i < preguntasSeleccionadas.Count - 1)
                {
                    Console.WriteLine("\nPresiona Enter para la siguiente pregunta...");
                    Console.ReadLine();
                }
            }
            
            MostrarResultadoFinal();
            Console.ReadKey();
        }
        
        static bool HacerPregunta(Pregunta pregunta)
        {
            Console.WriteLine(pregunta.Texto);
            Console.WriteLine();
            
            for (int i = 0; i < pregunta.Opciones.Length; i++)
            {
                Console.WriteLine($"{i + 1}. {pregunta.Opciones[i]}");
            }
            
            Console.Write("\nTu respuesta (1-4): ");
            
            try
            {
                int respuesta = int.Parse(Console.ReadLine()) - 1;
                return respuesta == pregunta.RespuestaCorrecta;
            }
            catch
            {
                Console.WriteLine("Respuesta inválida, se considera incorrecta.");
                return false;
            }
        }
        
        static void MostrarResultadoFinal()
        {
            Console.WriteLine("\n" + new string('=', 40));
            Console.WriteLine("🏆 RESULTADO FINAL 🏆");
            Console.WriteLine($"Puntuación: {puntuacionTotal}/30 puntos");
            
            string nivel = puntuacionTotal switch
            {
                30 => "¡PERFECTO! Eres un genio 🧠",
                >= 20 => "¡Excelente! Muy buen conocimiento 👏",
                >= 10 => "Bien, pero puedes mejorar 📚",
                _ => "Necesitas estudiar más 📖"
            };
            
            Console.WriteLine($"Nivel: {nivel}");
            Console.WriteLine($"Porcentaje de aciertos: {(puntuacionTotal / 30.0 * 100):F1}%");
        }
        
        class Pregunta
        {
            public string Texto { get; }
            public string[] Opciones { get; }
            public int RespuestaCorrecta { get; }
            
            public Pregunta(string texto, string[] opciones, int respuestaCorrecta)
            {
                Texto = texto;
                Opciones = opciones;
                RespuestaCorrecta = respuestaCorrecta;
            }
        }
    }
}