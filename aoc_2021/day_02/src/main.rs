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
            "forward" => Ok(Command{direction: Direction::Forward, step: step}),
            "up" => Ok(Command{direction: Direction::Up, step: step}),
            "down" => Ok(Command{direction: Direction::Down, step: step}),
            _ => Err(direction.to_string()),
        }
    }
}

impl std::fmt::Display for Direction {
    fn fmt(&self, f: &mut std::fmt::Formatter) -> std::fmt::Result {
        match *self {
            Direction::Up => write!(f, "Direction(Up)"),
            Direction::Forward => write!(f, "Direction(Forward)"),
            Direction::Down => write!(f, "Direction(Down)"),
        }
    }
}

impl std::fmt::Display for Command {
    fn fmt(&self, f: &mut std::fmt::Formatter) -> std::fmt::Result {
        write!(f, "Command(direction={}, step={})", self.direction, self.step)
    }
}

fn read_input(filename: &str) -> () {
    let content = fs::read_to_string(filename).expect("Something went wrong reading the file");
    for row in content.trim().split("\n") {
        let command = Command::from_row(row).expect("Shit.");
        println!("{}", command);
    }
}

fn main() {
    let input = read_input("input.txt");
}
