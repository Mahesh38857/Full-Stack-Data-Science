import streamlit as st
import random
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import json

# Page configuration
st.set_page_config(
    page_title="Cricket Game",
    page_icon="🏏",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        color: #1f77b4;
        margin-bottom: 2rem;
    }
    .score-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    .game-button {
        margin: 0.5rem;
    }
    .stats-container {
        display: flex;
        justify-content: space-between;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

class CricketGame:
    def __init__(self):
        self.reset_game()
    
    def reset_game(self):
        """Reset the game state"""
        self.player_score = 0
        self.computer_score = 0
        self.player_wickets = 0
        self.computer_wickets = 0
        self.overs = 0
        self.balls = 0
        self.max_overs = 5
        self.max_wickets = 10
        self.game_history = []
        self.current_innings = "player"
        self.game_over = False
        self.player_balls_faced = 0
        self.computer_balls_faced = 0
        self.player_fours = 0
        self.player_sixes = 0
        self.computer_fours = 0
        self.computer_sixes = 0
    
    def get_batting_result(self, shot_type, difficulty="normal"):
        """Calculate batting result based on shot type and difficulty"""
        shot_probabilities = {
            "Defensive": {"0": 0.4, "1": 0.3, "2": 0.2, "4": 0.08, "6": 0.02},
            "Drive": {"0": 0.2, "1": 0.3, "2": 0.25, "4": 0.2, "6": 0.05},
            "Pull": {"0": 0.15, "1": 0.25, "2": 0.3, "4": 0.25, "6": 0.05},
            "Sweep": {"0": 0.3, "1": 0.25, "2": 0.25, "4": 0.15, "6": 0.05},
            "Aggressive": {"0": 0.1, "1": 0.2, "2": 0.25, "4": 0.3, "6": 0.15}
        }
        
        # Adjust probabilities based on difficulty
        if difficulty == "easy":
            for shot in shot_probabilities:
                shot_probabilities[shot]["6"] += 0.05
                shot_probabilities[shot]["4"] += 0.1
                shot_probabilities[shot]["0"] -= 0.15
        elif difficulty == "hard":
            for shot in shot_probabilities:
                shot_probabilities[shot]["0"] += 0.1
                shot_probabilities[shot]["6"] -= 0.05
                shot_probabilities[shot]["4"] -= 0.05
        
        # Get probabilities for the selected shot
        probs = shot_probabilities[shot_type]
        
        # Random selection based on probabilities
        rand = random.random()
        cumulative = 0
        for runs, prob in probs.items():
            cumulative += prob
            if rand <= cumulative:
                return int(runs)
        
        return 0
    
    def get_bowling_result(self, ball_type):
        """Calculate bowling result"""
        ball_probabilities = {
            "Fast": {"wicket": 0.15, "dot": 0.3, "runs": 0.55},
            "Spin": {"wicket": 0.2, "dot": 0.25, "runs": 0.55},
            "Yorker": {"wicket": 0.25, "dot": 0.4, "runs": 0.35},
            "Bouncer": {"wicket": 0.3, "dot": 0.2, "runs": 0.5}
        }
        
        probs = ball_probabilities[ball_type]
        rand = random.random()
        
        if rand < probs["wicket"]:
            return "W"
        elif rand < probs["wicket"] + probs["dot"]:
            return 0
        else:
            return random.randint(1, 6)
    
    def play_ball(self, shot_type=None, ball_type=None):
        """Play a single ball"""
        if self.game_over:
            return
        
        if self.current_innings == "player":
            # Player batting
            if shot_type is None:
                shot_type = random.choice(["Defensive", "Drive", "Pull", "Sweep", "Aggressive"])
            
            runs = self.get_batting_result(shot_type)
            self.player_score += runs
            self.player_balls_faced += 1
            
            if runs == 4:
                self.player_fours += 1
            elif runs == 6:
                self.player_sixes += 1
            
            self.game_history.append({
                "innings": "player",
                "shot": shot_type,
                "runs": runs,
                "ball": self.balls + 1,
                "over": self.overs + 1
            })
            
        else:
            # Computer batting
            ball_type = ball_type or random.choice(["Fast", "Spin", "Yorker", "Bouncer"])
            result = self.get_bowling_result(ball_type)
            
            if result == "W":
                self.computer_wickets += 1
                runs = 0
            else:
                runs = result
                self.computer_score += runs
                self.computer_balls_faced += 1
                
                if runs == 4:
                    self.computer_fours += 1
                elif runs == 6:
                    self.computer_sixes += 1
            
            self.game_history.append({
                "innings": "computer",
                "ball_type": ball_type,
                "runs": runs,
                "ball": self.balls + 1,
                "over": self.overs + 1
            })
        
        # Update ball count
        self.balls += 1
        if self.balls == 6:
            self.balls = 0
            self.overs += 1
        
        # Check game end conditions
        self.check_game_end()
    
    def check_game_end(self):
        """Check if the game should end"""
        if self.current_innings == "player":
            if self.overs >= self.max_overs or self.player_wickets >= self.max_wickets:
                self.current_innings = "computer"
                self.overs = 0
                self.balls = 0
        else:
            if (self.overs >= self.max_overs or self.computer_wickets >= self.max_wickets or 
                self.computer_score > self.player_score):
                self.game_over = True
    
    def get_match_summary(self):
        """Get match summary"""
        if not self.game_over:
            return None
        
        if self.player_score > self.computer_score:
            winner = "Player"
            margin = self.player_score - self.computer_score
        elif self.computer_score > self.player_score:
            winner = "Computer"
            margin = self.computer_score - self.player_score
        else:
            winner = "Tie"
            margin = 0
        
        return {
            "winner": winner,
            "margin": margin,
            "player_score": self.player_score,
            "computer_score": self.computer_score,
            "player_wickets": self.player_wickets,
            "computer_wickets": self.computer_wickets
        }

# Initialize game
if 'game' not in st.session_state:
    st.session_state.game = CricketGame()

game = st.session_state.game

# Main header
st.markdown('<h1 class="main-header">🏏 Cricket Game</h1>', unsafe_allow_html=True)

# Sidebar for game controls
with st.sidebar:
    st.header("Game Controls")
    
    if st.button("New Game", key="new_game"):
        game.reset_game()
        st.rerun()
    
    st.markdown("---")
    st.header("Game Settings")
    
    difficulty = st.selectbox(
        "Difficulty Level",
        ["easy", "normal", "hard"],
        index=1
    )
    
    max_overs = st.slider("Max Overs", 1, 10, 5)
    game.max_overs = max_overs

# Main game area
col1, col2 = st.columns([2, 1])

with col1:
    # Score display
    st.markdown('<div class="score-card">', unsafe_allow_html=True)
    st.subheader("📊 Live Score")
    
    col_score1, col_score2 = st.columns(2)
    
    with col_score1:
        st.metric("Player", f"{game.player_score}/{game.player_wickets}")
        st.caption(f"Overs: {game.overs}.{game.balls}")
    
    with col_score2:
        st.metric("Computer", f"{game.computer_score}/{game.computer_wickets}")
        st.caption(f"Target: {game.player_score + 1}" if game.current_innings == "computer" else "")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Gameplay area
    if not game.game_over:
        if game.current_innings == "player":
            st.subheader("🎯 Your Turn - Batting")
            
            shot_options = ["Defensive", "Drive", "Pull", "Sweep", "Aggressive"]
            shot_cols = st.columns(len(shot_options))
            
            for i, shot in enumerate(shot_options):
                with shot_cols[i]:
                    if st.button(shot, key=f"shot_{shot}"):
                        game.play_ball(shot_type=shot)
                        st.rerun()
        else:
            st.subheader("🎯 Your Turn - Bowling")
            
            ball_options = ["Fast", "Spin", "Yorker", "Bouncer"]
            ball_cols = st.columns(len(ball_options))
            
            for i, ball in enumerate(ball_options):
                with ball_cols[i]:
                    if st.button(ball, key=f"ball_{ball}"):
                        game.play_ball(ball_type=ball)
                        st.rerun()
    else:
        # Game over
        summary = game.get_match_summary()
        if summary:
            st.subheader("🏆 Match Result")
            
            if summary["winner"] == "Player":
                st.success(f"🎉 You won by {summary['margin']} runs!")
            elif summary["winner"] == "Computer":
                st.error(f"😔 Computer won by {summary['margin']} runs!")
            else:
                st.warning("🤝 It's a tie!")
            
            st.metric("Final Score", f"{summary['player_score']} vs {summary['computer_score']}")

with col2:
    # Statistics
    st.subheader("📈 Statistics")
    
    if game.current_innings == "player" or game.game_over:
        st.metric("Player Balls Faced", game.player_balls_faced)
        st.metric("Player Fours", game.player_fours)
        st.metric("Player Sixes", game.player_sixes)
        if game.player_balls_faced > 0:
            st.metric("Player Strike Rate", f"{game.player_score / game.player_balls_faced * 100:.1f}")
    
    if game.current_innings == "computer" or game.game_over:
        st.metric("Computer Balls Faced", game.computer_balls_faced)
        st.metric("Computer Fours", game.computer_fours)
        st.metric("Computer Sixes", game.computer_sixes)
        if game.computer_balls_faced > 0:
            st.metric("Computer Strike Rate", f"{game.computer_score / game.computer_balls_faced * 100:.1f}")

# Ball by ball commentary
if game.game_history:
    st.subheader("📝 Ball by Ball Commentary")
    
    commentary_df = pd.DataFrame(game.game_history)
    
    # Create commentary text
    commentary_text = []
    for _, ball in commentary_df.iterrows():
        if ball['innings'] == 'player':
            if ball['runs'] == 0:
                commentary_text.append(f"Ball {ball['ball']}: {ball['shot']} shot - No run")
            elif ball['runs'] == 4:
                commentary_text.append(f"Ball {ball['ball']}: {ball['shot']} shot - FOUR! 🏏")
            elif ball['runs'] == 6:
                commentary_text.append(f"Ball {ball['ball']}: {ball['shot']} shot - SIX! 🚀")
            else:
                commentary_text.append(f"Ball {ball['ball']}: {ball['shot']} shot - {ball['runs']} runs")
        else:
            if ball['runs'] == 0:
                commentary_text.append(f"Ball {ball['ball']}: {ball['ball_type']} ball - Dot ball")
            elif ball['runs'] == 'W':
                commentary_text.append(f"Ball {ball['ball']}: {ball['ball_type']} ball - WICKET! 🎯")
            elif ball['runs'] == 4:
                commentary_text.append(f"Ball {ball['ball']}: {ball['ball_type']} ball - FOUR! 🏏")
            elif ball['runs'] == 6:
                commentary_text.append(f"Ball {ball['ball']}: {ball['ball_type']} ball - SIX! 🚀")
            else:
                commentary_text.append(f"Ball {ball['ball']}: {ball['ball_type']} ball - {ball['runs']} runs")
    
    # Display last 10 balls
    recent_commentary = commentary_text[-10:] if len(commentary_text) > 10 else commentary_text
    
    for comment in recent_commentary:
        st.write(comment)

# Charts and analytics
if len(game.game_history) > 1:
    st.subheader("📊 Game Analytics")
    
    # Create charts
    chart_col1, chart_col2 = st.columns(2)
    
    with chart_col1:
        # Runs progression chart
        df = pd.DataFrame(game.game_history)
        player_runs = df[df['innings'] == 'player']['runs'].cumsum()
        computer_runs = df[df['innings'] == 'computer']['runs'].cumsum()
        
        fig = go.Figure()
        if len(player_runs) > 0:
            fig.add_trace(go.Scatter(y=player_runs, name="Player", line=dict(color='blue')))
        if len(computer_runs) > 0:
            fig.add_trace(go.Scatter(y=computer_runs, name="Computer", line=dict(color='red')))
        
        fig.update_layout(title="Runs Progression", xaxis_title="Ball", yaxis_title="Runs")
        st.plotly_chart(fig, use_container_width=True)
    
    with chart_col2:
        # Shot distribution
        if game.current_innings == "player" or game.game_over:
            shot_counts = df[df['innings'] == 'player']['shot'].value_counts()
            if len(shot_counts) > 0:
                fig = px.pie(values=shot_counts.values, names=shot_counts.index, title="Shot Distribution")
                st.plotly_chart(fig, use_container_width=True)

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666;'>
    <p>🏏 Cricket Game - Built with Streamlit</p>
    <p>Use the sidebar to start a new game or adjust settings</p>
</div>
""", unsafe_allow_html=True) 