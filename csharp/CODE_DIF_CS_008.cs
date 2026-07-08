using System;
using System.Collections.Generic;
using System.IO;
using System.Text.Json;

namespace GestorTareas
{
    public enum PrioridadTarea { Baja, Media, Alta, Urgente }
    public enum EstadoTarea { Pendiente, EnProceso, Completada, Cancelada }
    
    public class Tarea
    {
        public int Id { get; set; }
        public string Titulo { get; set; }
        public string Descripcion { get; set; }
        public PrioridadTarea Prioridad { get; set; }
        public EstadoTarea Estado { get; set; }
        public DateTime FechaCreacion { get; set; }
        public DateTime? FechaVencimiento { get; set; }
        
        public Tarea()
        {
            FechaCreacion = DateTime.Now;
            Estado = EstadoTarea.Pendiente;
        }
        
        public override string ToString()
        {
            string vencimiento = FechaVencimiento?.ToString("dd/MM/yyyy") ?? "Sin fecha";
            return $"[{Id}] {Titulo} | {Prioridad} | {Estado} | Vence: {vencimiento}";
        }
    }
    
    class GestorTareas
    {
        private static List<Tarea> listaTareas = new List<Tarea>();
        private static int contadorId = 1;
        private static readonly string archivoTareas = "tareas.json";
        
        static void Main(string[] args)
        {
            CargarTareas();
            
            Console.WriteLine("📋 GESTOR PERSONAL DE TAREAS 📋");
            
            bool sistemaActivo = true;
            while (sistemaActivo)
            {
                MostrarMenuPrincipal();
                
                try
                {
                    int opcion = int.Parse(Console.ReadLine());
                    
                    switch (opcion)
                    {
                        case 1:
                            CrearNuevaTarea();
                            break;
                        case 2:
                            ListarTareas();
                            break;
                        case 3:
                            ActualizarEstadoTarea();
                            break;
                        case 4:
                            FiltrarTareasPorEstado();
                            break;
                        case 5:
                            EliminarTarea();
                            break;
                        case 6:
                            MostrarEstadisticas();
                            break;
                        case 7:
                            GuardarTareas();
                            sistemaActivo = false;
                            Console.WriteLine("👋 ¡Tareas guardadas! Hasta luego.");
                            break;
                        default:
                            Console.WriteLine("❌ Opción no válida");
                            break;
                    }
                }
                catch (Exception ex)
                {
                    Console.WriteLine($"❌ Error: {ex.Message}");
                }
                
                if (sistemaActivo)
                {
                    Console.WriteLine("\n⏸ Presiona Enter para continuar...");
                    Console.ReadLine();
                    Console.Clear();
                }
            }
        }
        
        static void MostrarMenuPrincipal()
        {
            Console.WriteLine("\n=== MENÚ PRINCIPAL ===");
            Console.WriteLine("1. ➕ Crear nueva tarea");
            Console.WriteLine("2. 📄 Listar todas las tareas");
            Console.WriteLine("3. ✏️ Actualizar estado de tarea");
            Console.WriteLine("4. 🔍 Filtrar tareas por estado");
            Console.WriteLine("5. 🗑️ Eliminar tarea");
            Console.WriteLine("6. 📊 Ver estadísticas");
            Console.WriteLine("7. 💾 Guardar y salir");
            Console.Write("\nSelecciona una opción: ");
        }
        
        static void CrearNuevaTarea()
        {
            Console.WriteLine("\n=== CREAR NUEVA TAREA ===");
            
            Console.Write("Título: ");
            string titulo = Console.ReadLine();
            
            Console.Write("Descripción: ");
            string descripcion = Console.ReadLine();
            
            Console.WriteLine("Prioridad (0-Baja, 1-Media, 2-Alta, 3-Urgente): ");
            PrioridadTarea prioridad = (PrioridadTarea)int.Parse(Console.ReadLine());
            
            Console.Write("Fecha vencimiento (dd/MM/yyyy) o Enter para omitir: ");
            string fechaInput = Console.ReadLine();
            DateTime? fechaVencimiento = null;
            
            if (!string.IsNullOrEmpty(fechaInput))
            {
                fechaVencimiento = DateTime.ParseExact(fechaInput, "dd/MM/yyyy", null);
            }
            
            var nuevaTarea = new Tarea
            {
                Id = contadorId++,
                Titulo = titulo,
                Descripcion = descripcion,
                Prioridad = prioridad,
                FechaVencimiento = fechaVencimiento
            };
            
            listaTareas.Add(nuevaTarea);
            Console.WriteLine("✅ Tarea creada exitosamente!");
        }
        
