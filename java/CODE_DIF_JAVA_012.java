package Java.Diferente;

import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;
import java.util.concurrent.ThreadLocalRandom;

public class CODE_DIF_JAVA_012 {
    private String[] departamentos = {"Ventas", "Marketing", "IT", "RRHH", "Finanzas"};
    private String[] tiposReporte = {"Mensual", "Trimestral", "Anual"};
    
    class Reporte {
        private String id;
        private String departamento;
        private String tipo;
        private LocalDateTime fechaCreacion;
        private double valorGenerado;
        
        public Reporte(String departamento, String tipo) {
            this.id = "RPT-" + System.currentTimeMillis();
            this.departamento = departamento;
            this.tipo = tipo;
            this.fechaCreacion = LocalDateTime.now();
            this.valorGenerado = ThreadLocalRandom.current().nextDouble(10000, 100000);
        }
        
        @Override
        public String toString() {
            DateTimeFormatter formatter = DateTimeFormatter.ofPattern("dd/MM/yyyy HH:mm");
            return String.format("ID: %s | %s - %s | Fecha: %s | Valor: $%.2f",
                               id, departamento, tipo, fechaCreacion.format(formatter), valorGenerado);
        }
    }
    
    public void generarReportesAleatorios() {
        System.out.println("=== GENERADOR AUTOMÁTICO DE REPORTES ===\n");
        
        for (int i = 0; i < 8; i++) {
            String deptAleatorio = departamentos[ThreadLocalRandom.current().nextInt(departamentos.length)];
            String tipoAleatorio = tiposReporte[ThreadLocalRandom.current().nextInt(tiposReporte.length)];
            
            Reporte reporte = new Reporte(deptAleatorio, tipoAleatorio);
            System.out.println(reporte);
            
            // Simular tiempo de procesamiento
            try {
                Thread.sleep(100);
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
            }
        }
        
        System.out.println("\n✓ Generación de reportes completada.");
    }
    
    public static void main(String[] args) {
        CODE_DIF_JAVA_012 generador = new CODE_DIF_JAVA_012();
        generador.generarReportesAleatorios();
    }
}