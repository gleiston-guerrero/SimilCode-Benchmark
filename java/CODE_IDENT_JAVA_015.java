package Java.Idéntico;

import java.util.Scanner;

public class CODE_IDENT_JAVA_015 {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        String[] tareas = new String[10];
        int contador = 0;
        
        while (true) {
            System.out.println("\n--- LISTA DE TAREAS ---");
            System.out.println("1. Agregar tarea");
            System.out.println("2. Mostrar tareas");
            System.out.println("3. Salir");
            System.out.print("Seleccione una opción: ");
            
            int opcion = scanner.nextInt();
            scanner.nextLine(); // Consumir salto de línea
            
            if (opcion == 1) {
                if (contador < 10) {
                    System.out.print("Ingrese la tarea: ");
                    tareas[contador] = scanner.nextLine();
                    contador++;
                    System.out.println("Tarea agregada!");
                } else {
                    System.out.println("Lista llena!");
                }
            } else if (opcion == 2) {
                System.out.println("\n--- TAREAS REGISTRADAS ---");
                if (contador == 0) {
                    System.out.println("No hay tareas registradas");
                } else {
                    for (int i = 0; i < contador; i++) {
                        System.out.println((i + 1) + ". " + tareas[i]);
                    }
                }
            } else if (opcion == 3) {
                System.out.println("¡Hasta luego!");
                break;
            } else {
                System.out.println("Opción inválida");
            }
        }
        scanner.close();
    }
}
