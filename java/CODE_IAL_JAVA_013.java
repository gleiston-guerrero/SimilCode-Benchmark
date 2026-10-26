package Java.Distinto;

import java.util.Scanner;

public class PROGRAMA_DISTINTO_013 {
    public static void main(String[] args) {
        Scanner teclado = new Scanner(System.in);
        
        System.out.print("¿Cuántos números va a ingresar? ");
        int cantidad = teclado.nextInt();
        
        int[] valores = new int[cantidad];
        for (int i = 0; i < cantidad; i++) {
            System.out.print("Número " + (i + 1) + ": ");
            valores[i] = teclado.nextInt();
        }
        
        int mayor = valores[0];
        for (int i = 1; i < valores.length; i++) {
            if (valores[i] > mayor) {
                mayor = valores[i];
            }
        }
        
        System.out.println("El número máximo es: " + mayor);
        teclado.close();
    }
}
