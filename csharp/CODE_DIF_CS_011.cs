using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;

namespace SistemaReservasHotel
{
    public enum TipoHabitacion { Simple, Doble, Suite, Presidencial }
    public enum EstadoReserva { Pendiente, Confirmada, Cancelada, CheckedIn, CheckedOut }
    
    public class Habitacion
    {
        public int Numero { get; set; }
        public TipoHabitacion Tipo { get; set; }
        public decimal PrecioPorNoche { get; set; }
        public bool Disponible { get; set; } = true;
        
        public override string ToString()
        {
            return $"Habitación {Numero} ({Tipo}) - ${PrecioPorNoche}/noche - {(Disponible ? "Disponible" : "Ocupada")}";
        }
    }
    
    public class Reserva
    {
        public int Id { get; set; }
        public string Cliente { get; set; }
        public Habitacion Habitacion { get; set; }
        public DateTime FechaEntrada { get; set; }
        public DateTime FechaSalida { get; set; }
        public EstadoReserva Estado { get; set; }
        
        public decimal CalcularTotal()
        {
            int noches = (FechaSalida - FechaEntrada).Days;
            return noches * Habitacion.PrecioPorNoche;
        }
    }
    
    public class HotelManager
    {
        private List<Habitacion> habitaciones = new();
        private List<Reserva> reservas = new();
        private int nextReservaId = 1;
        
        public HotelManager()
        {
            InicializarHabitaciones();
        }
        
        private void InicializarHabitaciones()
        {
            habitaciones.AddRange(new[]
            {
                new Habitacion { Numero = 101, Tipo = TipoHabitacion.Simple, PrecioPorNoche = 80 },
                new Habitacion { Numero = 102, Tipo = TipoHabitacion.Doble, PrecioPorNoche = 120 },
                new Habitacion { Numero = 201, Tipo = TipoHabitacion.Suite, PrecioPorNoche = 200 },
                new Habitacion { Numero = 301, Tipo = TipoHabitacion.Presidencial, PrecioPorNoche = 500 }
            });
        }
        
        public void MostrarHabitacionesDisponibles()
        {
            var disponibles = habitaciones.Where(h => h.Disponible).ToList();
            Console.WriteLine("\n=== HABITACIONES DISPONIBLES ===");
            disponibles.ForEach(h => Console.WriteLine(h));
        }
        
        public async Task<bool> CrearReserva(string cliente, int numeroHabitacion, DateTime entrada, DateTime salida)
        {
            var habitacion = habitaciones.FirstOrDefault(h => h.Numero == numeroHabitacion && h.Disponible);
            
            if (habitacion != null)
            {
                Console.WriteLine("Procesando reserva...");
                await Task.Delay(1500); // Simular procesamiento
                
                var reserva = new Reserva
                {
                    Id = nextReservaId++,
                    Cliente = cliente,
                    Habitacion = habitacion,
                    FechaEntrada = entrada,
                    FechaSalida = salida,
                    Estado = EstadoReserva.Confirmada
                };
                
                habitacion.Disponible = false;
                reservas.Add(reserva);
                
                Console.WriteLine($"Reserva #{reserva.Id} confirmada para {cliente}");
                Console.WriteLine($"Total a pagar: ${reserva.CalcularTotal():F2}");
                return true;
            }
            
            return false;
        }
        
        public void MostrarReservas()
        {
            Console.WriteLine("\n=== RESERVAS ACTIVAS ===");
            var activas = reservas.Where(r => r.Estado != EstadoReserva.Cancelada).ToList();
            
            foreach (var reserva in activas)
            {
                Console.WriteLine($"#{reserva.Id}: {reserva.Cliente} - Habitación {reserva.Habitacion.Numero}");
                Console.WriteLine($"  {reserva.FechaEntrada:dd/MM/yyyy} - {reserva.FechaSalida:dd/MM/yyyy} | Estado: {reserva.Estado}");
                Console.WriteLine($"  Total: ${reserva.CalcularTotal():F2}");
            }
        }
    }
    
    class Program
    {
        static async Task Main(string[] args)
        {
            var hotel = new HotelManager();
            bool continuar = true;
            
            Console.WriteLine("=== SISTEMA DE RESERVAS HOTEL PREMIUM ===");
            
            while (continuar)
            {
                Console.WriteLine("\n1. Ver habitaciones disponibles");
                Console.WriteLine("2. Hacer reserva");
                Console.WriteLine("3. Ver reservas");
                Console.WriteLine("4. Salir");
                Console.Write("Seleccione opción: ");
                
                switch (Console.ReadLine())
                {
                    case "1":
                        hotel.MostrarHabitacionesDisponibles();
                        break;
                        
                    case "2":
                        Console.Write("Nombre del cliente: ");
                        string cliente = Console.ReadLine();
                        
                        Console.Write("Número de habitación: ");
                        if (int.TryParse(Console.ReadLine(), out int numHab))
                        {
                            Console.Write("Fecha entrada (dd/MM/yyyy): ");
                            if (DateTime.TryParse(Console.ReadLine(), out DateTime entrada))
                            {
                                Console.Write("Fecha salida (dd/MM/yyyy): ");
                                if (DateTime.TryParse(Console.ReadLine(), out DateTime salida))
                                {
                                    bool exito = await hotel.CrearReserva(cliente, numHab, entrada, salida);
                                    if (!exito)
                                        Console.WriteLine("No se pudo crear la reserva");
                                }
                            }
                        }
                        break;
                        
                    case "3":
                        hotel.MostrarReservas();
                        break;
                        
                    case "4":
                        continuar = false;
                        break;
                        
                    default:
                        Console.WriteLine("Opción no válida");
                        break;
                }
            }
        }
    }
}