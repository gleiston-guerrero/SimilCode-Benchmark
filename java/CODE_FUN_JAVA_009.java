package Java.Funcional;

import java.util.HashMap;
import java.util.Map;

public class CODE_FUN_JAVA_009 {
    private Map<String, Boolean> actividades;
    
    public CODE_FUN_JAVA_009() {
        actividades = new HashMap<>();
        inicializarActividades();
    }
    
    private void inicializarActividades() {
        actividades.put("Estudiar Java", false);
        actividades.put("Hacer ejercicio", false);
        actividades.put("Comprar víveres", false);
        actividades.put("Llamar a mamá", false);
        actividades.put("Leer libro", false);
    }
    
    public void marcarCompletada(String tarea) {
        actividades.put(tarea, true);
    }
    
    public void mostrarLista() {
        System.out.println("=== LISTA DE TAREAS ===");
        int contador = 1;
        for(Map.Entry<String, Boolean> entry : actividades.entrySet()) {
            String estado = entry.getValue() ? "[✓]" : "[ ]";
            System.out.println(contador + ". " + estado + " " + entry.getKey());
            contador++;
        }
    }
    
    public void mostrarEstadisticas() {
        long terminadas = actividades.values().stream().filter(Boolean::booleanValue).count();
        long restantes = actividades.size() - terminadas;
        
        System.out.println("\nEstadísticas:");
        System.out.println("Completadas: " + terminadas);
        System.out.println("Pendientes: " + restantes);
        
        String mensaje = terminadas > restantes ? "¡Buen progreso!" : "Sigue trabajando";
        System.out.println(mensaje);
    }
    
    public static void main(String[] args) {
        CODE_FUN_JAVA_009 gestor = new CODE_FUN_JAVA_009();
        gestor.marcarCompletada("Estudiar Java");
        gestor.marcarCompletada("Hacer ejercicio");
        gestor.mostrarLista();
        gestor.mostrarEstadisticas();
    }
}