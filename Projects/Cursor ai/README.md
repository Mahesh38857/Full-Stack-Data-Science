# 🏏 Cricket Game

An interactive cricket game built with Python and Streamlit. Play cricket against the computer with realistic batting and bowling mechanics!

## Features

### 🎮 Gameplay
- **Batting**: Choose from 5 different shot types (Defensive, Drive, Pull, Sweep, Aggressive)
- **Bowling**: Select from 4 bowling styles (Fast, Spin, Yorker, Bouncer)
- **Realistic Mechanics**: Probability-based outcomes for different shots and deliveries
- **Two Innings**: Bat first, then bowl to defend your score

### 📊 Statistics & Analytics
- Live score tracking
- Ball-by-ball commentary
- Detailed statistics (strike rate, boundaries, etc.)
- Interactive charts showing runs progression
- Shot distribution analysis

### ⚙️ Customization
- Adjustable difficulty levels (Easy, Normal, Hard)
- Configurable number of overs (1-10)
- Real-time game settings

## Installation

1. **Clone or download the project files**

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the game**:
   ```bash
   streamlit run cricket_game.py
   ```

4. **Open your browser** and navigate to the URL shown in the terminal (usually `http://localhost:8501`)

## How to Play

### 🏏 Batting Phase
1. When it's your turn to bat, you'll see 5 shot options
2. Click on any shot type to play that shot
3. Each shot has different probabilities for runs (0, 1, 2, 4, 6)
4. Your innings ends when you reach the maximum overs or lose all wickets

### 🎯 Bowling Phase
1. When bowling, choose from 4 different ball types
2. Each ball type has different probabilities for wickets and runs
3. Try to restrict the computer's scoring while taking wickets
4. The game ends when the computer reaches your score or loses all wickets

### 🏆 Winning
- **You win** if you score more runs than the computer
- **Computer wins** if it scores more runs than you
- **Tie** if both teams score the same runs

## Game Features

### Shot Types
- **Defensive**: Safe shot, lower risk, fewer boundaries
- **Drive**: Balanced shot, good for singles and doubles
- **Pull**: Aggressive shot, higher chance of boundaries
- **Sweep**: Unorthodox shot, unpredictable results
- **Aggressive**: High-risk, high-reward shot

### Bowling Types
- **Fast**: High pace, good for dot balls
- **Spin**: Tricky deliveries, higher wicket chance
- **Yorker**: Full-length delivery, high dot ball probability
- **Bouncer**: Short-pitched delivery, high wicket chance

### Difficulty Levels
- **Easy**: Higher probability of boundaries and sixes
- **Normal**: Balanced gameplay
- **Hard**: Lower probability of boundaries, more dot balls

## Technical Details

- **Framework**: Streamlit
- **Charts**: Plotly for interactive visualizations
- **Data**: Pandas for data manipulation
- **Randomization**: Python's random module for realistic outcomes

## File Structure

```
cricket-game/
├── cricket_game.py      # Main game application
├── requirements.txt      # Python dependencies
└── README.md           # This file
```

## Customization

You can modify the game by editing `cricket_game.py`:

- **Shot Probabilities**: Adjust the `shot_probabilities` dictionary in the `get_batting_result` method
- **Bowling Probabilities**: Modify the `ball_probabilities` dictionary in the `get_bowling_result` method
- **Game Settings**: Change default values for overs, wickets, etc.
- **UI Styling**: Update the CSS in the `st.markdown` section

## Troubleshooting

- **Port already in use**: Try running `streamlit run cricket_game.py --server.port 8502`
- **Dependencies not found**: Make sure you're in the correct directory and run `pip install -r requirements.txt`
- **Browser issues**: Try refreshing the page or clearing browser cache

## Enjoy Playing! 🏏

Have fun playing cricket! The game combines strategy with luck, making each match unique and exciting. 