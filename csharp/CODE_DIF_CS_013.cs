using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace SistemaGestionEventos
{
    public interface INotificable
    {
        Task EnviarNotificacion(string mensaje);
    }
    
    public enum TipoEvento { Conferencia, Taller, Seminario, Networking }
    public enum EstadoEvento { Planificado, EnCurso, Finalizado, Cancelado }
    
    public class Participante : INotificable
    {
        public string Nombre { get; set; }
        public string Email { get; set; }
        public string Telefono { get; set; }
        public List<int> EventosInscritos { get; set; } = new();
        
        public async Task EnviarNotificacion(string mensaje)
        {
            Console.WriteLine($"📧 Enviando a {Nombre} ({Email}): {mensaje}");
            await Task.Delay(100); // Simular envío
        }
    }
    
    public class Evento
    {
        public int Id { get; set; }
        public string Titulo { get; set; }
        public TipoEvento Tipo { get; set; }
        public DateTime FechaInicio { get; set; }
        public DateTime FechaFin { get; set; }
        public string Ubicacion { get; set; }
        public int CapacidadMaxima { get; set; }
        public EstadoEvento Estado { get; set; }
        public List<Participante> Participantes { get; set; } = new();
        public decimal CostoPorPersona { get; set; }
        
        public bool TieneCapacidad => Participantes.Count < CapacidadMaxima;
        public TimeSpan Duracion => FechaFin - FechaInicio;
        public decimal IngresoTotal => Participantes.Count * CostoPorPersona;
        
        public async Task<bool> InscribirParticipante(Participante participante)
        {
            if (TieneCapacidad && Estado == EstadoEvento.Planificado)
            {
                Participantes.Add(participante);
                participante.EventosInscritos.Add(Id);
                
                await participante.EnviarNotificacion(
                    $"Te has inscrito exitosamente al evento: {Titulo}. Fecha: {FechaInicio:dd/MM/yyyy HH:mm}");
                
                return true;
            }
            return false;
        }
        
        public async Task NotificarATodos(string mensaje)
        {
            var tareas = Participantes.Select(p => p.EnviarNotificacion(mensaje));
            await Task.WhenAll(tareas);
        }
    }
    
    public class GestorEventos
    {
        private List<Evento> eventos = new();
        private List<Participante> participantes = new();
        private int nextEventId = 1;
        
        public void InicializarDatosPrueba()
        {
            // Participantes de prueba
            participantes.AddRange(new[]
            {
                new Participante { Nombre = "Ana García", Email = "ana@email.com", Telefono = "123-456-7890" },
                new Participante { Nombre = "Carlos Ruiz", Email = "carlos@email.com", Telefono = "123-456-7891" },
                new Participante { Nombre = "María López", Email = "maria@email.com", Telefono = "123-456-7892" }
            });
            
            // Eventos de prueba
            eventos.Add(new Evento
            {
                Id = nextEventId++,
                Titulo = "Conferencia de Tecnología 2025",
                Tipo = TipoEvento.Conferencia,
                FechaInicio = DateTime.Now.AddDays(30),
                FechaFin = DateTime.Now.AddDays(30).AddHours(8),
                Ubicacion = "Centro de Convenciones",
                CapacidadMaxima = 100,
                Estado = EstadoEvento.Planificado,
                CostoPorPersona = 150m
            });
        }
        
        public void MostrarEventosDisponibles()
        {
            var disponibles = eventos.Where(e => e.Estado == EstadoEvento.Planificado && e.TieneCapacidad).ToList();
            
            Console.WriteLine("\n=== EVENTOS DISPONIBLES ===");
            foreach (var evento in disponibles)
            {
                Console.WriteLine($"[{evento.Id}] {evento.Titulo} ({evento.Tipo})");
                Console.WriteLine($"    📅 {evento.FechaInicio:dd/MM/yyyy HH:mm} - {evento.FechaFin:HH:mm}");
                Console.WriteLine($"    📍 {evento.Ubicacion}");
                Console.WriteLine($"    👥 {evento.Participantes.Count}/{evento.CapacidadMaxima} participantes");
                Console.WriteLine($"    💰 ${evento.CostoPorPersona}");
                Console.WriteLine($"    ⏱️ Duración: {evento.Duracion.TotalHours:F1} horas");
                Console.WriteLine();
            }
        }
        
        public async Task<bool> InscribirParticipanteAEvento(int eventoId, string nombreParticipante)
        {
            var evento = eventos.FirstOrDefault(e => e.Id == eventoId);
            var participante = participantes.FirstOrDefault(p => 
                p.Nombre.Contains(nombreParticipante, StringComparison.OrdinalIgnoreCase));
            
            if (evento != null && participante != null)
            {
                return await evento.InscribirParticipante(participante);
            }
            
            return false;
        }
        
        public void GenerarReporteFinanciero()
        {
            Console.WriteLine("\n=== REPORTE FINANCIERO DE EVENTOS ===");
            decimal ingresoTotal = 0;
            int totalParticipantes = 0;
            
            foreach (var evento in eventos)
            {
                Console.WriteLine($"{evento.Titulo}:");
                Console.WriteLine($"  Participantes: {evento.Participantes.Count}");
                Console.WriteLine($"  Ingresos: ${evento.IngresoTotal:F2}");
                Console.WriteLine($"  Ocupación: {(evento.Participantes.Count * 100.0 / evento.CapacidadMaxima):F1}%");
                
                ingresoTotal += evento.IngresoTotal;
                totalParticipantes += evento.Participantes.Count;
                Console.WriteLine();
            }
            
            Console.WriteLine($"📊 TOTALES:");
            Console.WriteLine($"   Total participantes: {totalParticipantes}");
            Console.WriteLine($"   Ingresos totales: ${ingresoTotal:F2}");
            Console.WriteLine($"   Promedio por evento: ${ingresoTotal / eventos.Count:F2}");
        }
        
        public async Task EnviarRecordatoriosEventos()
        {
            var eventosProximos = eventos.Where(e => 
                e.Estado == EstadoEvento.Planificado && 
                e.FechaInicio <= DateTime.Now.AddDays(7)).ToList();
            
            Console.WriteLine("\n📢 Enviando recordatorios...");
            
            foreach (var evento in eventosProximos)
            {
                string mensaje = $"Recordatorio: El evento '{evento.Titulo}' será el {evento.FechaInicio:dd/MM/yyyy} en {evento.Ubicacion}";
                await evento.NotificarATodos(mensaje);
                Console.WriteLine($"Recordatorios enviados para: {evento.Titulo}");
            }
        }
    }
    
    class Program
    {
        static async Task Main(string[] args)
        {
            var gestor = new GestorEventos();
            gestor.InicializarDatosPrueba();
            
            bool continuar = true;
            Console.WriteLine("=== SISTEMA DE GESTIÓN DE EVENTOS PREMIUM ===");
            
            while (continuar)
            {
                Console.WriteLine("\n1. Ver eventos disponibles");
                Console.WriteLine("2. Inscribir participante");
                Console.WriteLine("3. Generar reporte financiero");
                Console.WriteLine("4. Enviar recordatorios");
                Console.WriteLine("5. Salir");
                Console.Write("Seleccione opción: ");
                
                switch (Console.ReadLine())
                {
                    case "1":
                        gestor.MostrarEventosDisponibles();
                        break;
                        
                    case "2":
                        Console.Write("ID del evento: ");
                        if (int.TryParse(Console.ReadLine(), out int eventoId))
                        {
                            Console.Write("Nombre del participante: ");
                            string nombre = Console.ReadLine();
                            
                            bool exito = await gestor.InscribirParticipanteAEvento(eventoId, nombre);
                            Console.WriteLine(exito ? "✅ Inscripción exitosa" : "❌ No se pudo inscribir");
                        }
                        break;
                        
                    case "3":
                        gestor.GenerarReporteFinanciero();
                        break;
                        
                    case "4":
                        await gestor.EnviarRecordatoriosEventos();
                        break;
                        
                    case "5":
                        continuar = false;
                        break;
                        
                    default:
                        Console.WriteLine("Opción no válida");
                        break;
                }
            }
            
            Console.WriteLine("¡Gracias por usar nuestro sistema de gestión de eventos!");
        }
    }
}
