"""The Game of Hog."""

#Fill in your email address and that of your partner
partner_one_email = "nyathiblesing2004@gmail.com"
partner_two_email = "h230564t@hit.ac.zw"
assignment = "hog"

from dice import four_sided, six_sided, make_test_dice
from ucb import main, trace, log_current_line, interact

GOAL_SCORE = 100 # The goal of Hog is to score 100 points.

######################
# Phase 1: Simulator #
######################

# Taking turns  

def roll_dice(num_rolls, dice=six_sided):
    """Roll DICE for NUM_ROLLS times.  Return either the sum of the outcomes,
    or 1 if a 1 is rolled (Pig out). This calls DICE exactly NUM_ROLLS times.

    num_rolls:  The number of dice rolls that will be made; at least 1.
    dice:       A zero-argument function that returns an integer outcome.
    """
    # These assert statements ensure that num_rolls is a positive integer.
    assert type(num_rolls) == int, 'num_rolls must be an integer.'
    assert num_rolls > 0, 'Must roll at least once.'

    # BEGIN Question 1

    total = 0
    pig_out = False
    rolls = 0
    
    while rolls < num_rolls:
        roll = dice()
        if roll == 1:
            pig_out = True
        total += roll
        rolls += 1
    
    if pig_out:
        return 1
    else:
        return total

    # END Question 1

    
def take_turn(num_rolls, opponent_score, dice=six_sided):
    """Simulate a turn rolling NUM_ROLLS dice, which may be 0 (Free bacon).

    num_rolls:       The number of dice rolls that will be made.
    opponent_score:  The total score of the opponent.
    dice:            A function of no args that returns an integer outcome.
    """
    assert type(num_rolls) == int, 'num_rolls must be an integer.'
    assert num_rolls >= 0, 'Cannot roll a negative number of dice.'
    assert num_rolls <= 10, 'Cannot roll more than 10 dice.'
    assert opponent_score < 100, 'The game should be over.'

    if num_rolls == 0:
        # Free bacon rule
        d1 = opponent_score // 10
        d2 = opponent_score % 10
        score = 1 + max(d1, d2)
    else:
        # Roll the dice
        score = roll_dice(num_rolls, dice)
    
    return score

# Playing a game

def select_dice(score, opponent_score):
    """Select six-sided dice unless the sum of SCORE and OPPONENT_SCORE is a
    multiple of 7, in which case select four-sided dice (Hog wild).

    >>> select_dice(4, 24) == four_sided
    True
    >>> select_dice(16, 64) == six_sided
    True
    >>> select_dice(0, 0) == four_sided
    True
    """
#MY CODE

    if (score + opponent_score) % 7 == 0:
        return four_sided
    else:
        return six_sided

def other(who):
    """Return the other player, for a player WHO numbered 0 or 1.

    >>> other(0)
    1
    >>> other(1)
    0
    """
    return 1 - who

def play(strategy0, strategy1, goal=GOAL_SCORE):
    """Simulate a game and return the final scores of both players, with
    Player 0's score first, and Player 1's score second.

    A strategy is a function that takes two total scores as arguments
    (the current player's score, and the opponent's score), and returns a
    number of dice that the current player will roll this turn.

    strategy0:  The strategy function for Player 0, who plays first.
    strategy1:  The strategy function for Player 1, who plays second.
    """
    who = 0  # Which player is about to take a turn, 0 (first) or 1 (second)
    score, opponent_score = 0, 0
    score = [0, 0]  # Scores for Player 0 and Player 1
    dice = six_sided  # Initial dice type is six-sided
    swap = False  # Flag to track if Swine swap rule is triggered
    
    while score[0] < goal and score[1] < goal:
        current_player = who
        opponent = other(who)
        
        if who == 0:
            num_rolls = strategy0(score[who], score[opponent])
        else:
            num_rolls = strategy1(score[who], score[opponent])
        
        dice = select_dice(score[who], score[opponent])
        
        turn_score = take_turn(num_rolls, score[opponent], dice)
        score[who] += turn_score
        
        if score[current_player] == 2 * score[opponent] or score[opponent] == 2 * score[current_player]:
            score[current_player], score[opponent] = score[opponent], score[current_player]
            swap = True
        else:
            swap = False
        
        who = other(who)
    
    return score[0], score[1]
    return score, opponent_score  # You may wish to change this line.

