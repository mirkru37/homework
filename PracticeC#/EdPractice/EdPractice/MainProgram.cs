using System;
using System.Collections;
using System.Collections.Generic;
using System.Linq;
using System.Threading;

namespace EdPractice
{
    internal class MainProgram
    {
        public static void Main(string[] args)
        {
            ClassCollection<Freelancer> cl = new ClassCollection<Freelancer>();
            while (true)
            {
                Console.WriteLine(@"Input number of option:
    1. Search
    2. Sort by parameter
    3. Delete by ID
    4. Add new
    5. Read from file
    6. Write to file
    7. Edit by ID
    8. Show all
    9. Exit");
                int num;
                try
                {
                    num = Int32.Parse(Console.ReadLine());
                }
                catch (FormatException e)
                {
                    Console.WriteLine(e.Message);
                    continue;
                }

                if (num == 1)
                {
                    Console.WriteLine("Input search param:");
                    string val = Console.ReadLine();
                    ClassCollection<Freelancer> nc = cl.Search(val);
                    nc.PrintAll();
                }else if (num == 2)
                {
                    try
                    {
                        Console.WriteLine("Input sort param:");
                        string val = Console.ReadLine();
                        cl.SortBy(val);
                        cl.PrintAll();
                    }
                    catch (NullReferenceException)
                    {
                        Console.WriteLine("Wrong!");
                    }
                }else if (num == 3)
                {
                    Console.WriteLine("Input Id:");
                    string val = Console.ReadLine();
                    if (!cl.Delete(val))
                    {
                        Console.WriteLine("Wrong");
                    }
                }else if (num == 4)
                {
                    Console.WriteLine("Input values");
                    string str = "Order: ";
                    foreach (var field in Freelancer.Fields)
                    {
                        str += field + " ";
                    }
                    Console.WriteLine(str);
                    string val = Console.ReadLine(); 
                    List<Hashtable> errors = cl.AddFromLine(val);
                    if (errors.Count != 0)
                    {
                        foreach (var error in errors)
                        {
                            foreach (var key in error.Keys)
                            {
                                Console.WriteLine($"{key}:{error[key]}");                
                            }
                        }
                    }
                }else if (num == 5)
                {
                    Console.WriteLine("Input file path");
                    string val = Console.ReadLine(); 
                    List<Hashtable> errors = cl.AddFromFile(val);
                    if (errors.Count != 0)
                    {
                        foreach (var error in errors)
                        {
                            foreach (var key in error.Keys)
                            {
                                Console.WriteLine($"{key}:{error[key]}");                
                            }
                        }
                    }
                }else if (num == 6)
                {
                    Console.WriteLine("Input file path");
                    string val = Console.ReadLine(); 
                    List<Hashtable> errors = cl.WriteToFile(val);
                    if (errors.Count != 0)
                    {
                        foreach (var error in errors)
                        {
                            foreach (var key in error.Keys)
                            {
                                Console.WriteLine($"{key}:{error[key]}");                
                            }
                        }
                    }
                }else if (num == 7)
                {
                    Console.WriteLine("Input Id:");
                    string val = Console.ReadLine();
                    List<Hashtable> errors = cl.Edit(val);
                    if (errors.Count != 0)
                    {
                        foreach (var error in errors)
                        {
                            foreach (var key in error.Keys)
                            {
                                Console.WriteLine($"{key}:{error[key]}");                
                            }
                        }
                    }
                }else if (num == 8)
                {
                    cl.PrintAll();
                }else if (num == 9)
                {
                    break;
                }
                else
                {
                    Console.WriteLine("Wrong");
                }

            }
        }
    }
}