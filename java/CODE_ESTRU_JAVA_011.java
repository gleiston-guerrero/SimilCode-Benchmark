package Java.Estructural;

import java.util.Scanner;

public class CODE_ESTRU_JAVA_011 {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        
        System.out.print("Ingrese el número de productos: ");
        int numProductos = scanner.nextInt();
        
        double totalValor = 0;
        for (int i = 0; i < numProductos; i++) {
            System.out.print("Ingrese precio del producto " + (i + 1) + ": ");
            double precio = scanner.nextDouble();
            totalValor += precio;
        }
        
        double valorPromedio = totalValor / numProductos;
        System.out.println("El valor promedio por producto es: " + valorPromedio);
        
        if (valorPromedio >= 50000) {
            System.out.println("INVENTARIO DE ALTO VALOR");
        } else {
            System.out.println("INVENTARIO DE BAJO VALOR");
        }
        
        scanner.close();
    }
}
