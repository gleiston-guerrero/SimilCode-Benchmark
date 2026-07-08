using System;
using System.Collections.Generic;
using System.Linq;

namespace SistemaInventario
{
    public interface IProducto
    {
        int Id { get; }
        string Nombre { get; }
        decimal Precio { get; }
        int CantidadStock { get; set; }
        decimal CalcularValorTotal();
        bool EstaDisponible();
    }
    
    public interface IVendible
    {
        bool PuedeVenderse(int cantidad);
        void Vender(int cantidad);
        void Reabastecer(int cantidad);
    }
    
    public class ProductoElectronico : IProducto, IVendible
    {
        public int Id { get; private set; }
        public string Nombre { get; private set; }
        public decimal Precio { get; private set; }
        public int CantidadStock { get; set; }
        public string Marca { get; private set; }
        public int GarantiaMeses { get; private set; }
        
        public ProductoElectronico(int id, string nombre, decimal precio, int stock, string marca, int garantia)
        {
            Id = id;
            Nombre = nombre;
            Precio = precio;
            CantidadStock = stock;
            Marca = marca;
            GarantiaMeses = garantia;
        }
        
        public decimal CalcularValorTotal() => Precio * CantidadStock;
        
        public bool EstaDisponible() => CantidadStock > 0;
        
        public bool PuedeVenderse(int cantidad) => CantidadStock >= cantidad;
        
        public void Vender(int cantidad)
        {
            if (PuedeVenderse(cantidad))
            {
                CantidadStock -= cantidad;
            }
            else
            {
                throw new InvalidOperationException("Stock insuficiente para la venta");
            }
        }
        
        public void Reabastecer(int cantidad)
        {
            if (cantidad > 0)
            {
                CantidadStock += cantidad;
            }
        }
        
        public override string ToString()
        {
            return $"[{Id}] {Nombre} ({Marca}) - ${Precio:N0} | Stock: {CantidadStock} | Garantía: {GarantiaMeses} meses";
        }
    }
    
    public class GestorInventario
    {
        private Dictionary<int, IProducto> productos;
        private List<string> historialVentas;
        
        public GestorInventario()
        {
            productos = new Dictionary<int, IProducto>();
            historialVentas = new List<string>();
        }
        
        public void AgregarProducto(IProducto producto)
        {
            productos[producto.Id] = producto;
        }
        
        public IProducto BuscarProducto(int id) => productos.GetValueOrDefault(id);
        
        public void ProcesarVenta(int idProducto, int cantidad)
        {
            var producto = BuscarProducto(idProducto);
            if (producto is IVendible vendible)
            {
                try
                {
                    vendible.Vender(cantidad);
                    decimal totalVenta = producto.Precio * cantidad;
                    string registro = $"{DateTime.Now:yyyy-MM-dd HH:mm} - Vendido: {producto.Nombre} x{cantidad} = ${totalVenta:N0}";
                    historialVentas.Add(registro);
                    Console.WriteLine($"✅ Venta realizada: {producto.Nombre} x{cantidad}");
                }
                catch (InvalidOperationException ex)
                {
                    Console.WriteLine($"❌ Error en venta: {ex.Message}");
                }
            }
        }
        
        public void MostrarInventario()
        {
            Console.WriteLine("=== INVENTARIO ACTUAL ===");
            var productosOrdenados = productos.Values.OrderBy(p => p.Nombre);
            foreach (var producto in productosOrdenados)
            {
                string estado = producto.EstaDisponible() ? "✅ Disponible" : "❌ Agotado";
                Console.WriteLine($"{producto} | {estado}");
            }
        }
        
        public void MostrarHistorialVentas()
        {
            Console.WriteLine("\n=== HISTORIAL DE VENTAS ===");
            foreach (var venta in historialVentas.TakeLast(10))
            {
                Console.WriteLine(venta);
            }
        }
        
        public decimal ValorTotalInventario() => productos.Values.Sum(p => p.CalcularValorTotal());
    }
    
    class Program
    {
        static void Main(string[] args)
        {
            GestorInventario inventario = new GestorInventario();
            
            // Agregar productos
            inventario.AgregarProducto(new ProductoElectronico(1, "Laptop Dell", 2500000, 15, "Dell", 24));
            inventario.AgregarProducto(new ProductoElectronico(2, "Mouse Logitech", 45000, 50, "Logitech", 12));
            inventario.AgregarProducto(new ProductoElectronico(3, "Monitor Samsung", 800000, 8, "Samsung", 36));
            inventario.AgregarProducto(new ProductoElectronico(4, "Teclado Mecánico", 150000, 25, "Corsair", 18));
            
            Console.WriteLine("💻 SISTEMA DE INVENTARIO TECNOLÓGICO 💻\n");
            
            inventario.MostrarInventario();
            Console.WriteLine($"\n💰 Valor total del inventario: ${inventario.ValorTotalInventario():N0}");
            
            // Simular algunas ventas
            Console.WriteLine("\n=== PROCESANDO VENTAS ===");
            inventario.ProcesarVenta(1, 2);  // Vender 2 laptops
            inventario.ProcesarVenta(2, 10); // Vender 10 mouse
            inventario.ProcesarVenta(3, 1);  // Vender 1 monitor
            
            inventario.MostrarHistorialVentas();
            
            Console.WriteLine("\n=== INVENTARIO ACTUALIZADO ===");
            inventario.MostrarInventario();
            
            Console.ReadKey();
        }
    }
}