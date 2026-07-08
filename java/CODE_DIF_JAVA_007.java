package Java.Diferente;

import java.io.FileWriter;
import java.io.IOException;
import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;
import java.util.HashMap;
import java.util.Map;

public class CODE_DIF_JAVA_007 {
    private Map<String, Integer> contadorEventos;
    private DateTimeFormatter formateador;
    private String archivoLog;
    
    public enum NivelLog {
        INFO, WARNING, ERROR, DEBUG
    }
    
    public CODE_DIF_JAVA_007(String nombreArchivo) {
        this.archivoLog = nombreArchivo;
        this.contadorEventos = new HashMap<>();
        this.formateador = DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm:ss");
        inicializarContadores();
    }
    
    private void inicializarContadores() {
        for(NivelLog nivel : NivelLog.values()) {
            contadorEventos.put(nivel.name(), 0);
        }
    }
    
    public void registrarEvento(NivelLog nivel, String mensaje) {
        String timestamp = LocalDateTime.now().format(formateador);
        String entrada = String.format("[%s] %s: %s%n", timestamp, nivel, mensaje);
        
        try(FileWriter writer = new FileWriter(archivoLog, true)) {
            writer.write(entrada);
            contadorEventos.put(nivel.name(), contadorEventos.get(nivel.name()) + 1);
            System.out.print(entrada);
        } catch(IOException e) {
            System.err.println("Error escribiendo log: " + e.getMessage());
        }
    }
    
    public void mostrarEstadisticas() {
        System.out.println("\n=== ESTADÍSTICAS DEL LOG ===");
        contadorEventos.forEach((nivel, count) -> 
            System.out.println(nivel + ": " + count + " eventos"));
    }
    
    public static void main(String[] args) {
        CODE_DIF_JAVA_007 logger = new CODE_DIF_JAVA_007("sistema.log");
        
        logger.registrarEvento(NivelLog.INFO, "Sistema iniciado correctamente");
        logger.registrarEvento(NivelLog.WARNING, "Memoria baja detectada");
        logger.registrarEvento(NivelLog.ERROR, "Fallo en conexión a base de datos");
        logger.registrarEvento(NivelLog.DEBUG, "Variable x = 42");
        logger.registrarEvento(NivelLog.INFO, "Proceso completado");
        
        logger.mostrarEstadisticas();
    }
}