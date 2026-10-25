package Java.Idéntico;

import java.util.ArrayList;

public class ListaTareas {
    public static void main(String[] args) {
        ArrayList<String> actividades = new ArrayList<>();
        actividades.add("Estudiar Java");
        actividades.add("Hacer ejercicio");
        actividades.add("Comprar víveres");
        actividades.add("Llamar a mamá");
        actividades.add("Leer libro");
        
        int finalizadas = 0;
        int restantes = actividades.size();
        
        System.out.println("=== LISTA DE TAREAS ===");
        for(int i = 0; i < actividades.size(); i++) {
            System.out.println((i + 1) + ". " + actividades.get(i));
        }
        
        // Simular completar algunas tareas
        finalizadas = 2;
        restantes = actividades.size() - finalizadas;
        
        System.out.println("\nEstadísticas:");
        System.out.println("Completadas: " + finalizadas);
        System.out.println("Pendientes: " + restantes);
        
        if(finalizadas > restantes) {
            System.out.println("¡Buen progreso!");
        } else {
            System.out.println("Sigue trabajando");
        }
    }
}
