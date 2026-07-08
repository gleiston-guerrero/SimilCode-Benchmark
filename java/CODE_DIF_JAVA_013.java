package Java.Diferente;

import java.util.HashMap;
import java.util.Map;
import java.util.Timer;
import java.util.TimerTask;

public class CODE_DIF_JAVA_013 {
    private Map<String, Double> recursosActivos;
    private Timer timer;
    private boolean sistemaActivo;
    
    public CODE_DIF_JAVA_013() {
        recursosActivos = new HashMap<>();
        timer = new Timer(true);
        sistemaActivo = true;
        inicializarRecursos();
    }
    
    private void inicializarRecursos() {
        recursosActivos.put("CPU", 0.0);
        recursosActivos.put("Memoria", 0.0);
        recursosActivos.put("Disco", 0.0);
        recursosActivos.put("Red", 0.0);
    }
    
    public void iniciarMonitoreo() {
        System.out.println("🖥️  INICIANDO MONITOR DE RECURSOS DEL SISTEMA");
        System.out.println("================================================");
        
        timer.scheduleAtFixedRate(new TimerTask() {
            @Override
            public void run() {
                if (!sistemaActivo) {
                    timer.cancel();
                    return;
                }
                actualizarMetricas();
                mostrarEstadoActual();
                verificarAlertas();
            }
        }, 0, 2000); // Ejecutar cada 2 segundos
        
        // Simular ejecución por 10 segundos
        Timer stopTimer = new Timer();
        stopTimer.schedule(new TimerTask() {
            @Override
            public void run() {
                detenerMonitoreo();
                stopTimer.cancel();
            }
        }, 10000);
    }
    
    private void actualizarMetricas() {
        for (String recurso : recursosActivos.keySet()) {
            double nuevoValor = Math.random() * 100;
            recursosActivos.put(recurso, nuevoValor);
        }
    }
    
    private void mostrarEstadoActual() {
        System.out.println("\n--- ESTADO ACTUAL ---");
        recursosActivos.forEach((recurso, valor) -> 
            System.out.printf("%s: %.1f%% %s%n", 
                            recurso, valor, obtenerBarraProgreso(valor))
        );
    }
    
    private String obtenerBarraProgreso(double porcentaje) {
        int barras = (int) (porcentaje / 10);
        StringBuilder barra = new StringBuilder("[");
        for (int i = 0; i < 10; i++) {
            barra.append(i < barras ? "█" : "░");
        }
        barra.append("]");
        return barra.toString();
    }
    
    private void verificarAlertas() {
        recursosActivos.forEach((recurso, valor) -> {
            if (valor > 90) {
                System.out.println("⚠️  ALERTA: " + recurso + " al " + String.format("%.1f", valor) + "%");
            }
        });
    }
    
    private void detenerMonitoreo() {
        sistemaActivo = false;
        System.out.println("\n🔴 Monitoreo detenido. Sistema cerrado correctamente.");
    }
    
    public static void main(String[] args) {
        CODE_DIF_JAVA_013 monitor = new CODE_DIF_JAVA_013();
        monitor.iniciarMonitoreo();
    }
}