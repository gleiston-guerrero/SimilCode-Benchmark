using System;
using System.Collections.Generic;
using System.Threading.Tasks;

namespace SistemaTransporte
{
    public enum TipoVehiculo { Autobus, Metro, Taxi, Bicicleta }
    public enum EstadoViaje { Programado, EnCurso, Completado, Cancelado }
    
    public delegate void ManejadorEventoViaje(object sender, EventoViajeArgs e);
    
    public class EventoViajeArgs : EventArgs
    {
        public string ViajeId { get; }
        public string Mensaje { get; }
        public DateTime Timestamp { get; }
        
        public EventoViajeArgs(string viajeId, string mensaje)
        {
            ViajeId = viajeId;
            Mensaje = mensaje;
            Timestamp = DateTime.Now;
        }
    }
    
    public abstract class Vehiculo
    {
        protected static int contadorId = 1;
        
        public string Id { get; protected set; }
        public TipoVehiculo Tipo { get; protected set; }
        public int CapacidadMaxima { get; protected set; }
        public int PasajerosActuales { get; protected set; }
        public bool EstaOperativo { get; set; } = true;
        
        public event ManejadorEventoViaje EventoViaje;
        
        protected Vehiculo(TipoVehiculo tipo, int capacidad)
        {
            Id = $"{tipo.ToString().ToUpper()}-{contadorId++:D3}";
            Tipo = tipo;
            CapacidadMaxima = capacidad;
            PasajerosActuales = 0;
        }
        
        public virtual bool PuedeAceptarPasajeros(int cantidad)
        {
            return EstaOperativo && (PasajerosActuales + cantidad <= CapacidadMaxima);
        }
        
        public virtual void SubirPasajeros(int cantidad)
        {
            if (PuedeAceptarPasajeros(cantidad))
            {
                PasajerosActuales += cantidad;
                OnEventoViaje($"Subieron {cantidad} pasajeros. Total: {PasajerosActuales}/{CapacidadMaxima}");
            }
            else
            {
                OnEventoViaje($"No se pueden subir {cantidad} pasajeros. Capacidad insuficiente.");
            }
        }
        
        public virtual void BajarPasajeros(int cantidad)
        {
            if (cantidad <= PasajerosActuales)
            {
                PasajerosActuales -= cantidad;
                OnEventoViaje($"Bajaron {cantidad} pasajeros. Total: {PasajerosActuales}/{CapacidadMaxima}");
            }
        }
        
        protected virtual void OnEventoViaje(string mensaje)
        {
            EventoViaje?.Invoke(this, new EventoViajeArgs(Id, mensaje));
        }
        
        public abstract decimal CalcularTarifa(double distanciaKm);
        public abstract Task<TimeSpan> EstimarTiempoViaje(double distanciaKm);
    }
    
    public class AutobusPublico : Vehiculo
    {
        public string Ruta { get; private set; }
        public List<string> Paradas { get; private set; }
        
        public AutobusPublico(string ruta, List<string> paradas) : base(TipoVehiculo.Autobus, 40)
        {
            Ruta = ruta;
            Paradas = new List<string>(paradas);
        }
        
        public override decimal CalcularTarifa(double distanciaKm)
        {
            return 2500; // Tarifa fija para buses públicos
        }
        
        public override async Task<TimeSpan> EstimarTiempoViaje(double distanciaKm)
        {
            await Task.Delay(100); // Simular cálculo asíncrono
            int minutos = (int)(distanciaKm * 4 + Paradas.Count * 2); // 4 min/km + 2 min por parada
            return TimeSpan.FromMinutes(minutos);
        }
        
        public void LlegarAParada(string parada)
        {
            OnEventoViaje($"Llegando a parada: {parada}");
        }
    }
    
    public class TaxiPrivado : Vehiculo
    {
        public string PlacaVehiculo { get; private set; }
        public string NombreConductor { get; private set; }
        
        public TaxiPrivado(string placa, string conductor) : base(TipoVehiculo.Taxi, 4)
        {
            PlacaVehiculo = placa;
            NombreConductor = conductor;
        }
        
        public override decimal CalcularTarifa(double distanciaKm)
        {
            decimal tarifaBase = 4500;
            decimal tarifaPorKm = 2200;
            return tarifaBase + (decimal)(distanciaKm * (double)tarifaPorKm);
        }
        
        public override async Task<TimeSpan> EstimarTiempoViaje(double distanciaKm)
        {
            await Task.Delay(50);
            int minutos = (int)(distanciaKm * 2.5); // 2.5 min/km (más rápido que bus)
            return TimeSpan.FromMinutes(minutos);
        }
    }
    
