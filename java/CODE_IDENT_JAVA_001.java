package Java.Idéntico;

public class CODE_IDENT_JAVA_001 {
    public static void main(String[] args) {
        int[] calificaciones = {85, 90, 78, 92, 88};
        int suma = 0;
        
        for(int i = 0; i < calificaciones.length; i++) {
            suma += calificaciones[i];
        }
        
        double promedio = suma / (double)calificaciones.length;
        
        if(promedio >= 90) {
            System.out.println("Excelente: " + promedio);
        } else if(promedio >= 80) {
            System.out.println("Bueno: " + promedio);
        } else {
            System.out.println("Regular: " + promedio);
        }
    }
}