use std::fs;

fn bin_str_to_int(bin_str: &str) -> u32 {
    isize::from_str_radix(bin_str, 2).unwrap() as u32
}

fn read_input(filename: &str) -> Vec<u32> {
    let content = fs::read_to_string(filename).expect("Something went wrong reading the file");
    content
        .trim() // Trim leading and trailing whitespaces.
        .split("\n") // Split by newline.
        .map(|x| bin_str_to_int(x)) // For every element, cast from binary string to int.
        .collect() // Collect all values, because map applies lazily.
}

fn get_bit_at(input: u32, n: u8) -> u32 {
    // Taken from https://www.reddit.com/r/rust/comments/3xgeo0/comment/cy4ei5n/?utm_source=share&utm_medium=web2x&context=3
    (input & (1 << n) != 0) as u32
}

fn get_majority_bit_at(inputs: &Vec<u32>, n: u8) -> u32 {
    // Take the mean of all inputs and determine whether it's greater than 0.5.
    let bit_at_sum = inputs.iter().map(|x| get_bit_at(*x, n)).sum::<u32>() as f32;
    (bit_at_sum / (inputs.len() as f32) >= 0.5) as u32
}

fn solve1(diagnostics: &Vec<u32>) -> u32 {
    // All binary strings in the input file have 12 digits.
    let n_digits = 12;

    let mut gamma_rate: u32 = 0;
    for n in 0..12 {
        gamma_rate = gamma_rate + get_majority_bit_at(&diagnostics, n) * u32::pow(2, n.into());
    }

    let epsilon_rate = !gamma_rate & bin_str_to_int(&"1".repeat(n_digits));
    gamma_rate * epsilon_rate
}

fn solve2(diagnostics: &Vec<u32>) -> u32 {
    // The bit criteria depends on which type of rating value you want to find:
    // To find oxygen generator rating, determine the most common value (0 or 1) in the current bit position, and keep only numbers with that bit in that position. If 0 and 1 are equally common, keep values with a 1 in the position being considered.
    // To find CO2 scrubber rating, determine the least common value (0 or 1) in the current bit position, and keep only numbers with that bit in that position. If 0 and 1 are equally common, keep values with a 0 in the position being considered.
    let mut remaining_diagnostics = diagnostics.clone();
    for n in (0..12).rev() {
        let majority_bit = get_majority_bit_at(&remaining_diagnostics, n);
        remaining_diagnostics.retain(|d| get_bit_at(*d, n) == majority_bit);
        if remaining_diagnostics.len() == 1 {
            break;
        }
    }
    let oxygen_rating = remaining_diagnostics.into_iter().nth(0).unwrap();
    remaining_diagnostics = diagnostics.clone();
    for n in (0..12).rev() {
        let majority_bit = 1 - get_majority_bit_at(&remaining_diagnostics, n);
        remaining_diagnostics.retain(|d| get_bit_at(*d, n) == majority_bit);
        if remaining_diagnostics.len() == 1 {
            break;
        }
    }
    let co2_rating = remaining_diagnostics.into_iter().nth(0).unwrap();
    co2_rating * oxygen_rating
}

fn main() {
    let diagnostics = read_input("input.txt");
    // println!("{:?}", diagnostics);

    let solution1 = solve1(&diagnostics);
    assert!(solution1 == 1082324);
    println!("Solution 1: {}", solution1);

    let solution2 = solve2(&diagnostics);
    assert!(solution2 == 1353024);
    println!("Solution 2: {:?}", solution2);
}
