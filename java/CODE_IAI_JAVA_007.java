package Java.Modificado;

import java.util.Random;

public class GENERADOR_ALEATORIO {
    public static void main(String[] args) {
        Random generador = new Random();
        int numElementos = 10;
        int limiteInferior = 1;
        int limiteSuperior = 100;
        int total = 0;
        
        System.out.println("Números generados:");
        for(int contador = 0; contador < numElementos; contador++) {
            int valor = generador.nextInt(limiteSuperior - limiteInferior + 1) + limiteInferior;
            System.out.print(valor + " ");
            total += valor;
        }
        
        double media = total / (double)numElementos;
        System.out.println("\nSuma total: " + total);
        System.out.println("Promedio: " + media);
    }
}
