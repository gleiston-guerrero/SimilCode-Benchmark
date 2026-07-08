package Java.Funcional;

import java.util.ArrayList;
import java.util.Random;
import java.util.stream.IntStream;

public class CODE_FUN_JAVA_007 {
    private ArrayList<Integer> valores;
    private Random generador;
    private int limiteInferior;
    private int limiteSuperior;
    private int totalElementos;
    
    public CODE_FUN_JAVA_007(int min, int max, int count) {
        this.limiteInferior = min;
        this.limiteSuperior = max;
        this.totalElementos = count;
        this.generador = new Random();
        this.valores = new ArrayList<>();
    }
    
    public void generarSecuencia() {
        IntStream.range(0, totalElementos)
                .forEach(i -> {
                    int valor = generador.nextInt(limiteSuperior - limiteInferior + 1) + limiteInferior;
                    valores.add(valor);
                });
    }
    
    public void mostrarEstadisticas() {
        System.out.println("Números generados:");
        valores.forEach(v -> System.out.print(v + " "));
        
        int total = valores.stream().mapToInt(Integer::intValue).sum();
        double media = valores.stream().mapToInt(Integer::intValue).average().orElse(0.0);
        
        System.out.println("\nSuma total: " + total);
        System.out.println("Promedio: " + media);
    }
    
    public static void main(String[] args) {
        CODE_FUN_JAVA_007 creador = new CODE_FUN_JAVA_007(1, 100, 10);
        creador.generarSecuencia();
        creador.mostrarEstadisticas();
    }
}