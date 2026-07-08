package Java.Estructural;

import java.util.ArrayList;

public class CODE_ESTRU_JAVA_009 {
    public static void main(String[] args) {
        ArrayList<String> productos = new ArrayList<>();
        productos.add("Laptop Dell");
        productos.add("Mouse inalámbrico");
        productos.add("Teclado mecánico");
        productos.add("Monitor 24 pulgadas");
        productos.add("Webcam HD");
        
        int enStock = 0;
        int agotados = productos.size();
        
        System.out.println("=== INVENTARIO DE PRODUCTOS ===");
        for(int i = 0; i < productos.size(); i++) {
            System.out.println((i + 1) + ". " + productos.get(i));
        }
        
        // Simular productos en stock
        enStock = 3;
        agotados = productos.size() - enStock;
        
        System.out.println("\nEstado del inventario:");
        System.out.println("En stock: " + enStock);
        System.out.println("Agotados: " + agotados);
        
        if(enStock > agotados) {
            System.out.println("Inventario saludable");
        } else {
            System.out.println("Necesita reabastecimiento");
        }
    }
}