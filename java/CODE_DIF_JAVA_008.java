package Java.Diferente;

import java.util.Scanner;
import java.util.ArrayList;
import java.util.Collections;

public class CODE_DIF_JAVA_008 {
    private ArrayList<String> cartas;
    private ArrayList<Boolean> reveladas;
    private Scanner entrada;
    private int intentos;
    private int paresEncontrados;
    
    public CODE_DIF_JAVA_008() {
        entrada = new Scanner(System.in);
        inicializarJuego();
    }
    
    private void inicializarJuego() {
        cartas = new ArrayList<>();
        reveladas = new ArrayList<>();
        intentos = 0;
        paresEncontrados = 0;
        
        // Crear pares de cartas
        String[] simbolos = {"🌟", "🎈", "🎯", "🎪", "🎨", "🎭", "🎪", "🏆"};
        for(String simbolo : simbolos) {
            cartas.add(simbolo);
            cartas.add(simbolo); // Agregar el par
        }
        
        Collections.shuffle(cartas);
        
        // Inicializar estado revelado
        for(int i = 0; i < cartas.size(); i++) {
            reveladas.add(false);
        }
    }
    
    public void mostrarTablero() {
        System.out.println("\n=== JUEGO DE MEMORIA ===");
        System.out.println("Intentos: " + intentos + " | Pares encontrados: " + paresEncontrados);
        
        for(int i = 0; i < cartas.size(); i++) {
            if(i % 4 == 0) System.out.println();
            
            if(reveladas.get(i)) {
                System.out.print(cartas.get(i) + " ");
            } else {
                System.out.print((i + 1) + " ");
            }
        }
        System.out.println();
    }
    
    public void jugar() {
        while(paresEncontrados < cartas.size() / 2) {
            mostrarTablero();
            
            System.out.print("Elige primera carta (1-" + cartas.size() + "): ");
            int carta1 = entrada.nextInt() - 1;
            
            System.out.print("Elige segunda carta (1-" + cartas.size() + "): ");
            int carta2 = entrada.nextInt() - 1;
            
            intentos++;
            
            if(carta1 != carta2 && cartas.get(carta1).equals(cartas.get(carta2))) {
                reveladas.set(carta1, true);
                reveladas.set(carta2, true);
                paresEncontrados++;
                System.out.println("¡Par encontrado! " + cartas.get(carta1));
            } else {
                System.out.println("No es par: " + cartas.get(carta1) + " - " + cartas.get(carta2));
                try { Thread.sleep(2000); } catch(InterruptedException e) {}
            }
        }
        
        System.out.println("\n¡Felicidades! Completaste el juego en " + intentos + " intentos.");
    }
    
    public static void main(String[] args) {
        new CODE_DIF_JAVA_008().jugar();
    }
}