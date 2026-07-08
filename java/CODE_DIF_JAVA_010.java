package Java.Diferente;

import java.io.BufferedReader;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;
import java.util.TreeMap;
import java.util.regex.Pattern;

public class CODE_DIF_JAVA_010 {
    private TreeMap<String, Integer> frecuenciaPalabras;
    private TreeMap<Character, Integer> frecuenciaCaracteres;
    private String nombreArchivo;
    private Pattern patternPalabra;
    
    public CODE_DIF_JAVA_010(String archivo) {
        this.nombreArchivo = archivo;
        this.frecuenciaPalabras = new TreeMap<>();
        this.frecuenciaCaracteres = new TreeMap<>();
        this.patternPalabra = Pattern.compile("[a-zA-ZáéíóúÁÉÍÓÚñÑ]+");
    }
    
    public void procesarArchivo() {
        try(BufferedReader reader = new BufferedReader(new FileReader(nombreArchivo))) {
            String linea;
            while((linea = reader.readLine()) != null) {
                analizarLinea(linea.toLowerCase());
            }
        } catch(IOException e) {
            System.err.println("Error leyendo archivo: " + e.getMessage());
            // Usar texto de ejemplo si no se puede leer archivo
            analizarLinea("java es un lenguaje de programacion orientado a objetos muy potente");
        }
    }
    
    private void analizarLinea(String texto) {
        // Análisis de palabras
        String[] palabras = texto.split("\\s+");
        for(String palabra : palabras) {
            if(patternPalabra.matcher(palabra).matches() && palabra.length() > 2) {
                frecuenciaPalabras.merge(palabra, 1, Integer::sum);
            }
        }
        
        // Análisis de caracteres
        for(char c : texto.toCharArray()) {
            if(Character.isLetter(c)) {
                frecuenciaCaracteres.merge(c, 1, Integer::sum);
            }
        }
    }
    
    public void generarReporteCompleto() {
        System.out.println("=== ANÁLISIS ESTADÍSTICO DE TEXTO ===");
        System.out.println("Archivo: " + nombreArchivo);
        
        System.out.println("\n--- TOP 10 PALABRAS MÁS FRECUENTES ---");
        frecuenciaPalabras.entrySet().stream()
            .sorted((e1, e2) -> e2.getValue().compareTo(e1.getValue()))
            .limit(10)
            .forEach(entry -> System.out.printf("%-15s: %d veces%n", 
                entry.getKey(), entry.getValue()));
        
        System.out.println("\n--- TOP 5 CARACTERES MÁS FRECUENTES ---");
        frecuenciaCaracteres.entrySet().stream()
            .sorted((e1, e2) -> e2.getValue().compareTo(e1.getValue()))
            .limit(5)
            .forEach(entry -> System.out.printf("'%c': %d veces%n", 
                entry.getKey(), entry.getValue()));
        
        exportarEstadisticas();
    }
    
    private void exportarEstadisticas() {
        try(FileWriter writer = new FileWriter("estadisticas_" + nombreArchivo.replace(".txt", "") + ".csv")) {
            writer.write("Palabra,Frecuencia\n");
            frecuenciaPalabras.forEach((palabra, freq) -> {
                try {
                    writer.write(palabra + "," + freq + "\n");
                } catch(IOException e) {
                    System.err.println("Error escribiendo estadísticas");
                }
            });
            System.out.println("\nEstadísticas exportadas a CSV");
        } catch(IOException e) {
            System.err.println("Error creando archivo de estadísticas: " + e.getMessage());
        }
    }
    
    public static void main(String[] args) {
        String archivo = args.length > 0 ? args[0] : "texto_ejemplo.txt";
        CODE_DIF_JAVA_010 analizador = new CODE_DIF_JAVA_010(archivo);
        analizador.procesarArchivo();
        analizador.generarReporteCompleto();
    }
}