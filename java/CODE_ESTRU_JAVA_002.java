package Java.Estructural;

public class CODE_ESTRU_JAVA_002 {
    public static void main(String[] args) {
        String email = "usuario@dominio.com";
        boolean tieneArroba = false;
        boolean tienePunto = false;
        boolean tieneTexto = false;
        
        for(int i = 0; i < email.length(); i++) {
            char c = email.charAt(i);
            if(c == '@') tieneArroba = true;
            if(c == '.') tienePunto = true;
            if((c >= 'a' && c <= 'z') || (c >= 'A' && c <= 'Z')) tieneTexto = true;
        }
        
        if(email.length() >= 5 && tieneArroba && tienePunto && tieneTexto) {
            System.out.println("Email válido");
        } else {
            System.out.println("Email inválido");
        }
    }
}