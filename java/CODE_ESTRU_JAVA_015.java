package Java.Estructural;

import java.util.Scanner;

public class CODE_ESTRU_JAVA_015 {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        String[] nombres = new String[10];
        String[] telefonos = new String[10];
        int contador = 0;
        
        while (true) {
            System.out.println("\n--- REGISTRO DE CONTACTOS ---");
            System.out.println("1. Agregar contacto");
            System.out.println("2. Mostrar contactos");
            System.out.println("3. Salir");
            System.out.print("Seleccione una opción: ");
            
            int opcion = scanner.nextInt();
            scanner.nextLine();
            
            if (opcion == 1) {
                if (contador < 10) {
                    System.out.print("Ingrese el nombre: ");
                    nombres[contador] = scanner.nextLine();
                    System.out.print("Ingrese el teléfono: ");
                    telefonos[contador] = scanner.nextLine();
                    contador++;
                    System.out.println("Contacto agregado!");
                } else {
                    System.out.println("Agenda llena!");
                }
            } else if (opcion == 2) {
                System.out.println("\n--- CONTACTOS GUARDADOS ---");
                if (contador == 0) {
                    System.out.println("No hay contactos registrados");
                } else {
                    for (int i = 0; i < contador; i++) {
                        System.out.println((i + 1) + ". " + nombres[i] + " - " + telefonos[i]);
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