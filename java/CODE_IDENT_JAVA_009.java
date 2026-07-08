package Java.Idéntico;

import java.util.ArrayList;

public class CODE_IDENT_JAVA_009 {
    public static void main(String[] args) {
        ArrayList<String> tareas = new ArrayList<>();
        tareas.add("Estudiar Java");
        tareas.add("Hacer ejercicio");
        tareas.add("Comprar víveres");
        tareas.add("Llamar a mamá");
        tareas.add("Leer libro");
        
        int completadas = 0;
        int pendientes = tareas.size();
        
        System.out.println("=== LISTA DE TAREAS ===");
        for(int i = 0; i < tareas.size(); i++) {
            System.out.println((i + 1) + ". " + tareas.get(i));
        }
        
        // Simular completar algunas tareas
        completadas = 2;
        pendientes = tareas.size() - completadas;
        
        System.out.println("\nEstadísticas:");
        System.out.println("Completadas: " + completadas);
        System.out.println("Pendientes: " + pendientes);
        
        if(completadas > pendientes) {
            System.out.println("¡Buen progreso!");
        } else {
            System.out.println("Sigue trabajando");
        }
    }
}