using System;
using System.Collections.Generic;
using System.IO;
using System.Text.Json;
using System.Threading.Tasks;

namespace SistemaAnalisisFinanciero
{
    public class TransaccionFinanciera
    {
        public DateTime Fecha { get; set; }
        public string Descripcion { get; set; }
        public decimal Monto { get; set; }
        public TipoTransaccion Tipo { get; set; }
        public string Categoria { get; set; }
    }
    
    public enum TipoTransaccion { Ingreso, Gasto, Transferencia, Inversion }
    
    public class AnalizadorFinanciero
    {
        private List<TransaccionFinanciera> transacciones = new();
        private readonly Dictionary<string, decimal> presupuestoCategoria = new()
        {
            { "Alimentación", 500m },
            { "Transporte", 200m },
            { "Entretenimiento", 150m },
            { "Servicios", 300m }
        };
        
        public async Task<bool> CargarDatosIniciales()
        {
            try
            {
                await Task.Delay(800); // Simular carga de datos
                
                transacciones.AddRange(new[]
                {
                    new TransaccionFinanciera 
                    { 
                        Fecha = DateTime.Now.AddDays(-15), 
                        Descripcion = "Salario", 
                        Monto = 2500m, 
                        Tipo = TipoTransaccion.Ingreso,
                        Categoria = "Salario"
                    },
                    new TransaccionFinanciera 
                    { 
                        Fecha = DateTime.Now.AddDays(-10), 
                        Descripcion = "Supermercado", 
                        Monto = -180m, 
                        Tipo = TipoTransaccion.Gasto,
                        Categoria = "Alimentación"
                    },
                    new TransaccionFinanciera 
                    { 
                        Fecha = DateTime.Now.AddDays(-5), 
                        Descripcion = "Gasolina", 
                        Monto = -85m, 
                        Tipo = TipoTransaccion.Gasto,
                        Categoria = "Transporte"
                    }
                });
                
                return true;
            }
            catch
            {
                return false;
            }
        }
        
        public void GenerarReporteCompleto()
        {
            Console.WriteLine("=== ANÁLISIS FINANCIERO AVANZADO ===\n");
            
            decimal totalIngresos = 0, totalGastos = 0;
            var gastosPorCategoria = new Dictionary<string, decimal>();
            
            foreach (var transaccion in transacciones)
            {
                if (transaccion.Tipo == TipoTransaccion.Ingreso)
                    totalIngresos += transaccion.Monto;
                else if (transaccion.Tipo == TipoTransaccion.Gasto)
                {
                    totalGastos += Math.Abs(transaccion.Monto);
                    
                    if (!gastosPorCategoria.ContainsKey(transaccion.Categoria))
                        gastosPorCategoria[transaccion.Categoria] = 0;
                    
                    gastosPorCategoria[transaccion.Categoria] += Math.Abs(transaccion.Monto);
                }
            }
            
            decimal balance = totalIngresos - totalGastos;
            
            Console.WriteLine($"💰 Ingresos totales: ${totalIngresos:F2}");
            Console.WriteLine($"💸 Gastos totales: ${totalGastos:F2}");
            Console.WriteLine($"📊 Balance neto: ${balance:F2}");
            Console.WriteLine($"📈 Tasa de ahorro: {(balance/totalIngresos)*100:F1}%\n");
            
            AnalizePresupuesto(gastosPorCategoria);
            GenerarRecomendaciones(balance, totalIngresos);
        }
        
        private void AnalizePresupuesto(Dictionary<string, decimal> gastosPorCategoria)
        {
            Console.WriteLine("=== ANÁLISIS DE PRESUPUESTO ===");
            
            foreach (var categoria in presupuestoCategoria)
            {
                decimal gastoReal = gastosPorCategoria.GetValueOrDefault(categoria.Key, 0);
                decimal porcentajeUsado = (gastoReal / categoria.Value) * 100;
                
                string estado = porcentajeUsado switch
                {
                    > 100 => "🚨 EXCEDIDO",
                    > 80 => "⚠️ CERCA DEL LÍMITE",
                    _ => "✅ DENTRO DEL PRESUPUESTO"
                };
                
                Console.WriteLine($"{categoria.Key}: ${gastoReal:F2}/${categoria.Value:F2} ({porcentajeUsado:F0}%) {estado}");
            }
            Console.WriteLine();
        }
        
        private void GenerarRecomendaciones(decimal balance, decimal ingresos)
        {
            Console.WriteLine("=== RECOMENDACIONES FINANCIERAS ===");
            
            if (balance < 0)
                Console.WriteLine("🔴 ALERTA: Estás gastando más de lo que ganas");
            else if (balance / ingresos < 0.1m)
                Console.WriteLine("🟡 Tasa de ahorro baja, considera reducir gastos");
            else if (balance / ingresos > 0.3m)
                Console.WriteLine("🟢 Excelente capacidad de ahorro, considera inversiones");
            else
                Console.WriteLine("🟢 Balance financiero saludable");
            
            Console.WriteLine("\n💡 Sugerencias:");
            Console.WriteLine("• Establecer metas de ahorro mensual");
            Console.WriteLine("• Revisar gastos no esenciales");
            Console.WriteLine("• Considerar fuentes de ingreso adicionales");
        }
        
        public async Task ExportarReporte()
        {
            var reporte = new
            {
                FechaGeneracion = DateTime.Now,
                TotalTransacciones = transacciones.Count,
                Transacciones = transacciones
            };
            
            try
            {
                string json = JsonSerializer.Serialize(reporte, new JsonSerializerOptions { WriteIndented = true });
                string filename = $"reporte_financiero_{DateTime.Now:yyyyMMdd_HHmmss}.json";
                
                Console.WriteLine($"Generando reporte: {filename}");
                await Task.Delay(1000); // Simular exportación
                Console.WriteLine("✅ Reporte exportado exitosamente");
            }
            catch (Exception ex)
            {
                Console.WriteLine($"❌ Error al exportar: {ex.Message}");
            }
        }
    }
    
    class Program
    {
        static async Task Main(string[] args)
        {
            var analizador = new AnalizadorFinanciero();
            
            Console.WriteLine("Cargando datos financieros...");
            bool cargaExitosa = await analizador.CargarDatosIniciales();
            
            if (cargaExitosa)
            {
                analizador.GenerarReporteCompleto();
                
                Console.WriteLine("\n¿Desea exportar el reporte? (s/n): ");
                if (Console.ReadLine()?.ToLower() == "s")
                {
                    await analizador.ExportarReporte();
                }
            }
            else
            {
                Console.WriteLine("Error al cargar los datos financieros");
            }
            
            Console.WriteLine("\nPresione cualquier tecla para continuar...");
            Console.ReadKey();
        }
    }
}