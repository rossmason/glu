import java.util.HashMap;
import java.util.Vector;

/*
 * $Id$
 * --------------------------------------------------------------------------------------
 * Copyright (c) MuleSource, Inc.  All rights reserved.  http://www.mulesource.com
 *
 * The software in this package is published under the terms of the CPAL v1.0
 * license, a copy of which has been included with this distribution in the
 * LICENSE.txt file.
 */


class A
{
    private int DEFAULT = 1;
    
    public     int a;
    protected  int b;
    
    public A()
    {
        a = DEFAULT;
        b = DEFAULT;
    }
    
    public A(int x)
    {
        a = x;
        b = x;
    }
    
    public String x()
    {
        return "A";
    }
    
    public int getA()
    {
        return a;
    }
    
    public void blah()
    {
        System.out.println("A: " + getA());
        System.out.println("B: " + this.b);
        System.out.println("X: " + x());
    }
}

class B extends A
{
    /*
    public     int a;
    protected  int b;
    private    int c;
    */
    private static int DEFAULT = 2;
    
    public B()
    {
        super(DEFAULT);
    }
    
    public String x()
    {
        return "B";
    }
}


public class Foo
{
    public static void main(String[] args)
    {
        System.out.println("------------------ A via a");
        A a = new A();
        a.blah();
        
        System.out.println("------------------ B via b");
        B b = new B();
        b.blah();
        
        System.out.println("------------------ B via a");
        a = new B();
        a.blah();
    }

}


