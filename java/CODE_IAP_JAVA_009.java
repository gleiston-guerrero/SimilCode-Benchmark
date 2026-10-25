public class SeguimientoActividades {
    private static final String[] QUEHACERES = {
        "Estudiar Java",
        "Hacer ejercicio",
        "Comprar víveres",
        "Llamar a mamá",
        "Leer libro"
    };

    public static void main(String[] argumentos) {
        desplegarEncabezado();
        desplegarQuehaceres();

        int tareasCompletadas = 2;
        int totalQuehaceres = QUEHACERES.length;
        int tareasPendientes = totalQuehaceres - tareasCompletadas;

        System.out.println();
        System.out.println("Estadísticas:");
        System.out.println("Completadas: " + tareasCompletadas);
        System.out.println("Pendientes: " + tareasPendientes);
        emitirVeredicto(tareasCompletadas, tareasPendientes);
    }

    private static void desplegarEncabezado() {
        System.out.println("=== LISTA DE TAREAS ===");
    }

    private static void desplegarQuehaceres() {
        int numero = 1;
        for (String quehacer : QUEHACERES) {
            System.out.println(numero + ". " + quehacer);
            numero++;
        }
    }

    private static void emitirVeredicto(int tareasCompletadas, int tareasPendientes) {
        if (tareasCompletadas > tareasPendientes) {
            System.out.println("¡Buen progreso!");
        } else {
            System.out.println("Sigue trabajando");
        }
    }
}
