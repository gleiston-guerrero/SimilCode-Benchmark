package Java.Diferente;

import java.util.ArrayList;
import java.util.Date;
import java.text.SimpleDateFormat;

public class CODE_DIF_JAVA_005 {
    private ArrayList<ArchivoInfo> archivos;
    private String directorioBase;
    private SimpleDateFormat formatoFecha;
    
    public CODE_DIF_JAVA_005(String directorio) {
        this.directorioBase = directorio;
        this.archivos = new ArrayList<>();
        this.formatoFecha = new SimpleDateFormat("yyyy-MM-dd HH:mm:ss");
    }
    
    class ArchivoInfo {
        private String nombre;
        private long tamaño;
        private Date fechaCreacion;
        private String tipo;
        
        public ArchivoInfo(String nombre, long tamaño, String tipo) {
            this.nombre = nombre;
            this.tamaño = tamaño;
            this.tipo = tipo;
            this.fechaCreacion = new Date();
        }
        
        public String obtenerExtension() {
            int indice = nombre.lastIndexOf('.');
            return indice > 0 ? nombre.substring(indice + 1) : "sin_extension";
        }
        
        @Override
        public String toString() {
            return String.format("%s [%s] - %.2f KB - %s", 
                nombre, tipo, tamaño / 1024.0, 
                formatoFecha.format(fechaCreacion));
        }
    }
    
    public void agregarArchivo(String nombre, long bytes, String categoria) {
        ArchivoInfo archivo = new ArchivoInfo(nombre, bytes, categoria);
        archivos.add(archivo);
        System.out.println("Archivo agregado: " + archivo.toString());
    }
    
    public void generarReporte() {
        System.out.println("\n=== REPORTE DE ARCHIVOS ===");
        System.out.println("Directorio: " + directorioBase);
        System.out.println("Total archivos: " + archivos.size());
        
        long totalBytes = archivos.stream().mapToLong(a -> a.tamaño).sum();
        System.out.println("Espacio total: " + String.format("%.2f MB", totalBytes / (1024.0 * 1024.0)));
        
        System.out.println("\nDetalle de archivos:");
        archivos.forEach(System.out::println);
    }
    
    public void buscarPorTipo(String tipoDeseado) {
        System.out.println("\n--- Archivos tipo: " + tipoDeseado + " ---");
        archivos.stream()
                .filter(a -> a.tipo.equalsIgnoreCase(tipoDeseado))
                .forEach(System.out::println);
    }
    
    public static void main(String[] args) {
        CODE_DIF_JAVA_005 gestor = new CODE_DIF_JAVA_005("/home/usuario/documentos");
        
        gestor.agregarArchivo("reporte.pdf", 1024000, "DOCUMENTO");
        gestor.agregarArchivo("imagen.jpg", 2048000, "IMAGEN");
        gestor.agregarArchivo("video.mp4", 15728640, "VIDEO");
        gestor.agregarArchivo("codigo.java", 4096, "CODIGO");
        
        gestor.generarReporte();
        gestor.buscarPorTipo("IMAGEN");
    }
}