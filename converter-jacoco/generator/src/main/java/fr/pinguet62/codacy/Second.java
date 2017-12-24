package fr.pinguet62.codacy;

public class Second {

    static void doNothing(Object arg) {
        if (arg instanceof Number) {
            System.out.println("1...");
            System.out.println("2...");
            System.out.println("3...");
            System.out.println("4...");
            System.out.println("5...");
        }
        System.out.println("Ok");
    }

}
