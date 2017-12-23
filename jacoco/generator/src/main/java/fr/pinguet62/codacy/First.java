package fr.pinguet62.codacy;

public class First {

    static boolean checkPositive(int arg) {
        if (arg < 0)
            throw new RuntimeException("arg must be positive");
        return true;
    }

}
