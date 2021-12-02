use std::fs;

enum Direction {
    Forward,
    Up,
    Down,
}

struct Command {
    direction: Direction,
    step: u32,
}

impl Command {
    fn from_row(row: &str) -> Result<Self, String> {
        // Example row: 'forward 4'.
        let mut splitter = row.split(" ");
        let direction = splitter.next().unwrap();
        let step = splitter.next().unwrap().parse::<u32>().unwrap();
        match direction {
            "forward" => Ok(Command {
                direction: Direction::Forward,
                step: step,
            }),
            "up" => Ok(Command {
                direction: Direction::Up,
                step: step,
            }),
            "down" => Ok(Command {
                direction: Direction::Down,
                step: step,
            }),
            _ => Err(direction.to_string()),
        }
    }
}

impl std::fmt::Debug for Direction {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        match *self {
            Direction::Up => write!(f, "Direction(Up)"),
            Direction::Forward => write!(f, "Direction(Forward)"),
            Direction::Down => write!(f, "Direction(Down)"),
        }
    }
}

impl std::fmt::Debug for Command {
    fn fmt(&self, f: &mut std::fmt::Formatter) -> std::fmt::Result {
        write!(
            f,
            "Command(direction={:?}, step={})",
            self.direction, self.step
        )
    }
}

fn read_input(filename: &str) -> Vec<Command> {
    let content = fs::read_to_string(filename).expect("Something went wrong reading the file");
    content
        .trim() // Trim leading and trailing whitespaces.
        .split("\n") // Split by newline.
        .map(|x| Command::from_row(x).unwrap()) // For every element, create Command struct.
        .collect() // Collect all values, because map applies lazily.
}

fn solve1(commands: &Vec<Command>) -> u32 {
    let mut horizontal_pos = 0;
    let mut vertical_pos = 0;
    for command in commands {
        if matches!(command.direction, Direction::Up) {
            vertical_pos = vertical_pos - command.step;
        } else if matches!(command.direction, Direction::Down) {
            vertical_pos = vertical_pos + command.step;
        } else {
            horizontal_pos = horizontal_pos + command.step;
        }
    }
    return horizontal_pos * vertical_pos;
}

fn solve2(commands: &Vec<Command>) -> u32 {
    // down X increases your aim by X units.
    // up X decreases your aim by X units.
    // forward X does two things:
    // It increases your horizontal position by X units.
    // It increases your depth by your aim multiplied by X.
    let mut aim = 0;
    let mut horizontal_pos = 0;
    let mut vertical_pos = 0;
    for command in commands {
        if matches!(command.direction, Direction::Up) {
            aim = aim - command.step;
        } else if matches!(command.direction, Direction::Down) {
            aim = aim + command.step;
        } else {
            horizontal_pos = horizontal_pos + command.step;
            vertical_pos = vertical_pos + aim * command.step;
        }
    }
    return horizontal_pos * vertical_pos;
}

fn main() {
    let commands = read_input("input.txt");
    // println!("{:?}", commands);

    let solution1 = solve1(&commands);
    assert!(solution1 == 1727835); // That's the expected value for my input set.
    println!("Solution 1: {}", solution1);

    let solution2 = solve2(&commands);
    assert!(solution1 == 1544000595); // That's the expected value for my input set.
    println!("Solution 2: {}", solution2);
}
