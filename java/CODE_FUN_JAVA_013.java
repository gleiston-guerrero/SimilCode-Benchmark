package Java.Funcional;

import java.util.ArrayList;
import java.util.Collections;
import java.util.Scanner;

public class CODE_FUN_JAVA_013 {
    private ArrayList<Integer> listaNumeros;
    
    public CODE_FUN_JAVA_013() {
        listaNumeros = new ArrayList<>();
    }
    
    public void solicitarDatos() {
        Scanner entrada = new Scanner(System.in);
        System.out.print("Cantidad de valores a procesar: ");
        int cantidad = entrada.nextInt();
        
        recolectarNumeros(entrada, cantidad);
        entrada.close();
    }
    
    private void recolectarNumeros(Scanner entrada, int cantidad) {
        for (int contador = 0; contador < cantidad; contador++) {
            System.out.print("Ingrese valor #" + (contador + 1) + ": ");
            int valor = entrada.nextInt();
            listaNumeros.add(valor);
        }
    }
    
    public int encontrarMaximo() {
        return Collections.max(listaNumeros);
    }
    
    public void mostrarResultado() {
        int valorMaximo = encontrarMaximo();
        System.out.println("El valor máximo encontrado es: " + valorMaximo);
    }
    
    public static void main(String[] args) {
        CODE_FUN_JAVA_013 detector = new CODE_FUN_JAVA_013();
        detector.solicitarDatos();
        detector.mostrarResultado();
    }
}