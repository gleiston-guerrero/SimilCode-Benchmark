package Java.Original;

import java.util.Scanner;

public class GestionTareas {
    public static void main(String[] args) {
        Scanner input = new Scanner(System.in);
        String[] lista = new String[10];
        int index = 0;
        
        while (true) {
            System.out.println("\n--- LISTA DE TAREAS ---");
            System.out.println("1. Agregar tarea");
            System.out.println("2. Mostrar tareas");
            System.out.println("3. Salir");
            System.out.print("Seleccione una opción: ");
            
            int choice = input.nextInt();
            input.nextLine(); // Consumir salto de línea
            
            if (choice == 1) {
                if (index < 10) {
                    System.out.print("Ingrese la tarea: ");
                    lista[index] = input.nextLine();
                    index++;
                    System.out.println("Tarea agregada!");
                } else {
                    System.out.println("Lista llena!");
                }
            } else if (choice == 2) {
                System.out.println("\n--- TAREAS REGISTRADAS ---");
                if (index == 0) {
                    System.out.println("No hay tareas registradas");
                } else {
                    for (int i = 0; i < index; i++) {
                        System.out.println((i + 1) + ". " + lista[i]);
                    }
                }
            } else if (choice == 3) {
                System.out.println("¡Hasta luego!");
                break;
            } else {
                System.out.println("Opción inválida");
            }
        }
        input.close();
    }
}
