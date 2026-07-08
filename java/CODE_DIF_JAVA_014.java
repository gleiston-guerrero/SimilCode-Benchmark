package Java.Diferente;

import java.util.ArrayList;
import java.util.List;
import java.util.concurrent.CompletableFuture;
import java.util.concurrent.ExecutionException;

public class CODE_DIF_JAVA_014 {
    
    public enum TipoTarea {
        PROCESAMIENTO_DATOS,
        ENVIO_EMAIL,
        BACKUP_ARCHIVOS,
        ACTUALIZACION_BD
    }
    
    public record Tarea(int id, String nombre, TipoTarea tipo, int duracionMs) {}
    
    private List<Tarea> colaTareas;
    
    public CODE_DIF_JAVA_014() {
        colaTareas = new ArrayList<>();
        inicializarTareas();
    }
    
    private void inicializarTareas() {
        colaTareas.add(new Tarea(1, "Procesar datos de ventas", TipoTarea.PROCESAMIENTO_DATOS, 3000));
        colaTareas.add(new Tarea(2, "Enviar reporte mensual", TipoTarea.ENVIO_EMAIL, 1500));
        colaTareas.add(new Tarea(3, "Backup base de datos", TipoTarea.BACKUP_ARCHIVOS, 5000));
        colaTareas.add(new Tarea(4, "Actualizar inventario", TipoTarea.ACTUALIZACION_BD, 2000));
    }
    
    public CompletableFuture<String> procesarTareaAsincrona(Tarea tarea) {
        return CompletableFuture.supplyAsync(() -> {
            System.out.printf("🔄 Iniciando: %s (ID: %d)%n", tarea.nombre(), tarea.id());
            
            try {
                Thread.sleep(tarea.duracionMs());
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
                return "❌ Tarea interrumpida: " + tarea.nombre();
            }
            
            return String.format("✅ Completada: %s en %dms", tarea.nombre(), tarea.duracionMs());
        });
    }
    
    public void ejecutarTodasLasTareas() {
        System.out.println("🚀 INICIANDO PROCESADOR DE TAREAS ASÍNCRONO");
        System.out.println("==========================================");
        
        List<CompletableFuture<String>> futuros = colaTareas.stream()
                .map(this::procesarTareaAsincrona)
                .toList();
        
        // Combinar todos los futuros
        CompletableFuture<Void> todasLasTareas = CompletableFuture.allOf(
                futuros.toArray(new CompletableFuture[0])
        );
        
        // Procesar resultados cuando estén listos
        todasLasTareas.thenRun(() -> {
            System.out.println("\n📊 RESUMEN DE EJECUCIÓN:");
            futuros.forEach(futuro -> {
                try {
                    System.out.println(futuro.get());
                } catch (InterruptedException | ExecutionException e) {
                    System.err.println("Error procesando tarea: " + e.getMessage());
                }
            });
            System.out.println("\n🎉 Todas las tareas han sido completadas!");
        }).join(); // Esperar a que termine
    }
    
    public static void main(String[] args) {
        CODE_DIF_JAVA_014 procesador = new CODE_DIF_JAVA_014();
        procesador.ejecutarTodasLasTareas();
    }
}