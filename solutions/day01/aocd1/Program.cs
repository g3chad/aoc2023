Console.WriteLine("Solving problem...");
string[] lines = System.IO.File.ReadAllLines(@"./input.txt");
var total = 0;
foreach (string line in lines)
{
    var just_digits = string.Concat(line.Where( Char.IsDigit ) );
    int first_two = Convert.ToInt32(Convert.ToString(just_digits[0]) + Convert.ToString(just_digits[^1]));
    total += first_two;
}
Console.WriteLine("Part 1: " + Convert.ToString(total));

total = 0;
foreach (string line in lines)
{
    // to do extract to a function
    var input = line.Replace("one", "o1e"); 
    input = input.Replace("two", "t2o"); 
    input = input.Replace("three", "t3hree"); 
    input = input.Replace("four", "f4our"); 
    input = input.Replace("five", "f5ive"); 
    input = input.Replace("six", "s6x"); 
    input = input.Replace("seven", "s7even"); 
    input = input.Replace("eight", "e8ght"); 
    input = input.Replace("nine", "n9ne"); 
    input = input.Replace("zero", "z0ro"); 
    var just_digits = string.Concat(input.Where( Char.IsDigit ) );
    int first_two = Convert.ToInt32(Convert.ToString(just_digits[0]) + Convert.ToString(just_digits[^1]));
    total += first_two;
}
Console.WriteLine("Part 2: " + Convert.ToString(total));