#######################
# Phase 2: Strategies #
#######################

# Basic Strategy

BASELINE_NUM_ROLLS = 5
BACON_MARGIN = 8

def always_roll(n):
    """Return a strategy that always rolls N dice.

    A strategy is a function that takes two total scores as arguments
    (the current player's score, and the opponent's score), and returns a
    number of dice that the current player will roll this turn.

    >>> strategy = always_roll(5)
    >>> strategy(0, 0)
    5
    >>> strategy(99, 99)
    5
    """
    def strategy(score, opponent_score):
        return n
    return strategy

# Experiments

def make_averaged(fn, num_samples=1000):
    """Return a function that returns the average_value of FN when called.

    To implement this function, you will have to use *args syntax, a new Python
    feature introduced in this project.  See the project description.

    >>> dice = make_test_dice(3, 1, 5, 6)
    >>> averaged_dice = make_averaged(dice, 1000)
    >>> averaged_dice()
    3.75
    >>> make_averaged(roll_dice, 1000)(2, dice)
    6.0

    In this last example, two different turn scenarios are averaged.
    - In the first, the player rolls a 3 then a 1, receiving a score of 1.
    - In the other, the player rolls a 5 and 6, scoring 11.
    Thus, the average value is 6.0.
    """

#MY CODE

    def averaged_fn(*args):
        total = 0
        count = 0
        while count < num_samples:
            total += fn(*args)
            count += 1
        return total / num_samples
    return averaged_fn

def max_scoring_num_rolls(dice=six_sided):
    """Return the number of dice (1 to 10) that gives the highest average turn
    score by calling roll_dice with the provided DICE.  Print all averages as in
    the doctest below.  Assume that dice always returns positive outcomes.

    >>> dice = make_test_dice(3)
    >>> max_scoring_num_rolls(dice)
    1 dice scores 3.0 on average
    2 dice scores 6.0 on average
    3 dice scores 9.0 on average
    4 dice scores 12.0 on average
    5 dice scores 15.0 on average
    6 dice scores 18.0 on average
    7 dice scores 21.0 on average
    8 dice scores 24.0 on average
    9 dice scores 27.0 on average
    10 dice scores 30.0 on average
    10
    """

    #MY CODE

    num_rolls = 1
    max_average = 0
    best_num_rolls = 0
    
    while num_rolls <= 10:
        total_score = 0
        num_samples = 1000       # Number of samples to average over
        sample_count = 0
        
        while sample_count < num_samples:
            total_score += roll_dice(num_rolls, dice)
            sample_count += 1
        
        average_score = total_score / num_samples
        
        print(f"{num_rolls} dice scores {average_score} on average")
        
        if average_score > max_average:
            max_average = average_score
            best_num_rolls = num_rolls
        
        num_rolls += 1
    
    return best_num_rolls

def winner(strategy0, strategy1):
    """Return 0 if strategy0 wins against strategy1, and 1 otherwise."""
    score0, score1 = play(strategy0, strategy1)
    if score0 > score1:
        return 0
    else:
        return 1

def average_win_rate(strategy, baseline=always_roll(BASELINE_NUM_ROLLS)):
    """Return the average win rate (0 to 1) of STRATEGY against BASELINE."""
    win_rate_as_player_0 = 1 - make_averaged(winner)(strategy, baseline)
    win_rate_as_player_1 = make_averaged(winner)(baseline, strategy)
    return (win_rate_as_player_0 + win_rate_as_player_1) / 2 # Average results

