using System;

namespace EvaluacionAcademica
{
    public class CalculadorPromedio
    {
        private double[] notas;
        private int totalAlumnos;
        
        public void InicializarSistema()
        {
            Console.WriteLine("Sistema de Calificaciones");
            Console.Write("Ingrese el número de estudiantes: ");
            totalAlumnos = Convert.ToInt32(Console.ReadLine());
            notas = new double[totalAlumnos];
            
            CapturarCalificaciones();
            MostrarResultados();
        }
        
        private void CapturarCalificaciones()
        {
            for (int contador = 0; contador < totalAlumnos; contador++)
            {
                Console.Write($"Calificación del estudiante {contador + 1}: ");
                notas[contador] = Convert.ToDouble(Console.ReadLine());
            }
        }
        
        private double CalcularPromedio()
        {
            double acumulador = 0;
            for (int i = 0; i < notas.Length; i++)
            {
                acumulador += notas[i];
            }
            return acumulador / notas.Length;
        }
        
        private void MostrarResultados()
        {
            double promedioGrupo = CalcularPromedio();
            string estadoGrupal = DeterminarEstado(promedioGrupo);
            
            Console.WriteLine($"Promedio del grupo: {promedioGrupo:F2}");
            Console.WriteLine($"Estado del grupo: {estadoGrupal}");
            MostrarRendimiento(promedioGrupo);
        }
        
        private string DeterminarEstado(double prom)
        {
            return prom >= 7.0 ? "Aprobado" : "Reprobado";
        }
        
        private void MostrarRendimiento(double prom)
        {
            switch (prom)
            {
                case >= 9.0:
                    Console.WriteLine("¡Excelente rendimiento!");
                    break;
                case >= 7.0:
                    Console.WriteLine("Buen rendimiento");
                    break;
                default:
                    Console.WriteLine("Necesita mejorar");
                    break;
            }
        }
    }
    
    class Program
    {
        static void Main()
        {
            CalculadorPromedio calculadora = new CalculadorPromedio();
            calculadora.InicializarSistema();
        }
    }
}