    public class CentralTransporte
    {
        private List<Vehiculo> flotaVehiculos;
        private Queue<string> solicitudesPendientes;
        
        public CentralTransporte()
        {
            flotaVehiculos = new List<Vehiculo>();
            solicitudesPendientes = new Queue<string>();
        }
        
        public void RegistrarVehiculo(Vehiculo vehiculo)
        {
            vehiculo.EventoViaje += ManejadorEventoVehiculo;
            flotaVehiculos.Add(vehiculo);
            Console.WriteLine($"🚗 Vehículo {vehiculo.Id} registrado en la central");
        }
        
        private void ManejadorEventoVehiculo(object sender, EventoViajeArgs e)
        {
            Console.WriteLine($"[{e.Timestamp:HH:mm:ss}] {e.ViajeId}: {e.Mensaje}");
        }
        
        public async Task<Vehiculo> SolicitarTransporte(TipoVehiculo tipoPreferido, int numeroPasajeros, double distancia)
        {
            var vehiculosDisponibles = flotaVehiculos.FindAll(v => 
                v.Tipo == tipoPreferido && v.PuedeAceptarPasajeros(numeroPasajeros));
            
            if (vehiculosDisponibles.Count > 0)
            {
                var vehiculoSeleccionado = vehiculosDisponibles[0];
                var tiempoEstimado = await vehiculoSeleccionado.EstimarTiempoViaje(distancia);
                var tarifaEstimada = vehiculoSeleccionado.CalcularTarifa(distancia);
                
                Console.WriteLine($"🎯 Transporte asignado: {vehiculoSeleccionado.Id}");
                Console.WriteLine($"⏱️ Tiempo estimado: {tiempoEstimado.TotalMinutes:F0} minutos");
                Console.WriteLine($"💰 Tarifa estimada: ${tarifaEstimada:N0}");
                
                return vehiculoSeleccionado;
            }
            
            Console.WriteLine($"❌ No hay vehículos {tipoPreferido} disponibles");
            return null;
        }
        
        public void MostrarEstadoFlota()
        {
            Console.WriteLine("\n=== ESTADO DE LA FLOTA ===");
            foreach (var vehiculo in flotaVehiculos)
            {
                string estado = vehiculo.EstaOperativo ? "✅ Operativo" : "❌ Fuera de servicio";
                Console.WriteLine($"{vehiculo.Id} ({vehiculo.Tipo}) - {vehiculo.PasajerosActuales}/{vehiculo.CapacidadMaxima} pasajeros - {estado}");
            }
        }
    }
    
    class Program
    {
        static async Task Main(string[] args)
        {
            CentralTransporte central = new CentralTransporte();
            
            // Registrar vehículos
            var bus1 = new AutobusPublico("Ruta 15A", new List<string> { "Plaza Central", "Universidad", "Hospital", "Terminal" });
            var taxi1 = new TaxiPrivado("ABC-123", "Carlos Ramírez");
            var taxi2 = new TaxiPrivado("XYZ-789", "Ana González");
            
            central.RegistrarVehiculo(bus1);
            central.RegistrarVehiculo(taxi1);
            central.RegistrarVehiculo(taxi2);
            
            Console.WriteLine("🚌 SISTEMA DE TRANSPORTE INTELIGENTE 🚌\n");
            
            // Simular solicitudes de transporte
            Console.WriteLine("=== SIMULACIÓN DE VIAJES ===");
            
            var vehiculo1 = await central.SolicitarTransporte(TipoVehiculo.Taxi, 2, 8.5);
            if (vehiculo1 != null)
            {
                vehiculo1.SubirPasajeros(2);
                await Task.Delay(1000);
                vehiculo1.BajarPasajeros(2);
            }
            
            Console.WriteLine();
            
            var vehiculo2 = await central.SolicitarTransporte(TipoVehiculo.Autobus, 15, 12.0);
            if (vehiculo2 != null && vehiculo2 is AutobusPublico bus)
            {
                vehiculo2.SubirPasajeros(15);
                bus.LlegarAParada("Universidad");
                vehiculo2.BajarPasajeros(5);
                bus.LlegarAParada("Hospital");
                vehiculo2.BajarPasajeros(10);
            }
            
            central.MostrarEstadoFlota();
            
            Console.WriteLine("\nPresiona cualquier tecla para finalizar...");
            Console.ReadKey();
        }
    }
}