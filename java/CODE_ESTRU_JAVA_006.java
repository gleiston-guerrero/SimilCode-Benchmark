package Java.Estructural;

public class CODE_ESTRU_JAVA_006 {
    public static void main(String[] args) {
        String[] contactos = {"Ana", "Carlos", "Diana", "Eduardo", "Fernanda", "Gabriel", "Helena"};
        String nombreBuscado = "Eduardo";
        boolean existe = false;
        int indice = -1;
        
        for(int i = 0; i < contactos.length; i++) {
            if(contactos[i].equals(nombreBuscado)) {
                existe = true;
                indice = i;
                break;
            }
        }
        
        if(existe) {
            System.out.println("Contacto " + nombreBuscado + " encontrado en posición: " + indice);
        } else {
            System.out.println("Contacto " + nombreBuscado + " no encontrado");
        }
    }
}