def run_experiments():
    """Run a series of strategy experiments and report results."""
    if True: # Change to False when done finding max_scoring_num_rolls
        six_sided_max = max_scoring_num_rolls(six_sided)
        print('Max scoring num rolls for six-sided dice:', six_sided_max)
        four_sided_max = max_scoring_num_rolls(four_sided)
        print('Max scoring num rolls for four-sided dice:', four_sided_max)

    if False: # Change to True to test always_roll(8)
        print('always_roll(8) win rate:', average_win_rate(always_roll(8)))

    if False: # Change to True to test bacon_strategy
        print('bacon_strategy win rate:', average_win_rate(bacon_strategy))

    if False: # Change to True to test swap_strategy
        print('swap_strategy win rate:', average_win_rate(swap_strategy))

    if False: # Change to True to test final_strategy
        print('final_strategy win rate:', average_win_rate(final_strategy))

    "*** You may add additional experiments as you wish ***"

# Strategies

def bacon_strategy(score, opponent_score):
    """This strategy rolls 0 dice if that gives at least BACON_MARGIN points,
    and rolls BASELINE_NUM_ROLLS otherwise.

    >>> bacon_strategy(0, 0)
    5
    >>> bacon_strategy(70, 50)
    5
    >>> bacon_strategy(50, 70)
    0
    """

#MY CODE

BACON_MARGIN = 6            #This is just an example value
BASELINE_NUM_ROLLS = 5      # ""

def bacon_strategy(score, opponent_score):
    """This strategy rolls 0 dice if that gives at least BACON_MARGIN points,
    and rolls BASELINE_NUM_ROLLS otherwise.
    """
    #To get my opponent's score digits
    tens_digit = opponent_score // 10 #tens_digit means that i take number that represent 10s
    ones_digit = opponent_score % 10  #I take units
    
    #To determine the maximum digit of my opponent's score
    max_digit = max(tens_digit, ones_digit)
    
    bacon_score = 1 + max_digit
    
    if bacon_score >= BACON_MARGIN:
        return 0
    else:
        return BASELINE_NUM_ROLLS


def swap_strategy(score, opponent_score):
    """This strategy rolls 0 dice when it would result in a beneficial swap and
    rolls BASELINE_NUM_ROLLS if it would result in a harmful swap. It also rolls
    0 dice if that gives at least BACON_MARGIN points and rolls
    BASELINE_NUM_ROLLS otherwise.

    >>> swap_strategy(23, 60) # 23 + (1 + max(6, 0)) = 30: Beneficial swap
    0
    >>> swap_strategy(27, 18) # 27 + (1 + max(1, 8)) = 36: Harmful swap
    5
    >>> swap_strategy(50, 80) # (1 + max(8, 0)) = 9: Lots of free bacon
    0
    >>> swap_strategy(12, 12) # Baseline
    5
    """

#MY CODE

BACON_MARGIN = 6          #This is just an example.
BASELINE_NUM_ROLLS = 5    # ""

def swap_strategy(score, opponent_score):
    """This strategy rolls 0 dice when it would result in a beneficial swap and
    rolls BASELINE_NUM_ROLLS if it would result in a harmful swap. It also rolls
    0 dice if that gives at least BACON_MARGIN points and rolls
    BASELINE_NUM_ROLLS otherwise.
    """
    #To get my opponent's score digits
    tens_digit = opponent_score // 10             #I take number that represent tens
    ones_digit = opponent_score % 10              #I take units
    
    bacon_score = 1 + max(tens_digit, ones_digit) #I will get a free bacon score
    
    # Determining my opponent's score after Free Bacon
    opponent_new_score = score + bacon_score
    
    if opponent_new_score > opponent_score:       #beneficial swap
        if opponent_new_score > score:
            return 0
    
    if opponent_new_score < opponent_score:       #harmful swap  
        if opponent_new_score < score:
            return BASELINE_NUM_ROLLS
    
    if bacon_score >= BACON_MARGIN:
        return 0
    return BASELINE_NUM_ROLLS

