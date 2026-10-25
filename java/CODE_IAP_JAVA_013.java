import java.util.ArrayList;
import java.util.List;
import java.util.Scanner;

public class AnalizadorNumerico {

    private static final Scanner LECTOR = new Scanner(System.in);

    public static void main(String[] argumentos) {
        int cantidad = preguntarCantidad();
        List<Integer> ingresados = obtenerValores(cantidad);
        int valorMayor = hallarMaximo(ingresados);
        mostrarResultado(valorMayor);
        LECTOR.close();
    }

    private static int preguntarCantidad() {
        System.out.print("¿Cuántos números va a ingresar? ");
        return LECTOR.nextInt();
    }

    private static List<Integer> obtenerValores(int total) {
        List<Integer> datos = new ArrayList<>();
        int contador = 1;

        while (contador <= total) {
            System.out.print("Número " + contador + ": ");
            datos.add(LECTOR.nextInt());
            contador++;
        }

        return datos;
    }

    private static int hallarMaximo(List<Integer> datos) {
        int maximo = datos.get(0);

        for (int actual : datos) {
            if (actual > maximo) {
                maximo = actual;
            }
        }

        return maximo;
    }

    private static void mostrarResultado(int maximo) {
        System.out.println("El número máximo es: " + maximo);
    }
}
