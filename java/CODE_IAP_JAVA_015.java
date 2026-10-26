import java.util.ArrayList;
import java.util.List;
import java.util.Scanner;

/**
 * Gestor sencillo de pendientes en consola.
 * Permite almacenar hasta un maximo fijo de anotaciones.
 */
public class GestorPendientes {

    /** Cantidad maxima de anotaciones admitidas. */
    private static final int CUPO = 10;

    private final List<String> anotaciones = new ArrayList<>();
    private final Scanner lector;

    private GestorPendientes(Scanner lector) {
        this.lector = lector;
    }

    public static void main(String[] args) {
        Scanner entrada = new Scanner(System.in);
        new GestorPendientes(entrada).ejecutar();
        entrada.close();
    }

    /* Bucle principal: se repite hasta que el usuario decide terminar. */
    private void ejecutar() {
        boolean seguir = true;
        do {
            pintarMenu();
            int eleccion = leerEntero();
            switch (eleccion) {
                case 1:
                    registrar();
                    break;
                case 2:
                    listar();
                    break;
                case 3:
                    System.out.println("¡Hasta luego!");
                    seguir = false;
                    break;
                default:
                    System.out.println("Opción inválida");
            }
        } while (seguir);
    }

    private void pintarMenu() {
        String[] renglones = {
            "\n--- LISTA DE TAREAS ---",
            "1. Agregar tarea",
            "2. Mostrar tareas",
            "3. Salir"
        };
        for (String renglon : renglones) {
            System.out.println(renglon);
        }
        System.out.print("Seleccione una opción: ");
    }

    /* Toma un numero y descarta el resto de la linea. */
    private int leerEntero() {
        int valor = lector.nextInt();
        lector.nextLine();
        return valor;
    }

    private void registrar() {
        if (anotaciones.size() >= CUPO) {
            System.out.println("Lista llena!");
            return;
        }
        System.out.print("Ingrese la tarea: ");
        anotaciones.add(lector.nextLine());
        System.out.println("Tarea agregada!");
    }

    private void listar() {
        System.out.println("\n--- TAREAS REGISTRADAS ---");
        if (anotaciones.isEmpty()) {
            System.out.println("No hay tareas registradas");
            return;
        }
        int posicion = 0;
        while (posicion < anotaciones.size()) {
            System.out.println((posicion + 1) + ". " + anotaciones.get(posicion));
            posicion++;
        }
    }
}
