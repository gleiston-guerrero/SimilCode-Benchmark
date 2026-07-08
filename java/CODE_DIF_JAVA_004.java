package Java.Diferente;

import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.ArrayList;

public class CODE_DIF_JAVA_004 {
    
    private ExecutorService executor;
    public CODE_DIF_JAVA_004() {
        executor = Executors.newFixedThreadPool(3);
        new ArrayList<>();
    }
    
    class TareaProcesamiento implements Runnable {
        private String nombre;
        private int duracion;
        
        public TareaProcesamiento(String nombre, int duracion) {
            this.nombre = nombre;
            this.duracion = duracion;
        }
        
        public void run() {
            try {
                System.out.println("Iniciando tarea: " + nombre);
                Thread.sleep(duracion * 1000);
                System.out.println("Completada tarea: " + nombre);
            } catch(InterruptedException e) {
                Thread.currentThread().interrupt();
            }
        }
    }
    
    public void ejecutarTareas() {
        executor.submit(new TareaProcesamiento("Análisis de datos", 3));
        executor.submit(new TareaProcesamiento("Generación de reportes", 2));
        executor.submit(new TareaProcesamiento("Backup de archivos", 4));
        
        executor.shutdown();
        while(!executor.isTerminated()) {
            try {
                Thread.sleep(500);
            } catch(InterruptedException e) {
                Thread.currentThread().interrupt();
            }
        }
        System.out.println("Todas las tareas completadas");
    }
    
    public static void main(String[] args) {
        new CODE_DIF_JAVA_004().ejecutarTareas();
    }
}