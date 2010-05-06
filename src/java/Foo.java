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


class Tuple
{
    public static Vector make(Object ... elems)
    {
        Vector v = new Vector();
        for (Object e : elems) {
            v.add(e);
        }
        return v;
    }
}


public class Foo
{
    public static void main(String[] args)
    {
        HashMap map = new HashMap();
        
        map.put("foo", "bar");
        map.put(1, 2);
        map.put(true, "argh");
        System.out.println(map.get("foo"));
        System.out.println(map.get(1));
        System.out.println(map.get(true));
        
        Vector v = new Vector();
        
        v.add("foo");
        v.add(123);
        v.add(true);
        
        
        for (Object i : v) {
            System.out.println(i);
            
        }

    }

}


