using System;
using System.Collections.Generic;
using System.Threading.Tasks;

namespace EcommerceAdvanced
{
    public interface IPaymentProcessor
    {
        Task<bool> ProcessPayment(decimal amount, string method);
    }
    
    public class PaymentService : IPaymentProcessor
    {
        private readonly Dictionary<string, decimal> fees = new()
        {
            { "credit", 0.03m },
            { "debit", 0.01m },
            { "paypal", 0.025m }
        };
        
        public async Task<bool> ProcessPayment(decimal amount, string method)
        {
            await Task.Delay(1000); // Simular procesamiento
            
            if (fees.ContainsKey(method.ToLower()))
            {
                decimal fee = amount * fees[method.ToLower()];
                Console.WriteLine($"Procesando ${amount} con comisión de ${fee:F2}");
                return new Random().Next(1, 11) > 2; // 80% éxito
            }
            return false;
        }
    }
    
    public class ShoppingCart
    {
        private readonly Dictionary<string, (decimal price, int quantity)> items = new();
        private readonly IPaymentProcessor paymentProcessor;
        
        public ShoppingCart(IPaymentProcessor processor)
        {
            paymentProcessor = processor;
        }
        
        public void AddItem(string product, decimal price, int quantity = 1)
        {
            if (items.ContainsKey(product))
            {
                var current = items[product];
                items[product] = (current.price, current.quantity + quantity);
            }
            else
            {
                items[product] = (price, quantity);
            }
            
            Console.WriteLine($"Agregado: {quantity}x {product} - ${price * quantity:F2}");
        }
        
        public decimal GetTotal()
        {
            decimal total = 0;
            foreach (var item in items.Values)
            {
                total += item.price * item.quantity;
            }
            return total;
        }
        
        public void ShowCart()
        {
            Console.WriteLine("\n=== CARRITO DE COMPRAS ===");
            foreach (var kvp in items)
            {
                var (price, quantity) = kvp.Value;
                Console.WriteLine($"{kvp.Key}: {quantity}x ${price} = ${price * quantity:F2}");
            }
            Console.WriteLine($"TOTAL: ${GetTotal():F2}");
        }
        
        public async Task<bool> Checkout(string paymentMethod)
        {
            decimal total = GetTotal();
            if (total > 0)
            {
                Console.WriteLine($"\nProcesando pago de ${total:F2} con {paymentMethod}...");
                bool success = await paymentProcessor.ProcessPayment(total, paymentMethod);
                
                if (success)
                {
                    items.Clear();
                    Console.WriteLine("¡Compra realizada exitosamente!");
                    return true;
                }
                else
                {
                    Console.WriteLine("Error en el procesamiento del pago");
                    return false;
                }
            }
            return false;
        }
    }
    
    class Program
    {
        static async Task Main(string[] args)
        {
            var paymentService = new PaymentService();
            var cart = new ShoppingCart(paymentService);
            bool shopping = true;
            
            Console.WriteLine("=== TIENDA ONLINE AVANZADA ===");
            
            while (shopping)
            {
                Console.WriteLine("\n1. Agregar producto");
                Console.WriteLine("2. Ver carrito");
                Console.WriteLine("3. Pagar");
                Console.WriteLine("4. Salir");
                Console.Write("Opción: ");
                
                string option = Console.ReadLine();
                
                switch (option)
                {
                    case "1":
                        Console.Write("Nombre del producto: ");
                        string product = Console.ReadLine();
                        Console.Write("Precio: $");
                        if (decimal.TryParse(Console.ReadLine(), out decimal price))
                        {
                            Console.Write("Cantidad: ");
                            if (int.TryParse(Console.ReadLine(), out int qty))
                            {
                                cart.AddItem(product, price, qty);
                            }
                        }
                        break;
                        
                    case "2":
                        cart.ShowCart();
                        break;
                        
                    case "3":
                        if (cart.GetTotal() > 0)
                        {
                            Console.WriteLine("Métodos de pago: credit, debit, paypal");
                            Console.Write("Seleccione método: ");
                            string method = Console.ReadLine();
                            await cart.Checkout(method);
                        }
                        else
                        {
                            Console.WriteLine("El carrito está vacío");
                        }
                        break;
                        
                    case "4":
                        shopping = false;
                        break;
                        
                    default:
                        Console.WriteLine("Opción no válida");
                        break;
                }
            }
            
            Console.WriteLine("¡Gracias por usar nuestra tienda!");
        }
    }
}