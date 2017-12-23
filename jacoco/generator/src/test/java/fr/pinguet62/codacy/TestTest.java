package fr.pinguet62.codacy;

import org.junit.Test;

public class TestTest {

    @Test
    public void first() {
        First.checkPositive(42);
    }

    @Test
    public void second() {
        Second.doNothing("direct");
    }

}
