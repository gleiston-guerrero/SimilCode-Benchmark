package Java.Diferente;

import java.util.concurrent.Executors;
import java.util.concurrent.ScheduledExecutorService;
import java.util.concurrent.TimeUnit;
import java.util.concurrent.atomic.AtomicInteger;

public class CODE_DIF_JAVA_015 {
    
    public enum TipoPaquete {
        HTTP(80, "Navegación web"),
        HTTPS(443, "Navegación segura"),
        FTP(21, "Transferencia archivos"),
        SSH(22, "Conexión remota"),
        DNS(53, "Resolución nombres");
        
        private final int puerto;
        private final String descripcion;
        
        TipoPaquete(int puerto, String descripcion) {
            this.puerto = puerto;
            this.descripcion = descripcion;
        }
        
        public int getPuerto() { return puerto; }
        public String getDescripcion() { return descripcion; }
    }
    
    public record PaqueteRed(
        int id,
        String origen,
        String destino,
        TipoPaquete tipo,
        int tamaño,
        long timestamp
    ) {}
    
    private final ScheduledExecutorService scheduler;
    private final AtomicInteger contadorPaquetes;
    private final String[] ipsOrigen = {
        "192.168.1.100", "192.168.1.101", "192.168.1.102", 
        "10.0.0.50", "10.0.0.51"
    };
    private final String[] ipsDestino = {
        "8.8.8.8", "1.1.1.1", "208.67.222.222", 
        "185.228.168.9", "76.76.19.19"
    };
    
    public CODE_DIF_JAVA_015() {
        this.scheduler = Executors.newScheduledThreadPool(3);
        this.contadorPaquetes = new AtomicInteger(0);
    }
    
    public void iniciarSimulacion() {
        System.out.println("🌐 SIMULADOR DE TRÁFICO DE RED");
        System.out.println("==============================");
        System.out.println("Iniciando monitoreo de paquetes...\n");
        
        // Generar paquetes cada 500ms
        scheduler.scheduleAtFixedRate(this::generarPaqueteAleatorio, 0, 500, TimeUnit.MILLISECONDS);
        
        // Mostrar estadísticas cada 3 segundos
        scheduler.scheduleAtFixedRate(this::mostrarEstadisticas, 3, 3, TimeUnit.SECONDS);
        
        // Detener simulación después de 15 segundos
        scheduler.schedule(() -> {
            System.out.println("\n🔴 Deteniendo simulación...");
            scheduler.shutdown();
        }, 15, TimeUnit.SECONDS);
    }
    
    private void generarPaqueteAleatorio() {
        int id = contadorPaquetes.incrementAndGet();
        String origen = ipsOrigen[(int)(Math.random() * ipsOrigen.length)];
        String destino = ipsDestino[(int)(Math.random() * ipsDestino.length)];
        TipoPaquete tipo = TipoPaquete.values()[(int)(Math.random() * TipoPaquete.values().length)];
        int tamaño = 64 + (int)(Math.random() * 1436); // Tamaño típico de paquete
        long timestamp = System.currentTimeMillis();
        
        PaqueteRed paquete = new PaqueteRed(id, origen, destino, tipo, tamaño, timestamp);
        procesarPaquete(paquete);
    }
    
    private void procesarPaquete(PaqueteRed paquete) {
        String indicador = determinarIndicadorTrafico(paquete.tamaño());
        System.out.printf("%s [ID:%d] %s:%d → %s (%s) - %d bytes%n",
                         indicador, paquete.id(), paquete.origen(), 
                         paquete.tipo().getPuerto(), paquete.destino(),
                         paquete.tipo().getDescripcion(), paquete.tamaño());
    }
    
    private String determinarIndicadorTrafico(int tamaño) {
        if (tamaño < 200) return "🟢";
        else if (tamaño < 800) return "🟡";
        else return "🔴";
    }
    
    private void mostrarEstadisticas() {
        int totalPaquetes = contadorPaquetes.get();
        double promedioPorSegundo = totalPaquetes / 3.0;
        
        System.out.println("\n📊 === ESTADÍSTICAS DE RED ===");
        System.out.printf("Total paquetes procesados: %d%n", totalPaquetes);
        System.out.printf("Promedio por segundo: %.1f paquetes/s%n", promedioPorSegundo);
        
        // Simular latencia promedio
        double latenciaPromedio = 15 + (Math.random() * 50);
        System.out.printf("Latencia promedio: %.1f ms%n", latenciaPromedio);
        System.out.println("=============================\n");
    }
    
    public static void main(String[] args) {
        CODE_DIF_JAVA_015 simulador = new CODE_DIF_JAVA_015();
        simulador.iniciarSimulacion();
        
        // Mantener el programa ejecutándose
        try {
            Thread.sleep(16000);
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
        }
    }
}