package Java.Distinto;

import java.util.Scanner;

public class NUMEROS_PAR {
    public static void main(String[] args) {
        Scanner entrada = new Scanner(System.in);
        
        System.out.print("Ingrese la cantidad de números: ");
        int totalNumeros = entrada.nextInt();
        
        int paresContador = 0;
        for (int indice = 0; indice < totalNumeros; indice++) {
            System.out.print("Número " + (indice + 1) + ": ");
            int valor = entrada.nextInt();
            
            if (valor % 2 == 0) {
                paresContador++;
            }
        }
        
        System.out.println("Cantidad de números pares: " + paresContador);
        entrada.close();
    }
}