        static void ListarTareas()
        {
            Console.WriteLine("\n=== LISTA DE TAREAS ===");
            if (listaTareas.Count == 0)
            {
                Console.WriteLine("📝 No hay tareas registradas");
                return;
            }
            
            foreach (var tarea in listaTareas)
            {
                string indicador = tarea.Estado switch
                {
                    EstadoTarea.Completada => "✅",
                    EstadoTarea.EnProceso => "🔄",
                    EstadoTarea.Cancelada => "❌",
                    _ => "⏳"
                };
                
                Console.WriteLine($"{indicador} {tarea}");
            }
        }
        
        static void ActualizarEstadoTarea()
        {
            Console.Write("ID de la tarea a actualizar: ");
            int id = int.Parse(Console.ReadLine());
            
            var tarea = listaTareas.Find(t => t.Id == id);
            if (tarea == null)
            {
                Console.WriteLine("❌ Tarea no encontrada");
                return;
            }
            
            Console.WriteLine("Nuevo estado (0-Pendiente, 1-EnProceso, 2-Completada, 3-Cancelada): ");
            EstadoTarea nuevoEstado = (EstadoTarea)int.Parse(Console.ReadLine());
            
            tarea.Estado = nuevoEstado;
            Console.WriteLine("✅ Estado actualizado correctamente!");
        }
        
        static void FiltrarTareasPorEstado()
        {
            Console.WriteLine("Filtrar por estado (0-Pendiente, 1-EnProceso, 2-Completada, 3-Cancelada): ");
            EstadoTarea estadoFiltro = (EstadoTarea)int.Parse(Console.ReadLine());
            
            var tareasFiltradas = listaTareas.FindAll(t => t.Estado == estadoFiltro);
            
            Console.WriteLine($"\n=== TAREAS CON ESTADO: {estadoFiltro} ===");
            foreach (var tarea in tareasFiltradas)
            {
                Console.WriteLine(tarea);
            }
        }
        
        static void EliminarTarea()
        {
            Console.Write("ID de la tarea a eliminar: ");
            int id = int.Parse(Console.ReadLine());
            
            int eliminadas = listaTareas.RemoveAll(t => t.Id == id);
            
            if (eliminadas > 0)
                Console.WriteLine("✅ Tarea eliminada correctamente!");
            else
                Console.WriteLine("❌ Tarea no encontrada");
        }
        
        static void MostrarEstadisticas()
        {
            Console.WriteLine("\n=== ESTADÍSTICAS GENERALES ===");
            
            int pendientes = listaTareas.FindAll(t => t.Estado == EstadoTarea.Pendiente).Count;
            int enProceso = listaTareas.FindAll(t => t.Estado == EstadoTarea.EnProceso).Count;
            int completadas = listaTareas.FindAll(t => t.Estado == EstadoTarea.Completada).Count;
            int canceladas = listaTareas.FindAll(t => t.Estado == EstadoTarea.Cancelada).Count;
            
            Console.WriteLine($"📊 Total de tareas: {listaTareas.Count}");
            Console.WriteLine($"⏳ Pendientes: {pendientes}");
            Console.WriteLine($"🔄 En proceso: {enProceso}");
            Console.WriteLine($"✅ Completadas: {completadas}");
            Console.WriteLine($"❌ Canceladas: {canceladas}");
            
            if (listaTareas.Count > 0)
            {
                double porcentajeCompletado = (completadas * 100.0) / listaTareas.Count;
                Console.WriteLine($"📈 Porcentaje de finalización: {porcentajeCompletado:F1}%");
            }
        }
        
        static void CargarTareas()
        {
            try
            {
                if (File.Exists(archivoTareas))
                {
                    string json = File.ReadAllText(archivoTareas);
                    var tareasData = JsonSerializer.Deserialize<List<Tarea>>(json);
                    
                    if (tareasData != null)
                    {
                        listaTareas = tareasData;
                        contadorId = listaTareas.Count > 0 ? listaTareas.Max(t => t.Id) + 1 : 1;
                        Console.WriteLine($"📂 Cargadas {listaTareas.Count} tareas desde archivo");
                    }
                }
            }
            catch (Exception ex)
            {
                Console.WriteLine($"⚠ Error al cargar tareas: {ex.Message}");
            }
        }
        
        static void GuardarTareas()
        {
            try
            {
                string json = JsonSerializer.Serialize(listaTareas, new JsonSerializerOptions { WriteIndented = true });
                File.WriteAllText(archivoTareas, json);
                Console.WriteLine($"💾 {listaTareas.Count} tareas guardadas correctamente");
            }
            catch (Exception ex)
            {
                Console.WriteLine($"⚠ Error al guardar tareas: {ex.Message}");
            }
        }
    }
}