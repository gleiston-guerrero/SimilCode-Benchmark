package Java.Diferente;

import java.util.HashMap;
import java.util.Map;
import java.util.Scanner;

public class CODE_DIF_JAVA_011 {
    private Map<String, Boolean> libros;
    private Scanner scanner;
    
    public CODE_DIF_JAVA_011() {
        libros = new HashMap<>();
        scanner = new Scanner(System.in);
        inicializarLibros();
    }
    
    private void inicializarLibros() {
        libros.put("Don Quijote", true);
        libros.put("Cien Años de Soledad", true);
        libros.put("1984", false);
        libros.put("El Principito", true);
    }
    
    public void mostrarMenu() {
        int opcion;
        do {
            System.out.println("\n=== SISTEMA DE BIBLIOTECA ===");
            System.out.println("1. Mostrar libros disponibles");
            System.out.println("2. Prestar libro");
            System.out.println("3. Devolver libro");
            System.out.println("4. Salir");
            System.out.print("Seleccione una opción: ");
            
            opcion = scanner.nextInt();
            scanner.nextLine();
            
            switch (opcion) {
                case 1 -> mostrarLibrosDisponibles();
                case 2 -> prestarLibro();
                case 3 -> devolverLibro();
                case 4 -> System.out.println("¡Hasta luego!");
                default -> System.out.println("Opción inválida");
            }
        } while (opcion != 4);
    }
    
    private void mostrarLibrosDisponibles() {
        System.out.println("\n--- LIBROS DISPONIBLES ---");
        for (Map.Entry<String, Boolean> entry : libros.entrySet()) {
            if (entry.getValue()) {
                System.out.println("• " + entry.getKey());
            }
        }
    }
    
    private void prestarLibro() {
        System.out.print("Ingrese el nombre del libro: ");
        String nombreLibro = scanner.nextLine();
        
        if (libros.containsKey(nombreLibro) && libros.get(nombreLibro)) {
            libros.put(nombreLibro, false);
            System.out.println("Libro prestado exitosamente!");
        } else {
            System.out.println("Libro no disponible o no existe.");
        }
    }
    
    private void devolverLibro() {
        System.out.print("Ingrese el nombre del libro a devolver: ");
        String nombreLibro = scanner.nextLine();
        
        if (libros.containsKey(nombreLibro)) {
            libros.put(nombreLibro, true);
            System.out.println("Libro devuelto exitosamente!");
        } else {
            System.out.println("Este libro no pertenece a nuestra biblioteca.");
        }
    }
    
    public static void main(String[] args) {
        CODE_DIF_JAVA_011 sistema = new CODE_DIF_JAVA_011();
        sistema.mostrarMenu();
    }
}