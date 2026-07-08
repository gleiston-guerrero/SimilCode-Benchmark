using System;
using System.Linq;

namespace SistemaAcademico
{
    public class RegistroAcademico
    {
        private string[] nombresAlumnos;
        private double[] notasAlumnos;
        private int totalAlumnos = 3;
        
        static void Main(string[] args)
        {
            var sistema = new RegistroAcademico();
            sistema.EjecutarSistema();
        }
        
        public void EjecutarSistema()
        {
            Console.WriteLine("=== REGISTRO ACADÉMICO ===");
            InicializarArrays();
            CapturarDatos();
            MostrarResultados();
            EvaluarRendimiento();
        }
        
        private void InicializarArrays()
        {
            nombresAlumnos = new string[totalAlumnos];
            notasAlumnos = new double[totalAlumnos];
        }
        
        private void CapturarDatos()
        {
            for (int contador = 0; contador < totalAlumnos; contador++)
            {
                Console.Write($"Nombre del alumno {contador + 1}: ");
                nombresAlumnos[contador] = Console.ReadLine();
                
                Console.Write($"Nota de {nombresAlumnos[contador]}: ");
                notasAlumnos[contador] = double.Parse(Console.ReadLine());
            }
        }
        
        private void MostrarResultados()
        {
            for (int indice = 0; indice < totalAlumnos; indice++)
            {
                Console.WriteLine($"{nombresAlumnos[indice]}: {notasAlumnos[indice]}");
            }
            
            double promedioGrupo = notasAlumnos.Average();
            Console.WriteLine($"Promedio del grupo: {promedioGrupo:F2}");
        }
        
        private void EvaluarRendimiento()
        {
            double media = notasAlumnos.Sum() / totalAlumnos;
            string mensaje = media >= 7.0 ? "Excelente rendimiento grupal" : "Necesita mejorar el grupo";
            Console.WriteLine(mensaje);
        }
    }
}
