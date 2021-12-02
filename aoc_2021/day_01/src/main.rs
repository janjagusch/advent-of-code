use std::fs;

fn read_input(filename: String) -> Vec<u32> {
    let content = fs::read_to_string(filename).expect("Something went wrong reading the file");
    content
        .trim() // Trim leading and trailing whitespaces.
        .split("\n") // Split by newline.
        .map(|x| x.parse::<u32>().unwrap()) // For every element, cast to u32.
        .collect() // Collect all values, because map applies lazily.
}


fn solve1(depths: Vec<u32>) -> u32 {
    let mut deeper_than_previous_count = 0;
    let mut previous_depth = 0;  // Assumes that none of the actual depths is 0.
    for depth in &depths {
        if depth > &previous_depth && previous_depth > 0 {
            deeper_than_previous_count = deeper_than_previous_count + 1;
        }
        previous_depth = *depth;  // I don't fully understand why the * is required.
    };
    deeper_than_previous_count
}


fn main() {
    // --snip--
    let filename = "input.txt".to_string();
    println!("In file {}", filename);

    let depths = read_input(filename);

    let solution1 = solve1(depths);
    assert!(solution1 == 1400);  // The expected solution on my input set if 1400.
    println!("Solution 1: {}", solution1);
}
