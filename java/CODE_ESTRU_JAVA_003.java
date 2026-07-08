package Java.Estructural;

public class CODE_ESTRU_JAVA_003 {
    public static void main(String[] args) {
        String[] nombres = {"Carlos", "Ana", "Pedro", "Maria", "Juan", "Sofia", "Luis"};
        int n = nombres.length;
        
        for(int i = 0; i < n-1; i++) {
            for(int j = 0; j < n-i-1; j++) {
                if(nombres[j].compareTo(nombres[j+1]) > 0) {
                    String temp = nombres[j];
                    nombres[j] = nombres[j+1];
                    nombres[j+1] = temp;
                }
            }
        }
        
        System.out.print("Nombres ordenados: ");
        for(String nombre : nombres) {
            System.out.print(nombre + " ");
        }
    }
}