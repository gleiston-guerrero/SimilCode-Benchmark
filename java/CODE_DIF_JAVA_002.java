package Java.Diferente;

import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;
import java.util.ArrayList;

public class CODE_DIF_JAVA_002 {
    private ArrayList<Actividad> actividades;
    
    public CODE_DIF_JAVA_002() {
        actividades = new ArrayList<>();
    }
    
    class Actividad {
        private String descripcion;
        private LocalDateTime fecha;
        private String categoria;
        
        public Actividad(String descripcion, String categoria) {
            this.descripcion = descripcion;
            this.categoria = categoria;
            this.fecha = LocalDateTime.now();
        }
        
        @Override
        public String toString() {
            return String.format("[%s] %s - %s", 
                categoria, descripcion, 
                fecha.format(DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm")));
        }
    }
    
    public void agregarActividad(String desc, String cat) {
        actividades.add(new Actividad(desc, cat));
    }
    
    public void mostrarHistorial() {
        System.out.println("=== HISTORIAL DE ACTIVIDADES ===");
        actividades.forEach(System.out::println);
    }
    
    public static void main(String[] args) {
        CODE_DIF_JAVA_002 registro = new CODE_DIF_JAVA_002();
        registro.agregarActividad("Reunión equipo", "TRABAJO");
        registro.agregarActividad("Ejercicio matutino", "SALUD");
        registro.mostrarHistorial();
    }
}