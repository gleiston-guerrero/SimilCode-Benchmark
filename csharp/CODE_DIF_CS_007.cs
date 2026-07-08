using System;
using System.Collections.Generic;
using System.Linq;

namespace AdministradorTareas
{
    class GestorProductividad
    {
        static List<Tarea> listaTareas = new List<Tarea>();
        static int contadorId = 1;
        
        static void Main(string[] args)
        {
            Console.WriteLine("📋 ADMINISTRADOR PERSONAL DE TAREAS 📋");
            
            bool sistemaActivo = true;
            
            while (sistemaActivo)
            {
                MostrarMenuPrincipal();
                string seleccion = Console.ReadLine();
                
                switch (seleccion)
                {
                    case "1":
                        CrearNuevaTarea();
                        break;
                    case "2":
                        ListarTareasPendientes();
                        break;
                    case "3":
                        MarcarTareaCompletada();
                        break;
                    case "4":
                        EliminarTarea();
                        break;
                    case "5":
                        MostrarEstadisticasProductividad();
                        break;
                    case "6":
                        sistemaActivo = false;
                        Console.WriteLine("¡Hasta luego! Mantén la productividad 🚀");
                        break;
                    default:
                        Console.WriteLine("❌ Selección no válida");
                        break;
                }
                
                if (sistemaActivo)
                {
                    Console.WriteLine("\nPresiona Enter para continuar...");
                    Console.ReadLine();
                    Console.Clear();
                }
            }
        }
        
        static void MostrarMenuPrincipal()
        {
            Console.WriteLine("\n=== GESTIÓN DE TAREAS ===");
            Console.WriteLine("1. ➕ Crear nueva tarea");
            Console.WriteLine("2. 📝 Ver tareas pendientes");
            Console.WriteLine("3. ✅ Marcar tarea como completada");
            Console.WriteLine("4. 🗑️ Eliminar tarea");
            Console.WriteLine("5. 📊 Ver estadísticas");
            Console.WriteLine("6. 🚪 Salir del sistema");
            Console.Write("\nElige una opción: ");
        }
        
        static void CrearNuevaTarea()
        {
            Console.Write("Descripción de la tarea: ");
            string descripcion = Console.ReadLine();
            
            Console.WriteLine("Prioridad (1-Alta, 2-Media, 3-Baja): ");
            if (int.TryParse(Console.ReadLine(), out int prioridad) && prioridad >= 1 && prioridad <= 3)
            {
                var nuevaTarea = new Tarea(contadorId++, descripcion, (NivelPrioridad)prioridad);
                listaTareas.Add(nuevaTarea);
                Console.WriteLine($"✅ Tarea '{descripcion}' creada exitosamente (ID: {nuevaTarea.Id})");
            }
            else
            {
                Console.WriteLine("❌ Prioridad inválida. Tarea no creada.");
            }
        }
        
        static void ListarTareasPendientes()
        {
            var tareasPendientes = listaTareas.Where(t => !t.EstaCompletada).OrderBy(t => t.Prioridad).ToList();
            
            Console.WriteLine("\n=== TAREAS PENDIENTES ===");
            if (!tareasPendientes.Any())
            {
                Console.WriteLine("🎉 ¡No tienes tareas pendientes!");
            }
            else
            {
                foreach (var tarea in tareasPendientes)
                {
                    string iconoPrioridad = tarea.Prioridad switch
                    {
                        NivelPrioridad.Alta => "🔴",
                        NivelPrioridad.Media => "🟡", 
                        NivelPrioridad.Baja => "🟢",
                        _ => "⚪"
                    };
                    Console.WriteLine($"{iconoPrioridad} [{tarea.Id}] {tarea.Descripcion} ({tarea.Prioridad})");
                }
            }
        }
        
        static void MarcarTareaCompletada()
        {
            Console.Write("ID de la tarea a completar: ");
            if (int.TryParse(Console.ReadLine(), out int id))
            {
                var tarea = listaTareas.FirstOrDefault(t => t.Id == id && !t.EstaCompletada);
                if (tarea != null)
                {
                    tarea.MarcarComoCompletada();
                    Console.WriteLine($"✅ Tarea '{tarea.Descripcion}' marcada como completada!");
                }
                else
                {
                    Console.WriteLine("❌ Tarea no encontrada o ya está completada.");
                }
            }
            else
            {
                Console.WriteLine("❌ ID inválido.");
            }
        }
        
        static void EliminarTarea()
        {
            Console.Write("ID de la tarea a eliminar: ");
            if (int.TryParse(Console.ReadLine(), out int id))
            {
                var tarea = listaTareas.FirstOrDefault(t => t.Id == id);
                if (tarea != null)
                {
                    listaTareas.Remove(tarea);
                    Console.WriteLine($"🗑️ Tarea '{tarea.Descripcion}' eliminada.");
                }
                else
                {
                    Console.WriteLine("❌ Tarea no encontrada.");
                }
            }
            else
            {
                Console.WriteLine("❌ ID inválido.");
            }
        }
        
        static void MostrarEstadisticasProductividad()
        {
            int totalTareas = listaTareas.Count;
            int tareasCompletadas = listaTareas.Count(t => t.EstaCompletada);
            int tareasPendientes = totalTareas - tareasCompletadas;
            
            Console.WriteLine("\n📊 ESTADÍSTICAS DE PRODUCTIVIDAD");
            Console.WriteLine($"📝 Total de tareas: {totalTareas}");
            Console.WriteLine($"✅ Tareas completadas: {tareasCompletadas}");
            Console.WriteLine($"⏳ Tareas pendientes: {tareasPendientes}");
            
            if (totalTareas > 0)
            {
                double porcentajeCompletado = (double)tareasCompletadas / totalTareas * 100;
                Console.WriteLine($"📈 Porcentaje de completado: {porcentajeCompletado:F1}%");
            }
        }
    }
    
    enum NivelPrioridad
    {
        Alta = 1,
        Media = 2,
        Baja = 3
    }
    
    class Tarea
    {
        public int Id { get; }
        public string Descripcion { get; }
        public NivelPrioridad Prioridad { get; }
        public bool EstaCompletada { get; private set; }
        public DateTime FechaCreacion { get; }
        public DateTime? FechaCompletada { get; private set; }
        
        public Tarea(int id, string descripcion, NivelPrioridad prioridad)
        {
            Id = id;
            Descripcion = descripcion;
            Prioridad = prioridad;
            EstaCompletada = false;
            FechaCreacion = DateTime.Now;
        }
        
        public void MarcarComoCompletada()
        {
            EstaCompletada = true;
            FechaCompletada = DateTime.Now;
        }
    }
}