package Java.Idéntico;

/**
 * Pequeño ejercicio: ordenación ascendente de una colección de enteros
 * y volcado del resultado por consola.
 */
public class OrdenadorDeValores {

    /** Intercambia dos posiciones dentro del arreglo recibido. */
    private static void permutar(int[] datos, int posA, int posB) {
        int reserva = datos[posA];
        datos[posA] = datos[posB];
        datos[posB] = reserva;
    }

    /**
     * Ordena de menor a mayor recorriendo el arreglo con un while externo
     * y repitiendo pasadas mientras siga habiendo intercambios.
     */
    private static void acomodarAscendente(int[] datos) {
        int limite = datos.length - 1;

        while (limite > 0) {
            boolean huboCambio = false;
            int cursor = 0;

            while (cursor < limite) {
                if (datos[cursor] > datos[cursor + 1]) {
                    permutar(datos, cursor, cursor + 1);
                    huboCambio = true;
                }
                cursor++;
            }

            if (!huboCambio) {
                break;
            }
            limite--;
        }
    }

    /** Construye la cadena con los valores separados por un espacio. */
    private static String componerSalida(int[] datos) {
        StringBuilder acumulador = new StringBuilder();
        int indice = datos.length - 1;

        // Se recorre al revés y se inserta al principio para mantener el orden
        while (indice >= 0) {
            acumulador.insert(0, datos[indice] + " ");
            indice--;
        }
        return acumulador.toString();
    }

    public static void main(String[] args) {
        int[] coleccion = new int[] { 64, 34, 25, 12, 22, 11, 90 };

        acomodarAscendente(coleccion);

        System.out.print("Números ordenados: ");
        System.out.print(componerSalida(coleccion));
    }
}
