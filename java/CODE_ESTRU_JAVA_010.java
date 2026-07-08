package Java.Estructural;

public class CODE_ESTRU_JAVA_010 {
    public static void main(String[] args) {
        String[][] puntuaciones = {{"Ana", "85", "90"}, {"Bob", "78", "85"}, {"Eva", "92", "88"}};
        int filas = puntuaciones.length;
        int columnas = puntuaciones[0].length;
        String[][] reorganizada = new String[columnas][filas];
        
        System.out.println("Tabla original (Estudiantes):");
        for(int i = 0; i < filas; i++) {
            for(int j = 0; j < columnas; j++) {
                System.out.print(puntuaciones[i][j] + "\t");
            }
            System.out.println();
        }
        
        // Reorganizar por materias
        for(int i = 0; i < filas; i++) {
            for(int j = 0; j < columnas; j++) {
                reorganizada[j][i] = puntuaciones[i][j];
            }
        }
        
        System.out.println("\nTabla reorganizada (Por materias):");
        for(int i = 0; i < columnas; i++) {
            for(int j = 0; j < filas; j++) {
                System.out.print(reorganizada[i][j] + "\t");
            }
            System.out.println();
        }
    }
}