def final_strategy(score, opponent_score):
    """Write a brief description of your final strategy.

    ***My strategy picks dice based on numbers, aiming for a big Bacon bonus, and changes the opponent's score to win***
    """
#MY CODE
BACON_MARGIN = 6                                  #Example values
BASELINE_NUM_ROLLS = 5

def final_strategy(score, opponent_score):
    """Final strategy combining various ideas to achieve a high win rate."""
    
    if score % 7 == 0 or opponent_score % 7 == 0:
        current_dice = 4
    else:
        current_dice = 6
    
    tens_digit = opponent_score // 10               #I take number that represent tens
    ones_digit = opponent_score % 10                #T takes units
    bacon_score = 1 + max(tens_digit, ones_digit)
    
    opponent_new_score = score + bacon_score        #new score after free bacon
    
    if current_dice == 4:
        # Prefer to leave the opponent with 4-sided dice
        if score + bacon_score * 2 == opponent_score:
            return 0
        if bacon_score >= BACON_MARGIN and opponent_score < score + bacon_score:
            return 0
        elif opponent_new_score > opponent_score:
            if opponent_new_score > score:
                return 0
        elif opponent_new_score < opponent_score:
            strategy


##########################
# Command Line Interface #
##########################

# Note: Functions in this section do not need to be changed.  They use features
#       of Python not yet covered in the course.

def get_int(prompt, min):
    """Return an integer greater than or equal to MIN, given by the user."""
    choice = input(prompt)
    while not choice.isnumeric() or int(choice) < min:
        print('Please enter an integer greater than or equal to', min)
        choice = input(prompt)
    return int(choice)

def interactive_dice():
    """A dice where the outcomes are provided by the user."""
    return get_int('Result of dice roll: ', 1)

def make_interactive_strategy(player):
    """Return a strategy for which the user provides the number of rolls."""
    prompt = 'Number of rolls for Player {0}: '.format(player)
    def interactive_strategy(score, opp_score):
        if player == 1:
            score, opp_score = opp_score, score
        print(score, 'vs.', opp_score)
        choice = get_int(prompt, 0)
        return choice
    return interactive_strategy

def roll_dice_interactive():
    """Interactively call roll_dice."""
    num_rolls = get_int('Number of rolls: ', 1)
    turn_total = roll_dice(num_rolls, interactive_dice)
    print('Turn total:', turn_total)

def take_turn_interactive():
    """Interactively call take_turn."""
    num_rolls = get_int('Number of rolls: ', 0)
    opp_score = get_int('Opponent score: ', 0)
    turn_total = take_turn(num_rolls, opp_score, interactive_dice)
    print('Turn total:', turn_total)

def play_interactive():
    """Interactively call play."""
    strategy0 = make_interactive_strategy(0)
    strategy1 = make_interactive_strategy(1)
    score0, score1 = play(strategy0, strategy1)
    print('Final scores:', score0, 'to', score1)

@main
def run(*args):
    """Read in the command-line argument and calls corresponding functions.

    This function uses Python syntax/techniques not yet covered in this course.
    """
    import argparse
    parser = argparse.ArgumentParser(description="Play Hog")
    parser.add_argument('--interactive', '-i', type=str,
                        help='Run interactive tests for the specified question')
    parser.add_argument('--run_experiments', '-r', action='store_true',
                        help='Runs strategy experiments')
    args = parser.parse_args()

    if args.interactive:
        test = args.interactive + '_interactive'
        if test not in globals():
            print('To use the -i option, please choose one of these:')
            print('\troll_dice', '\ttake_turn', '\tplay', sep='\n')
            exit(1)
        try:
            globals()[test]()
        except (KeyboardInterrupt, EOFError):
            print('\nQuitting interactive test')
            exit(0)
    elif args.run_experiments:
        run_experiments()
