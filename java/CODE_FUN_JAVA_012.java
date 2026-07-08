package Java.Funcional;

import java.util.ArrayList;
import java.util.Scanner;

public class CODE_FUN_JAVA_012 {
    private ArrayList<Integer> numeros;
    
    public CODE_FUN_JAVA_012() {
        this.numeros = new ArrayList<>();
    }
    
    public void capturarNumeros() {
        Scanner input = new Scanner(System.in);
        System.out.print("¿Cuántos números ingresará? ");
        int total = input.nextInt();
        
        for (int indice = 0; indice < total; indice++) {
            System.out.print("Ingrese el número #" + (indice + 1) + ": ");
            int valor = input.nextInt();
            numeros.add(valor);
        }
        input.close();
    }
    
    public int contarPares() {
        int paresEncontrados = 0;
        for (Integer num : numeros) {
            if (esPar(num)) {
                paresEncontrados++;
            }
        }
        return paresEncontrados;
    }
    
    private boolean esPar(int numero) {
        return numero % 2 == 0;
    }
    
    public void mostrarResultado() {
        int totalPares = contarPares();
        System.out.println("Total de números pares encontrados: " + totalPares);
    }
    
    public static void main(String[] args) {
        CODE_FUN_JAVA_012 analizador = new CODE_FUN_JAVA_012();
        analizador.capturarNumeros();
        analizador.mostrarResultado();
    }
}