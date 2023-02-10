public class Program
{
    public static void Main(string[] args)
    {
        // Display the number of command line arguments.
        Console.WriteLine("Number of arguments: {0}", args.Length);

        for (int i = 0; i < args.Length; i++)
        {
            Console.WriteLine("{0}. argument: {1}", i, args[i]);
        }
    }
}