package Java.Funcional;

import java.util.ArrayList;
import java.util.List;
import java.util.Scanner;

public class CODE_FUN_JAVA_015 {
    private List<String> actividades;
    private Scanner entrada;
    
    public CODE_FUN_JAVA_015() {
        this.actividades = new ArrayList<>();
        this.entrada = new Scanner(System.in);
    }
    
    public void mostrarMenu() {
        boolean continuar = true;
        
        while (continuar) {
            System.out.println("\n=== GESTOR DE ACTIVIDADES ===");
            System.out.println("A. Añadir nueva actividad");
            System.out.println("B. Listar todas las actividades");
            System.out.println("C. Terminar programa");
            System.out.print("Ingrese su elección: ");
            
            String eleccion = entrada.nextLine().toUpperCase();
            
            switch (eleccion) {
                case "A" -> agregarActividad();
                case "B" -> listarActividades();
                case "C" -> {
                    System.out.println("Programa finalizado.");
                    continuar = false;
                }
                default -> System.out.println("Opción no válida. Intente nuevamente.");
            }
        }
    }
    
    private void agregarActividad() {
        System.out.print("Describa la actividad: ");
        String nuevaActividad = entrada.nextLine();
        actividades.add(nuevaActividad);
        System.out.println("✓ Actividad registrada exitosamente!");
    }
    
    private void listarActividades() {
        System.out.println("\n--- REGISTRO DE ACTIVIDADES ---");
        if (actividades.isEmpty()) {
            System.out.println("Sin actividades por mostrar");
        } else {
            for (int indice = 0; indice < actividades.size(); indice++) {
                System.out.printf("%d) %s%n", indice + 1, actividades.get(indice));
            }
        }
    }
    
    public static void main(String[] args) {
        CODE_FUN_JAVA_015 gestor = new CODE_FUN_JAVA_015();
        gestor.mostrarMenu();
    }
}