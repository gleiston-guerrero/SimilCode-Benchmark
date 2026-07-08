package Java.Diferente;

import java.util.HashMap;
import java.util.Scanner;

public class CODE_DIF_JAVA_001 {
    private HashMap<String, String> libros;
    private Scanner scanner;
    
    public void SistemaBiblioteca() {
        libros = new HashMap<>();
        scanner = new Scanner(System.in);
        inicializarLibros();
    }
    
    private void inicializarLibros() {
        libros.put("001", "El Quijote");
        libros.put("002", "Cien años de soledad");
        libros.put("003", "1984");
    }
    
    public void mostrarMenu() {
        boolean continuar = true;
        while(continuar) {
            System.out.println("\n=== SISTEMA BIBLIOTECA ===");
            System.out.println("1. Buscar libro");
            System.out.println("2. Mostrar todos");
            System.out.println("3. Salir");
            
            int opcion = scanner.nextInt();
            scanner.nextLine();
            
            switch(opcion) {
                case 1: buscarLibro(); break;
                case 2: mostrarTodos(); break;
                case 3: continuar = false; break;
                default: System.out.println("Opción inválida");
            }
        }
    }
    
    private void buscarLibro() {
        System.out.print("Ingrese código: ");
        String codigo = scanner.nextLine();
        String libro = libros.get(codigo);
        System.out.println(libro != null ? "Encontrado: " + libro : "No encontrado");
    }
    
    private void mostrarTodos() {
        libros.forEach((k, v) -> System.out.println(k + ": " + v));
    }
    
    public static void main(String[] args) {
        new CODE_DIF_JAVA_001().mostrarMenu();
    }
}
