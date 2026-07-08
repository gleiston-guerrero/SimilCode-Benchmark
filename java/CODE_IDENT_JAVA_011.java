package Java.Idéntico;

import java.util.Scanner;

public class CODE_IDENT_JAVA_011 {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        
        System.out.print("Ingrese el número de materias: ");
        int numMaterias = scanner.nextInt();
        
        double suma = 0;
        for (int i = 0; i < numMaterias; i++) {
            System.out.print("Ingrese nota " + (i + 1) + ": ");
            double nota = scanner.nextDouble();
            suma += nota;
        }
        
        double promedio = suma / numMaterias;
        System.out.println("El promedio es: " + promedio);
        
        if (promedio >= 3.0) {
            System.out.println("APROBADO");
        } else {
            System.out.println("REPROBADO");
        }
        
        scanner.close();
    }
}