import streamlit as st
import random
import time
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.title("Formula 1 Racing 🏎️🏁🚥🏆")
st.set_page_config(page_title="Formula 1", layout="wide")

# Add custom CSS for table styling
st.markdown("""
    <style>
    div[data-testid="stTable"] {
        width: 100% !important;
    }
    .leaderboard {
        background-color: #f0f2f6;
        border-radius: 10px;
        padding: 15px;
        margin-bottom: 20px;
        max-height: 600px;
        overflow-y: auto;
    }
    .leaderboard-item {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 8px 12px;
        margin: 4px 0;
        background-color: white;
        border-radius: 5px;
        border-left: 4px solid #1f77b4;
        font-family: monospace;
        font-size: 14px;
    }
    .position-1 { border-left-color: #FFD700; }
    .position-2 { border-left-color: #C0C0C0; }
    .position-3 { border-left-color: #CD7F32; }
    
    .rating-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 15px;
        padding: 20px;
        margin: 10px 0;
        color: white;
        box-shadow: 0 8px 32px rgba(102, 126, 234, 0.3);
        border: 1px solid rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
    }
    
    .rating-card-gold {
        background: linear-gradient(135deg, #FFD700 0%, #FFA500 100%);
        color: #000;
    }
    
    .rating-card-silver {
        background: linear-gradient(135deg, #C0C0C0 0%, #A8A8A8 100%);
        color: #000;
    }
    
    .rating-card-bronze {
        background: linear-gradient(135deg, #CD7F32 0%, #B8860B 100%);
        color: #fff;
    }
    
    .rating-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 15px;
    }
    
    .rating-score {
        font-size: 2.5em;
        font-weight: bold;
        text-align: right;
    }
    
    .rating-details {
        display: flex;
        justify-content: space-between;
        font-size: 0.9em;
        opacity: 0.9;
    }
    
    .driver-name {
        font-size: 1.3em;
        font-weight: bold;
    }
    
    .team-name {
        font-size: 1em;
        opacity: 0.8;
    }
    </style>
""", unsafe_allow_html=True)

# Team and driver data
teams_drivers = {
    "Alpine": ["Gas", "Col"],
    "Aston Martin": ["Alo", "Str"],
    "Ferrari": ["Lec", "Ham"],
    "Haas": ["Oco", "Bea"],
    "McLaren": ["Nor", "Pia"],
    "Mercedes": ["Rus", "Ant"],
    "Racing Bulls": ["Had", "Law"],
    "Red Bull": ["Ver", "Tsu"],
    "Sauber": ["Hul", "Bor"],
    "Williams": ["Sai", "Alb"]
}

# Team colors
team_colors = {
    "Alpine": "hsl(308, 100%, 34.4%)",
    "Aston Martin": "hsl(185, 99.6%, 31.7%)",
    "Ferrari": "hsl(0, 99.6%, 39.7%)",
    "Haas": "hsl(0, 99.6%, 28.2%)",
    "McLaren": "hsl(33, 99.6%, 42.4%)",
    "Mercedes": "hsl(165, 99.6%, 9.4%)",
    "Racing Bulls": "hsl(198, 99.6%, 80.3%)",
    "Red Bull": "hsl(247, 99.6%, 24.1%)",
    "Sauber": "hsl(124, 99.6%, 31.4%)",
    "Williams": "hsl(201, 99.6%, 32.2%)"
}

# Driver colors with slight variation (±5% lightness)
driver_colors = {}
for team, drivers_list in teams_drivers.items():
    color_parts = team_colors[team].replace('hsl(', '').replace(')', '').split(',')
    hue = float(color_parts[0])
    saturation = float(color_parts[1].replace('%', ''))
    lightness = float(color_parts[2].replace('%', ''))
    driver_colors[drivers_list[0]] = f"hsl({hue}, {saturation}%, {min(100, lightness + 5)}%)"
    driver_colors[drivers_list[1]] = f"hsl({hue}, {saturation}%, {max(0, lightness - 5)}%)"

# Flatten drivers list with team association
drivers = []
for team, driver_list in teams_drivers.items():
    for driver in driver_list:
        drivers.append({"driver": driver, "team": team})

# Points system (1-10 only)
points_system = {1: 25, 2: 18, 3: 15, 4: 12, 5: 10, 6: 8, 7: 6, 8: 4, 9: 2, 10: 1}

# Initialize session state
if 'progress_values' not in st.session_state:
    st.session_state.progress_values = [0] * 20
if 'finish_order' not in st.session_state:
    st.session_state.finish_order = []
if 'total_team_points' not in st.session_state:
    st.session_state.total_team_points = {team: 0 for team in teams_drivers}
if 'total_driver_points' not in st.session_state:
    st.session_state.total_driver_points = {driver['driver']: 0 for driver in drivers}
if 'team_wins' not in st.session_state:
    st.session_state.team_wins = {team: 0 for team in teams_drivers}
if 'team_podiums' not in st.session_state:
    st.session_state.team_podiums = {team: 0 for team in teams_drivers}
if 'driver_wins' not in st.session_state:
    st.session_state.driver_wins = {driver['driver']: 0 for driver in drivers}
if 'driver_podiums' not in st.session_state:
    st.session_state.driver_podiums = {driver['driver']: 0 for driver in drivers}
if 'race_finished' not in st.session_state:
    st.session_state.race_finished = False
if 'races_completed' not in st.session_state:
    st.session_state.races_completed = 0
if 'race_summaries' not in st.session_state:
    st.session_state.race_summaries = []
if 'race_started' not in st.session_state:
    st.session_state.race_started = False
if 'driver_headstarts' not in st.session_state:
    st.session_state.driver_headstarts = {driver['driver']: 1 for driver in drivers}

# Function to calculate driver rating out of 10
def calculate_driver_rating(driver):
    points = st.session_state.total_driver_points[driver]
    wins = st.session_state.driver_wins[driver]
    podiums = st.session_state.driver_podiums[driver]
    races = st.session_state.races_completed
    
    if races == 0:
        return 5.0  # Base rating when no races completed
    
    # Calculate normalized metrics (0-1 scale)
    max_possible_points = races * 25  # Maximum points if driver won every race
    points_ratio = min(points / max_possible_points, 1.0) if max_possible_points > 0 else 0
    
    win_ratio = wins / races if races > 0 else 0
    podium_ratio = podiums / races if races > 0 else 0
    
    # Weighted calculation (out of 10)
    # Points: 50%, Wins: 30%, Podiums: 20%
    rating = (points_ratio * 5.0) + (win_ratio * 3.0) + (podium_ratio * 2.0)
    
    # Ensure rating is between 0 and 10
    return min(max(rating, 0.0), 10.0)

# Function to get current leaderboard
def get_current_leaderboard():
    finished_drivers = []
    racing_drivers = []
    
    for driver_info in st.session_state.finish_order:
        finished_drivers.append({
            'driver': driver_info['driver'],
            'team': driver_info['team'],
            'progress': 100,
            'finished': True
        })
    
    finished_driver_names = [d['driver'] for d in st.session_state.finish_order]
    for i, driver_info in enumerate(drivers):
        if driver_info['driver'] not in finished_driver_names:
            racing_drivers.append({
                'driver': driver_info['driver'],
                'team': driver_info['team'],
                'progress': st.session_state.progress_values[i],
                'finished': False,
                'index': i
            })
    
    racing_drivers.sort(key=lambda x: x['progress'], reverse=True)
    return finished_drivers + racing_drivers

# Create tabs
tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
    "Race & Results",
    "Drivers' Championship",
    "Constructors' Championship",
    "Team & Driver Stats",
    "Driver Upgrades",
    "Driver Ratings",
    "Season Summary"
])

# Tab 1: Enhanced Race and Current Results (Podium) - PROGRESS BARS SECTION ONLY
# Tab 1: Enhanced Race and Current Results (Podium) - PROGRESS BARS SECTION ONLY
with tab1:
    # Use full width since no leaderboard
    if st.button("🏁 Start Race"):
        # Initialize progress with individual driver headstarts
        st.session_state.progress_values = [0] * 20
        for i, driver_info in enumerate(drivers):
            driver = driver_info['driver']
            headstart = st.session_state.driver_headstarts.get(driver, 1)
            st.session_state.progress_values[i] = min(100, headstart)
        st.session_state.finish_order = []
        st.session_state.race_finished = False
        st.session_state.race_started = True
        st.rerun()

    # ENHANCED VISUAL PROGRESS BARS SECTION
    if st.session_state.race_started and not st.session_state.race_finished:
        
        # Add enhanced CSS for beautiful progress bars
        st.markdown("""
            <style>
            .race-container {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                border-radius: 15px;
                padding: 20px;
                margin: 10px 0;
                box-shadow: 0 8px 32px rgba(102, 126, 234, 0.3);
            }
            
            .driver-row {
                background: rgba(255, 255, 255, 0.95);
                border-radius: 12px;
                padding: 15px;
                margin: 8px 0;
                display: flex;
                align-items: center;
                box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
                transition: all 0.3s ease;
                border-left: 5px solid var(--driver-color);
            }
            
            .driver-row:hover {
                transform: translateY(-2px);
                box-shadow: 0 6px 20px rgba(0, 0, 0, 0.15);
            }
            
            .driver-info {
                min-width: 150px;
                display: flex;
                flex-direction: column;
            }
            
            .driver-name {
                font-weight: bold;
                font-size: 16px;
                color: #2c3e50;
                margin-bottom: 4px;
            }
            
            .team-name {
                font-size: 12px;
                color: #7f8c8d;
                text-transform: uppercase;
                letter-spacing: 0.5px;
            }
            
            .progress-container {
                flex: 1;
                margin: 0 20px;
                position: relative;
            }
            
            .custom-progress-bar {
                width: 100%;
                height: 25px;
                background: linear-gradient(90deg, #ecf0f1 0%, #bdc3c7 100%);
                border-radius: 15px;
                overflow: hidden;
                position: relative;
                box-shadow: inset 0 2px 4px rgba(0, 0, 0, 0.1);
            }
            
            .progress-fill {
                height: 100%;
                background: linear-gradient(90deg, var(--driver-color) 0%, var(--driver-color-light) 100%);
                border-radius: 15px;
                position: relative;
                transition: width 0.5s ease-out;
                box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
            }
            
            .progress-fill::before {
                content: '';
                position: absolute;
                top: 0;
                left: 0;
                right: 0;
                height: 50%;
                background: linear-gradient(90deg, 
                    rgba(255,255,255,0.3) 0%, 
                    rgba(255,255,255,0.1) 50%, 
                    rgba(255,255,255,0.3) 100%);
                border-radius: 15px 15px 0 0;
            }
            
            .progress-text {
                position: absolute;
                top: 50%;
                left: 50%;
                transform: translate(-50%, -50%);
                font-weight: bold;
                font-size: 12px;
                color: #2c3e50;
                text-shadow: 0 1px 2px rgba(255, 255, 255, 0.8);
                z-index: 10;
            }
            
            .progress-status {
                min-width: 100px;
                text-align: right;
                display: flex;
                flex-direction: column;
                align-items: flex-end;
            }
            
            .status-text {
                font-weight: bold;
                font-size: 14px;
                color: #2c3e50;
            }
            
            .status-subtext {
                font-size: 11px;
                color: #7f8c8d;
                margin-top: 2px;
            }
            
            .finished-row {
                background: rgba(255, 255, 255, 0.95);
                color: #2c3e50;
            }
            
            .finished-row .driver-name,
            .finished-row .team-name,
            .finished-row .status-text,
            .finished-row .progress-text {
                color: #2c3e50;
                text-shadow: 0 1px 2px rgba(255, 255, 255, 0.8);
            }
            
            .position-indicator {
                font-size: 18px;
                font-weight: bold;
                margin-right: 10px;
                min-width: 40px;
                text-align: center;
            }
            
            .racing-animation {
                animation: pulse 2s infinite;
            }
            
            @keyframes pulse {
                0% { box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1); }
                50% { box-shadow: 0 6px 25px rgba(102, 126, 234, 0.3); }
                100% { box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1); }
            }
            
            .speed-indicator {
                position: absolute;
                right: 10px;
                top: 50%;
                transform: translateY(-50%);
                background: rgba(0, 0, 0, 0.1);
                border-radius: 10px;
                padding: 2px 8px;
                font-size: 10px;
                font-weight: bold;
            }
            
            .podium-section {
                background: linear-gradient(135deg, #1e3c72 0%, #2a5298 50%, #1e3c72 100%);
                border-radius: 20px;
                padding: 30px;
                margin: 20px 0;
                box-shadow: 0 15px 35px rgba(30, 60, 114, 0.4);
                position: relative;
                overflow: hidden;
            }
            
            .podium-section::before {
                content: '';
                position: absolute;
                top: 0;
                left: 0;
                right: 0;
                bottom: 0;
                background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><defs><pattern id="checkered" patternUnits="userSpaceOnUse" width="10" height="10"><rect width="5" height="5" fill="rgba(255,255,255,0.03)"/><rect x="5" y="5" width="5" height="5" fill="rgba(255,255,255,0.03)"/></pattern></defs><rect width="100" height="100" fill="url(%23checkered)"/></svg>');
                opacity: 0.1;
            }
            
            .podium-title {
                text-align: center;
                color: white;
                font-size: 28px;
                font-weight: bold;
                margin-bottom: 30px;
                text-shadow: 0 2px 4px rgba(0, 0, 0, 0.5);
                position: relative;
                z-index: 2;
            }
            
            .podium-cards-container {
                display: flex;
                justify-content: center;
                gap: 20px;
                flex-wrap: wrap;
                position: relative;
                z-index: 2;
            }
            
            .podium-card {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                border-radius: 15px;
                padding: 20px;
                margin: 10px 0;
                color: white;
                box-shadow: 0 8px 32px rgba(102, 126, 234, 0.3);
                border: 1px solid rgba(255, 255, 255, 0.1);
                backdrop-filter: blur(10px);
                min-width: 250px;
                text-align: center;
                transition: transform 0.3s ease;
            }
            
            .podium-card:hover {
                transform: translateY(-5px);
            }
            
            .podium-card-gold {
                background: linear-gradient(135deg, #FFD700 0%, #FFA500 100%);
                color: #000;
                border: 2px solid rgba(255, 215, 0, 0.5);
                box-shadow: 0 12px 40px rgba(255, 215, 0, 0.4);
            }
            
            .podium-card-silver {
                background: linear-gradient(135deg, #C0C0C0 0%, #A8A8A8 100%);
                color: #000;
                border: 2px solid rgba(192, 192, 192, 0.5);
                box-shadow: 0 12px 40px rgba(192, 192, 192, 0.4);
            }
            
            .podium-card-bronze {
                background: linear-gradient(135deg, #CD7F32 0%, #B8860B 100%);
                color: #fff;
                border: 2px solid rgba(205, 127, 50, 0.5);
                box-shadow: 0 12px 40px rgba(205, 127, 50, 0.4);
            }
            
            .podium-medal {
                font-size: 48px;
                margin-bottom: 15px;
                display: block;
                filter: drop-shadow(0 2px 4px rgba(0, 0, 0, 0.3));
            }
            
            .podium-position {
                font-size: 24px;
                font-weight: bold;
                margin-bottom: 10px;
            }
            
            .podium-driver-name {
                font-size: 20px;
                font-weight: bold;
                margin-bottom: 5px;
            }
            
            .podium-team-name {
                font-size: 14px;
                opacity: 0.9;
                text-transform: uppercase;
                letter-spacing: 0.5px;
                margin-bottom: 15px;
            }
            
            .podium-points {
                font-size: 16px;
                font-weight: bold;
                background: rgba(255, 255, 255, 0.2);
                padding: 8px 16px;
                border-radius: 25px;
                display: inline-block;
                backdrop-filter: blur(10px);
                margin-bottom: 10px;
            }
            
            .podium-details {
                font-size: 12px;
                opacity: 0.8;
                line-height: 1.4;
            }
            
            .celebration-effects {
                position: absolute;
                top: 0;
                left: 0;
                right: 0;
                bottom: 0;
                pointer-events: none;
                overflow: hidden;
            }
            
            .confetti {
                position: absolute;
                width: 6px;
                height: 6px;
                background: #ffd700;
                animation: confetti-fall 3s linear infinite;
                border-radius: 50%;
            }
            
            .confetti:nth-child(odd) {
                background: #ff6b6b;
                animation-delay: -1s;
            }
            
            .confetti:nth-child(3n) {
                background: #4ecdc4;
                animation-delay: -2s;
            }
            
            .confetti:nth-child(4n) {
                background: #45b7d1;
                animation-delay: -0.5s;
            }
            
            @keyframes confetti-fall {
                0% {
                    transform: translateY(-100vh) rotate(0deg);
                    opacity: 1;
                }
                100% {
                    transform: translateY(100vh) rotate(360deg);
                    opacity: 0;
                }
            }
            </style>
        """, unsafe_allow_html=True)
        
        st.markdown('<div class="race-container">', unsafe_allow_html=True)
        st.markdown("### 🏎️ Live Race Progress")
        
        # Create progress bars with enhanced styling
        progress_placeholders = []
        current_leaderboard = get_current_leaderboard()
        
        for pos, driver_info in enumerate(current_leaderboard, 1):
            progress = driver_info['progress']
            driver = driver_info['driver']
            team = driver_info['team']
            is_finished = driver_info.get('finished', False)
            
            # Get driver color
            base_color = driver_colors.get(driver, '#3498db')
            # Create lighter version for gradient
            if base_color.startswith('hsl'):
                # Extract HSL values and create lighter version
                hsl_parts = base_color.replace('hsl(', '').replace(')', '').split(',')
                hue = hsl_parts[0].strip()
                saturation = hsl_parts[1].strip()
                lightness = float(hsl_parts[2].replace('%', '').strip())
                lighter_lightness = min(95, lightness + 20)
                light_color = f"hsl({hue}, {saturation}, {lighter_lightness}%)"
            else:
                light_color = base_color
            
            # Position indicators
            position_emoji = ""
            if pos == 1:
                position_emoji = "🥇"
            elif pos == 2:
                position_emoji = "🥈"
            elif pos == 3:
                position_emoji = "🥉"
            else:
                position_emoji = f"P{pos}"
            
            # Status text
            if is_finished:
                status_text = "🏁 FINISHED"
                status_subtext = "Race Complete"
                row_class = "finished-row"
                animation_class = ""
            else:
                status_text = f"{progress:.1f}%"
                status_subtext = "Racing..."
                row_class = ""
                animation_class = "racing-animation" if progress > 50 else ""
            
            # Speed calculation (simulated)
            speed_kmh = int(200 + (progress / 100) * 150 + (pos * -5))  # Simulate speed
            
            # Create the enhanced progress bar HTML
            progress_html = f'''
            <div class="driver-row {row_class} {animation_class}" 
                 style="--driver-color: {base_color}; --driver-color-light: {light_color};">
                <div class="position-indicator">{position_emoji}</div>
                <div class="driver-info">
                    <div class="driver-name">{driver}</div>
                    <div class="team-name">{team}</div>
                </div>
                <div class="progress-container">
                    <div class="custom-progress-bar">
                        <div class="progress-fill" style="width: {progress}%;">
                            <div class="speed-indicator">{speed_kmh} km/h</div>
                        </div>
                        <div class="progress-text">{progress:.1f}%</div>
                    </div>
                </div>
                <div class="progress-status">
                    <div class="status-text">{status_text}</div>
                    <div class="status-subtext">{status_subtext}</div>
                </div>
            </div>
            '''
            
            placeholder = st.empty()
            placeholder.markdown(progress_html, unsafe_allow_html=True)
            progress_placeholders.append((placeholder, driver_info))
        
        st.markdown('</div>', unsafe_allow_html=True)

        # Brief pause to show initial headstarts
        time.sleep(1)

        # RACE SIMULATION LOOP WITH ENHANCED UPDATES
        while (st.session_state.race_started and 
               any(value < 100 for value in st.session_state.progress_values) and 
               not st.session_state.race_finished):
            
            for i in range(20):
                if st.session_state.progress_values[i] < 100:
                    increment = random.randint(0, 4)
                    st.session_state.progress_values[i] = min(100, st.session_state.progress_values[i] + increment)
                    if st.session_state.progress_values[i] == 100 and drivers[i]['driver'] not in [d['driver'] for d in st.session_state.finish_order]:
                        st.session_state.finish_order.append(drivers[i])
            
            # Update progress bars with new styling
            current_leaderboard = get_current_leaderboard()
            
            for idx, (placeholder, _) in enumerate(progress_placeholders):
                if idx < len(current_leaderboard):
                    driver_info = current_leaderboard[idx]
                    pos = idx + 1
                    progress = driver_info['progress']
                    driver = driver_info['driver']
                    team = driver_info['team']
                    is_finished = driver_info.get('finished', False)
                    
                    # Get driver color
                    base_color = driver_colors.get(driver, '#3498db')
                    if base_color.startswith('hsl'):
                        hsl_parts = base_color.replace('hsl(', '').replace(')', '').split(',')
                        hue = hsl_parts[0].strip()
                        saturation = hsl_parts[1].strip()
                        lightness = float(hsl_parts[2].replace('%', '').strip())
                        lighter_lightness = min(95, lightness + 20)
                        light_color = f"hsl({hue}, {saturation}, {lighter_lightness}%)"
                    else:
                        light_color = base_color
                    
                    # Position indicators
                    position_emoji = ""
                    if pos == 1:
                        position_emoji = "🥇"
                    elif pos == 2:
                        position_emoji = "🥈"
                    elif pos == 3:
                        position_emoji = "🥉"
                    else:
                        position_emoji = f"P{pos}"
                    
                    # Status text
                    if is_finished:
                        status_text = "🏁 FINISHED"
                        status_subtext = "Race Complete"
                        row_class = "finished-row"
                        animation_class = ""
                    else:
                        status_text = f"{progress:.1f}%"
                        status_subtext = "Racing..."
                        row_class = ""
                        animation_class = "racing-animation" if progress > 70 else ""
                    
                    # Dynamic speed simulation
                    base_speed = 200 + (progress / 100) * 150
                    position_penalty = pos * -3
                    random_variation = random.randint(-10, 10)
                    speed_kmh = int(base_speed + position_penalty + random_variation)
                    speed_kmh = max(180, min(350, speed_kmh))  # Realistic F1 speed range
                    
                    # Update the progress bar
                    progress_html = f'''
                    <div class="driver-row {row_class} {animation_class}" 
                         style="--driver-color: {base_color}; --driver-color-light: {light_color};">
                        <div class="position-indicator">{position_emoji}</div>
                        <div class="driver-info">
                            <div class="driver-name">{driver}</div>
                            <div class="team-name">{team}</div>
                        </div>
                        <div class="progress-container">
                            <div class="custom-progress-bar">
                                <div class="progress-fill" style="width: {progress}%;">
                                    <div class="speed-indicator">{speed_kmh} km/h</div>
                                </div>
                                <div class="progress-text">{progress:.1f}%</div>
                            </div>
                        </div>
                        <div class="progress-status">
                            <div class="status-text">{status_text}</div>
                            <div class="status-subtext">{status_subtext}</div>
                        </div>
                    </div>
                    '''
                    
                    placeholder.markdown(progress_html, unsafe_allow_html=True)
            
            if len(st.session_state.finish_order) == 20:
                st.session_state.race_finished = True
                st.session_state.races_completed += 1
                st.session_state.race_started = False
                
                # Final update with finished styling
                for idx, (placeholder, _) in enumerate(progress_placeholders):
                    if idx < len(current_leaderboard):
                        driver_info = current_leaderboard[idx]
                        pos = idx + 1
                        driver = driver_info['driver']
                        team = driver_info['team']
                        base_color = driver_colors.get(driver, '#3498db')
                        
                        position_emoji = ""
                        if pos == 1:
                            position_emoji = "🥇"
                        elif pos == 2:
                            position_emoji = "🥈"
                        elif pos == 3:
                            position_emoji = "🥉"
                        else:
                            position_emoji = f"P{pos}"
                        
                        points = points_system.get(pos, 0)
                        status_text = f"🏁 FINISHED"
                        status_subtext = f"{points} points" if pos <= 10 else "0 points"
                        
                        progress_html = f'''
                        <div class="driver-row finished-row">
                            <div class="position-indicator">{position_emoji}</div>
                            <div class="driver-info">
                                <div class="driver-name">{driver}</div>
                                <div class="team-name">{team}</div>
                            </div>
                            <div class="progress-container">
                                <div class="custom-progress-bar">
                                    <div class="progress-fill" style="width: 100%;">
                                    </div>
                                    <div class="progress-text">100%</div>
                                </div>
                            </div>
                            <div class="progress-status">
                                <div class="status-text">{status_text}</div>
                                <div class="status-subtext">{status_subtext}</div>
                            </div>
                        </div>
                        '''
                        
                        placeholder.markdown(progress_html, unsafe_allow_html=True)
                
                # Update points and statistics
                for position, driver_info in enumerate(st.session_state.finish_order, 1):
                    if position <= 10:
                        points = points_system.get(position, 0)
                        st.session_state.total_driver_points[driver_info['driver']] += points
                        st.session_state.total_team_points[driver_info['team']] += points
                    if position == 1:
                        st.session_state.driver_wins[driver_info['driver']] += 1
                        st.session_state.team_wins[driver_info['team']] += 1
                    if position <= 3:
                        st.session_state.driver_podiums[driver_info['driver']] += 1
                        st.session_state.team_podiums[driver_info['team']] += 1
                
                if len(st.session_state.finish_order) >= 3:
                    race_summary = {
                        "Race": st.session_state.races_completed,
                        "P1": f"{st.session_state.finish_order[0]['driver']} ({st.session_state.finish_order[0]['team']})",
                        "P2": f"{st.session_state.finish_order[1]['driver']} ({st.session_state.finish_order[1]['team']})",
                        "P3": f"{st.session_state.finish_order[2]['driver']} ({st.session_state.finish_order[2]['team']})"
                    }
                    st.session_state.race_summaries.append(race_summary)
                break
            
            time.sleep(1)

    if st.session_state.race_finished:
        st.markdown("---")
        
        # ENHANCED PODIUM DISPLAY WITH CARD STYLING
        if len(st.session_state.finish_order) >= 3:
            # Get podium finishers
            podium_positions = [
                (st.session_state.finish_order[0], 1, "🥇", "podium-card-gold"),   # 1st place
                (st.session_state.finish_order[1], 2, "🥈", "podium-card-silver"),  # 2nd place
                (st.session_state.finish_order[2], 3, "🥉", "podium-card-bronze")    # 3rd place
            ]
            
            # Build podium cards HTML
            podium_cards_html = ""
            for driver_info, position, medal, css_class in podium_positions:
                points = points_system.get(position, 0)
                driver_name = driver_info['driver']
                team_name = driver_info['team']
                
                # Calculate additional stats for this driver
                total_points = st.session_state.total_driver_points[driver_name]
                total_wins = st.session_state.driver_wins[driver_name]
                total_podiums = st.session_state.driver_podiums[driver_name]
                
                # Position text
                position_text = ""
                if position == 1:
                    position_text = "🏆 RACE WINNER"
                elif position == 2:
                    position_text = "🥈 SECOND PLACE"
                else:
                    position_text = "🥉 THIRD PLACE"
                
                card_html = f'''
                <div class="podium-card {css_class}">
                    <span class="podium-medal">{medal}</span>
                    <div class="podium-position">{position_text}</div>
                    <div class="podium-driver-name">{driver_name}</div>
                    <div class="podium-team-name">{team_name}</div>
                    <div class="podium-points">{points} points this race</div>
                    <div class="podium-details">
                        Championship Points: {total_points}<br>
                        Season Wins: {total_wins} | Season Podiums: {total_podiums}
                    </div>
                </div>'''
                podium_cards_html += card_html
            
            # Create complete podium section HTML
            st.markdown(f'''
            <div class="podium-section">
                <div class="celebration-effects">
                    <div class="confetti" style="left: 10%; animation-delay: 0s;"></div>
                    <div class="confetti" style="left: 20%; animation-delay: -0.5s;"></div>
                    <div class="confetti" style="left: 30%; animation-delay: -1s;"></div>
                    <div class="confetti" style="left: 40%; animation-delay: -1.5s;"></div>
                    <div class="confetti" style="left: 50%; animation-delay: -2s;"></div>
                    <div class="confetti" style="left: 60%; animation-delay: -2.5s;"></div>
                    <div class="confetti" style="left: 70%; animation-delay: -3s;"></div>
                    <div class="confetti" style="left: 80%; animation-delay: -0.3s;"></div>
                    <div class="confetti" style="left: 90%; animation-delay: -1.8s;"></div>
                </div>
                <div class="podium-title">🏆 RACE PODIUM 🏆</div>
                <div class="podium-cards-container">
                    {podium_cards_html}
                </div>
            </div>
            ''', unsafe_allow_html=True)

        st.markdown("---")
        st.subheader("🏁 Race Summary")
        st.write(f"**Races Completed: {st.session_state.races_completed}**")
        st.markdown("")
        race_summary_data = []
        for summary in st.session_state.race_summaries:
            race_summary_data.append({
                "Race": summary["Race"],
                "P1": summary["P1"],
                "P2": summary["P2"],
                "P3": summary["P3"]
            })
        if race_summary_data:
            race_summary_df = pd.DataFrame(race_summary_data)
            st.dataframe(race_summary_df, use_container_width=True, hide_index=True)
        else:
            st.write("No races completed yet.")

# Tab 2: Drivers' Championship Standings and Chart
with tab2:
    st.subheader("🏆 Drivers' Championship Standings")
    st.write(f"**Races Completed: {st.session_state.races_completed}**")
    st.markdown("")
    sorted_driver_standings = sorted(st.session_state.total_driver_points.items(), key=lambda x: x[1], reverse=True)
    st.write("**Top 3 Drivers**")
    for pos, (driver, points) in enumerate(sorted_driver_standings[:3], 1):
        team = next(d['team'] for d in drivers if d['driver'] == driver)
        if pos == 1:
            st.write(f"🥇 **P1: {driver} ({team})** - {points} points")
        elif pos == 2:
            st.write(f"🥈 **P2: {driver} ({team})** - {points} points")
        elif pos == 3:
            st.write(f"🥉 **P3: {driver} ({team})** - {points} points")
    st.markdown("")
    
    # Enhanced driver standings table with teammate comparison
    driver_standings_data = []
    for pos, (driver, points) in enumerate(sorted_driver_standings, 1):
        team = next(d['team'] for d in drivers if d['driver'] == driver)
        
        # Find teammate
        teammate = None
        teammate_points = 0
        for other_driver in teams_drivers[team]:
            if other_driver != driver:
                teammate = other_driver
                teammate_points = st.session_state.total_driver_points[other_driver]
                break
        
        # Calculate gap to teammate
        points_gap = points - teammate_points
        gap_display = ""
        if points_gap > 0:
            gap_display = f"+{points_gap}"
        elif points_gap < 0:
            gap_display = f"{points_gap}"
        else:
            gap_display = "0"
        
        driver_standings_data.append({
            "Position": pos, 
            "Driver": driver, 
            "Team": team, 
            "Total Points": points,
            "Teammate": teammate,
            "Teammate Points": teammate_points,
            "Gap to Teammate": gap_display
        })
    
    driver_df = pd.DataFrame(driver_standings_data)
    st.dataframe(driver_df, use_container_width=True, hide_index=True)

    st.markdown("---")
    
    # Teammate Comparison Section
    st.markdown("### 🤝 Teammate Battles")
    
    if st.session_state.races_completed > 0:
        # Create teammate comparison cards
        teams_processed = set()
        
        for team, team_drivers in teams_drivers.items():
            if team not in teams_processed:
                driver1, driver2 = team_drivers
                driver1_points = st.session_state.total_driver_points[driver1]
                driver2_points = st.session_state.total_driver_points[driver2]
                
                # Determine who's leading
                if driver1_points > driver2_points:
                    leading_driver = driver1
                    trailing_driver = driver2
                    leading_points = driver1_points
                    trailing_points = driver2_points
                elif driver2_points > driver1_points:
                    leading_driver = driver2
                    trailing_driver = driver1
                    leading_points = driver2_points
                    trailing_points = driver1_points
                else:
                    leading_driver = driver1
                    trailing_driver = driver2
                    leading_points = driver1_points
                    trailing_points = driver2_points
                
                gap = leading_points - trailing_points
                
                # Create comparison visualization
                col1, col2 = st.columns([1, 1])
                
                with col1:
                    st.markdown(f"#### {team}")
                    
                    # Leading driver bar
                    leading_percentage = 100 if (leading_points + trailing_points) == 0 else (leading_points / (leading_points + trailing_points)) * 100 if leading_points > 0 else 50
                    trailing_percentage = 100 - leading_percentage
                    
                    # Custom HTML for teammate comparison
                    st.markdown(f'''
                    <div style="margin-bottom: 15px;">
                        <div style="display: flex; justify-content: space-between; margin-bottom: 5px;">
                            <span style="font-weight: bold; color: {driver_colors[leading_driver]};">🥇 {leading_driver}</span>
                            <span style="font-weight: bold;">{leading_points} pts</span>
                        </div>
                        <div style="background-color: #f0f0f0; border-radius: 10px; height: 20px; overflow: hidden;">
                            <div style="background-color: {driver_colors[leading_driver]}; height: 100%; width: {leading_percentage}%; display: flex; align-items: center; justify-content: center; color: white; font-size: 12px; font-weight: bold;">
                                {leading_percentage:.0f}%
                            </div>
                        </div>
                    </div>
                    
                    <div style="margin-bottom: 15px;">
                        <div style="display: flex; justify-content: space-between; margin-bottom: 5px;">
                            <span style="font-weight: bold; color: {driver_colors[trailing_driver]};">🥈 {trailing_driver}</span>
                            <span style="font-weight: bold;">{trailing_points} pts</span>
                        </div>
                        <div style="background-color: #f0f0f0; border-radius: 10px; height: 20px; overflow: hidden;">
                            <div style="background-color: {driver_colors[trailing_driver]}; height: 100%; width: {trailing_percentage}%; display: flex; align-items: center; justify-content: center; color: white; font-size: 12px; font-weight: bold;">
                                {trailing_percentage:.0f}%
                            </div>
                        </div>
                    </div>
                    
                    <div style="text-align: center; font-size: 14px; color: #666;">
                        <strong>Gap: {gap} points</strong>
                    </div>
                    ''', unsafe_allow_html=True)
                
                teams_processed.add(team)
        
        st.markdown("---")
        
        # Team Battle Chart
        #st.markdown("### 📊 Team Battle Visualization")
        
        # Create data for teammate comparison chart
        # teammate_data = []
        # for team, team_drivers in teams_drivers.items():
        #     driver1, driver2 = team_drivers
        #     driver1_points = st.session_state.total_driver_points[driver1]
        #     driver2_points = st.session_state.total_driver_points[driver2]
            
        #     teammate_data.extend([
        #         {"Team": team, "Driver": driver1, "Points": driver1_points, "Color": driver_colors[driver1]},
        #         {"Team": team, "Driver": driver2, "Points": driver2_points, "Color": driver_colors[driver2]}
        #     ])
        
        # teammate_df = pd.DataFrame(teammate_data)

        
        
        ## Create grouped bar chart
    #     fig_teammates = px.bar(
    #         teammate_df,
    #         x="Team",
    #         y="Points",
    #         color="Driver",
    #         title="Teammate Points Comparison by Team",
    #         text="Points",
    #         color_discrete_map={row["Driver"]: row["Color"] for _, row in teammate_df.iterrows()}
    #     )
        
    #     fig_teammates.update_layout(
    #         height=500,
    #         xaxis_title="Team",
    #         yaxis_title="Championship Points",
    #         legend_title="Driver",
    #         barmode="group"
    #     )
        
    #     fig_teammates.update_traces(textposition="outside")
    #     st.plotly_chart(fig_teammates, use_container_width=True)
    
    # else:
    #     st.write("Complete some races to see teammate battles!")

    driver_chart_data = []
    for driver, points in sorted_driver_standings:
        team = next(d['team'] for d in drivers if d['driver'] == driver)
        driver_chart_data.append({"Driver": driver, "Team": team, "Points": points})

    if driver_chart_data:
        driver_df_chart = pd.DataFrame(driver_chart_data)
        # Debug: Display the DataFrame to verify structure
        #st.write("Debug: DataFrame for Bar Chart")
        #st.dataframe(driver_df_chart, use_container_width=True, hide_index=True)

        # Create bar chart sorted by points in descending order
        fig = px.bar(
            driver_df_chart,
            x="Driver",
            y="Points",
            color="Team",
            text="Points",
            color_discrete_map=team_colors  # Use provided team_colors
        )
        fig.update_traces(textposition="outside", texttemplate="%{text:.0f}", width=0.6)  # Maintain wide bars
        fig.update_layout(
            height=600,
            width=1000,
            xaxis_title="Driver",
            yaxis_title="Points",
            legend_title="Team",
            bargap=0.2,  # Gap between bars
            font=dict(size=12),
            title="Driver Points in Descending Order",
            title_font_size=16
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.write("No points data available yet. Please complete a race in the 'Race & Results' tab.")

    #st.markdown("---")

    # st.markdown("### 🥧 Drivers' Points Distribution")
    # driver_chart_data = [
    #     {"value": points, "name": f"{driver} ({next(d['team'] for d in drivers if d['driver'] == driver)})", "itemStyle": {"color": driver_colors[driver]}}
    #     for driver, points in sorted_driver_standings if points > 0
    # ]
    # if driver_chart_data:
    #     driver_df_chart = pd.DataFrame([
    #         {"Driver": item["name"], "Points": item["value"], "Color": item["itemStyle"]["color"]}
    #         for item in driver_chart_data
    #     ])
    #     fig = px.pie(
    #         driver_df_chart,
    #         values="Points",
    #         names="Driver",
    #         color="Driver",
    #         color_discrete_map={row["Driver"]: row["Color"] for _, row in driver_df_chart.iterrows()}
    #     )
    #     fig.update_traces(textposition="outside", textinfo="label+value")
    #     fig.update_layout(height=600, legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5))
    #     st.plotly_chart(fig, use_container_width=True)
    # else:
    #     st.write("No points data available yet. Please complete a race in the 'Race & Results' tab.")

# Tab 3: Constructors' Championship Standings and Chart
with tab3:
    st.subheader("🏆 Constructors' Championship Standings")
    st.write(f"**Races Completed: {st.session_state.races_completed}**")
    st.markdown("")
    sorted_team_standings = sorted(st.session_state.total_team_points.items(), key=lambda x: x[1], reverse=True)
    st.write("**Top 3 Constructors**")
    for pos, (team, points) in enumerate(sorted_team_standings[:3], 1):
        if pos == 1:
            st.write(f"🥇 **P1: {team}** - {points} points")
        elif pos == 2:
            st.write(f"🥈 **P2: {team}** - {points} points")
        elif pos == 3:
            st.write(f"🥉 **P3: {team}** - {points} points")
    st.markdown("")
    team_standings_data = []
    for pos, (team, points) in enumerate(sorted_team_standings, 1):
        team_standings_data.append({"Position": pos, "Team": team, "Total Points": points})
    team_df = pd.DataFrame(team_standings_data)
    st.dataframe(team_df, use_container_width=True, hide_index=True)

    st.markdown("### Constructors' Points Distribution")
    team_chart_data = [
        {"value": points, "name": team, "itemStyle": {"color": team_colors[team]}}
        for team, points in sorted_team_standings if points > 0
    ]
    if team_chart_data:
        team_df_chart = pd.DataFrame([
            {"Team": item["name"], "Points": item["value"], "Color": item["itemStyle"]["color"]}
            for item in team_chart_data
        ])
        fig = px.pie(
            team_df_chart,
            values="Points",
            names="Team",
            color="Team",
            color_discrete_map={row["Team"]: row["Color"] for _, row in team_df_chart.iterrows()}
        )
        fig.update_traces(textposition="outside", textinfo="label+value")
        fig.update_layout(height=600, legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5))
        st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("### Team Member Contributions")
        # Create stacked bar chart data
        team_contribution_data = []
        for team, team_points in sorted_team_standings:
            if team_points > 0:
                driver1, driver2 = teams_drivers[team]
                driver1_points = st.session_state.total_driver_points[driver1]
                driver2_points = st.session_state.total_driver_points[driver2]
                
                team_contribution_data.append({
                    "Team": team,
                    driver1: driver1_points,
                    driver2: driver2_points,
                    "Total": team_points
                })
        
        if team_contribution_data:
            contrib_df = pd.DataFrame(team_contribution_data)
            
            # Create stacked bar chart
            fig_bar = px.bar(
                contrib_df,
                x="Team",
                y=[col for col in contrib_df.columns if col not in ["Team", "Total"]],
                title="Points Contribution by Team Members",
                labels={"value": "Points", "variable": "Driver"},
                text_auto=True
            )
            
            # Update colors to match driver colors
            colors = []
            for team in contrib_df["Team"]:
                driver1, driver2 = teams_drivers[team]
                colors.extend([driver_colors[driver1], driver_colors[driver2]])
            
            # Apply colors to traces
            for i, trace in enumerate(fig_bar.data):
                team_idx = i // 2 if len(fig_bar.data) > len(contrib_df) else i
                driver_idx = i % 2
                team = contrib_df.iloc[team_idx]["Team"]
                driver = teams_drivers[team][driver_idx]
                trace.marker.color = driver_colors[driver]
                trace.name = driver
            
            fig_bar.update_layout(
                height=500,
                xaxis_title="Team",
                yaxis_title="Points",
                legend_title="Driver",
                barmode="stack"
            )
            fig_bar.update_traces(textposition="inside", textfont_size=10)
            st.plotly_chart(fig_bar, use_container_width=True)
        else:
            st.write("No team contribution data available yet.")
    else:
        st.write("No points data available yet. Please complete a race in the 'Race & Results' tab.")

# Tab 4: Constructors' and Drivers' Stats
with tab4:
    st.subheader("🏆 Constructor Statistics")
    st.write(f"**Races Completed: {st.session_state.races_completed}**")
    st.markdown("")
    constructor_stats_data = []
    sorted_team_stats = sorted(
        st.session_state.team_wins.items(),
        key=lambda x: (st.session_state.team_wins[x[0]], st.session_state.team_podiums[x[0]]),
        reverse=True
    )
    for pos, (team, wins) in enumerate(sorted_team_stats, 1):
        podiums = st.session_state.team_podiums[team]
        constructor_stats_data.append({"Position": pos, "Team": team, "Wins": wins, "Podiums": podiums})
    constructor_stats_df = pd.DataFrame(constructor_stats_data)
    st.dataframe(constructor_stats_df, use_container_width=True, hide_index=True)

    st.markdown("---")
    st.subheader("🏆 Driver Statistics")
    st.write(f"**Races Completed: {st.session_state.races_completed}**")
    st.markdown("")
    driver_stats_data = []
    sorted_driver_stats = sorted(
        st.session_state.driver_wins.items(),
        key=lambda x: (st.session_state.driver_wins[x[0]], st.session_state.driver_podiums[x[0]]),
        reverse=True
    )
    for pos, (driver, wins) in enumerate(sorted_driver_stats, 1):
        team = next(d['team'] for d in drivers if d['driver'] == driver)
        podiums = st.session_state.driver_podiums[driver]
        driver_stats_data.append({"Position": pos, "Driver": driver, "Team": team, "Wins": wins, "Podiums": podiums})
    driver_stats_df = pd.DataFrame(driver_stats_data)
    st.dataframe(driver_stats_df, use_container_width=True, hide_index=True)

# Tab 5: Driver Upgrades
with tab5:
    st.subheader("Driver Upgrades")
    st.markdown("Set a headstart percentage (1-9%) for each driver at the start of a race.")
    st.markdown("")
    
    headstart_data = []
    for driver_info in drivers:
        driver = driver_info['driver']
        team = driver_info['team']
        st.write(f"**{driver} ({team})**")
        headstart = st.number_input(
            f"Headstart for {driver}",
            min_value=1,
            max_value=9,
            value=st.session_state.driver_headstarts.get(driver, 1),
            step=1,
            key=f"headstart_{driver}"
        )
        st.session_state.driver_headstarts[driver] = headstart
        headstart_data.append({"Driver": driver, "Team": team, "Headstart (%)": headstart})
    
    st.markdown("---")
    st.subheader("Current Headstart Settings")
    headstart_df = pd.DataFrame(headstart_data)
    st.dataframe(headstart_df, use_container_width=True, hide_index=True)

# Tab 6: Driver Ratings
with tab6:
    st.subheader("⭐ Driver Ratings")
    st.write(f"**Races Completed: {st.session_state.races_completed}**")
    st.markdown("*Ratings calculated based on Points (50%), Wins (30%), and Podiums (20%)*")
    st.markdown("")
    
    # Calculate ratings for all drivers
    driver_ratings = []
    for driver_info in drivers:
        driver = driver_info['driver']
        team = driver_info['team']
        rating = calculate_driver_rating(driver)
        points = st.session_state.total_driver_points[driver]
        wins = st.session_state.driver_wins[driver]
        podiums = st.session_state.driver_podiums[driver]
        
        driver_ratings.append({
            'driver': driver,
            'team': team,
            'rating': rating,
            'points': points,
            'wins': wins,
            'podiums': podiums
        })
    
    # Sort by rating (descending)
    driver_ratings.sort(key=lambda x: x['rating'], reverse=True)
    
    if st.session_state.races_completed > 0:
        # Display top 3 drivers with special styling
        st.markdown("### 🏆 Top 3 Rated Drivers")
        
        for i, driver_data in enumerate(driver_ratings[:3]):
            driver = driver_data['driver']
            team = driver_data['team']
            rating = driver_data['rating']
            points = driver_data['points']
            wins = driver_data['wins']
            podiums = driver_data['podiums']
            
            # Determine card style based on position
            if i == 0:
                card_class = "rating-card-gold"
                medal = "🥇"
                position = "1st"
            elif i == 1:
                card_class = "rating-card-silver"
                medal = "🥈"
                position = "2nd"
            else:
                card_class = "rating-card-bronze"
                medal = "🥉"
                position = "3rd"
            
            st.markdown(f'''
            <div class="rating-card {card_class}">
                <div class="rating-header">
                    <div>
                        <div class="driver-name">{medal} {position} - {driver}</div>
                        <div class="team-name">{team}</div>
                    </div>
                    <div class="rating-score">{rating:.1f}/10</div>
                </div>
                <div class="rating-details">
                    <span>Points: {points}</span>
                    <span>Wins: {wins}</span>
                    <span>Podiums: {podiums}</span>
                </div>
            </div>
            ''', unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Complete driver ratings table
        st.subheader("📊 Complete Driver Ratings")
        ratings_data = []
        for i, driver_data in enumerate(driver_ratings, 1):
            ratings_data.append({
                "Position": i,
                "Driver": driver_data['driver'],
                "Team": driver_data['team'],
                "Rating": f"{driver_data['rating']:.1f}/10",
                "Points": driver_data['points'],
                "Wins": driver_data['wins'],
                "Podiums": driver_data['podiums']
            })
        
        ratings_df = pd.DataFrame(ratings_data)
        st.dataframe(ratings_df, use_container_width=True, hide_index=True)
        
        # Driver Ratings Visualization
        st.markdown("### 📈 Driver Ratings Visualization")
        
        # Create bar chart
        chart_data = pd.DataFrame([
            {
                "Driver": f"{d['driver']} ({d['team']})",
                "Rating": d['rating'],
                "Color": driver_colors[d['driver']]
            }
            for d in driver_ratings
        ])
        
        fig_ratings = px.bar(
            chart_data,
            x="Driver",
            y="Rating",
            title="Driver Ratings (Out of 10)",
            color="Driver",
            color_discrete_map={row["Driver"]: row["Color"] for _, row in chart_data.iterrows()}
        )
        
        fig_ratings.update_layout(
            height=500,
            xaxis_title="Driver",
            yaxis_title="Rating (out of 10)",
            yaxis=dict(range=[0, 10]),
            showlegend=False,
            xaxis_tickangle=-45
        )
        
        # Add rating values on top of bars
        fig_ratings.update_traces(
            text=[f"{rating:.1f}" for rating in chart_data["Rating"]],
            textposition="outside"
        )
        
        st.plotly_chart(fig_ratings, use_container_width=True)
        
        # Radar chart for top 5 drivers
        st.markdown("### 🕸️ Top 5 Drivers Performance Radar")
        
        if len(driver_ratings) >= 5:
            top_5_drivers = driver_ratings[:5]
            
            # Normalize metrics for radar chart (0-10 scale)
            max_points = max([d['points'] for d in top_5_drivers]) if max([d['points'] for d in top_5_drivers]) > 0 else 1
            max_wins = max([d['wins'] for d in top_5_drivers]) if max([d['wins'] for d in top_5_drivers]) > 0 else 1
            max_podiums = max([d['podiums'] for d in top_5_drivers]) if max([d['podiums'] for d in top_5_drivers]) > 0 else 1
            
            fig_radar = go.Figure()
            
            for driver_data in top_5_drivers:
                normalized_points = (driver_data['points'] / max_points) * 10
                normalized_wins = (driver_data['wins'] / max_wins) * 10
                normalized_podiums = (driver_data['podiums'] / max_podiums) * 10
                
                fig_radar.add_trace(go.Scatterpolar(
                    r=[normalized_points, normalized_wins, normalized_podiums, driver_data['rating']],
                    theta=['Points', 'Wins', 'Podiums', 'Overall Rating'],
                    fill='toself',
                    name=f"{driver_data['driver']} ({driver_data['team']})",
                    line_color=driver_colors[driver_data['driver']]
                ))
            
            fig_radar.update_layout(
                polar=dict(
                    radialaxis=dict(
                        visible=True,
                        range=[0, 10]
                    )),
                showlegend=True,
                title="Performance Comparison - Top 5 Drivers",
                height=600
            )
            
            st.plotly_chart(fig_radar, use_container_width=True)
        
        # Rating distribution
        st.markdown("### 📊 Rating Distribution")
        
        # Create histogram
        fig_hist = px.histogram(
            chart_data,
            x="Rating",
            nbins=10,
            title="Distribution of Driver Ratings",
            labels={"count": "Number of Drivers", "Rating": "Rating (out of 10)"}
        )
        
        fig_hist.update_layout(
            height=400,
            xaxis=dict(range=[0, 10]),
            bargap=0.1
        )
        
        st.plotly_chart(fig_hist, use_container_width=True)
        
    else:
        st.markdown("### 🏁 No Data Available")
        st.write("Complete some races to see driver ratings!")
        
        # Show all drivers with base rating
        st.markdown("### Current Drivers")
        base_ratings_data = []
        for i, driver_info in enumerate(drivers, 1):
            base_ratings_data.append({
                "Position": i,
                "Driver": driver_info['driver'],
                "Team": driver_info['team'],
                "Rating": "5.0/10 (Base)",
                "Points": 0,
                "Wins": 0,
                "Podiums": 0
            })
        
        base_ratings_df = pd.DataFrame(base_ratings_data)
        st.dataframe(base_ratings_df, use_container_width=True, hide_index=True)

# Tab 7: Enhanced Season Summary
with tab7:
    st.subheader("🏁 Season Summary")
    st.write(f"**Races Completed: {st.session_state.races_completed}**")
    st.markdown("")
    
    if st.session_state.races_completed > 0:
        # Championship Leaders Section
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 🏆 Drivers' Championship Leaders")
            
            # Get top 3 drivers by points
            sorted_driver_standings = sorted(st.session_state.total_driver_points.items(), key=lambda x: x[1], reverse=True)
            top_drivers = sorted_driver_standings[:3]
            
            for i, (driver, points) in enumerate(top_drivers):
                team = next(d['team'] for d in drivers if d['driver'] == driver)
                wins = st.session_state.driver_wins[driver]
                podiums = st.session_state.driver_podiums[driver]
                
                # Determine card style based on position
                if i == 0:
                    card_class = "rating-card-gold"
                    medal = "🥇"
                    position = "1st"
                elif i == 1:
                    card_class = "rating-card-silver"
                    medal = "🥈"
                    position = "2nd"
                else:
                    card_class = "rating-card-bronze"
                    medal = "🥉"
                    position = "3rd"
                
                st.markdown(f'''
                <div class="rating-card {card_class}">
                    <div class="rating-header">
                        <div>
                            <div class="driver-name">{medal} {position} - {driver}</div>
                            <div class="team-name">{team}</div>
                        </div>
                        <div class="rating-score">{points} pts</div>
                    </div>
                    <div class="rating-details">
                        <span>Wins: {wins}</span>
                        <span>Podiums: {podiums}</span>
                        <span>Avg: {points/st.session_state.races_completed:.1f} pts/race</span>
                    </div>
                </div>
                ''', unsafe_allow_html=True)
        
        with col2:
            st.markdown("### 🏗️ Constructors' Championship Leaders")
            
            # Get top 3 constructors by points
            sorted_team_standings = sorted(st.session_state.total_team_points.items(), key=lambda x: x[1], reverse=True)
            top_teams = sorted_team_standings[:3]
            
            for i, (team, points) in enumerate(top_teams):
                wins = st.session_state.team_wins[team]
                podiums = st.session_state.team_podiums[team]
                driver1, driver2 = teams_drivers[team]
                driver1_points = st.session_state.total_driver_points[driver1]
                driver2_points = st.session_state.total_driver_points[driver2]
                
                # Determine card style based on position
                if i == 0:
                    card_class = "rating-card-gold"
                    medal = "🥇"
                    position = "1st"
                elif i == 1:
                    card_class = "rating-card-silver"
                    medal = "🥈"
                    position = "2nd"
                else:
                    card_class = "rating-card-bronze"
                    medal = "🥉"
                    position = "3rd"
                
                st.markdown(f'''
                <div class="rating-card {card_class}">
                    <div class="rating-header">
                        <div>
                            <div class="driver-name">{medal} {position} - {team}</div>
                            <div class="team-name">{driver1}: {driver1_points} pts | {driver2}: {driver2_points} pts</div>
                        </div>
                        <div class="rating-score">{points} pts</div>
                    </div>
                    <div class="rating-details">
                        <span>Wins: {wins}</span>
                        <span>Podiums: {podiums}</span>
                        <span>Avg: {points/st.session_state.races_completed:.1f} pts/race</span>
                    </div>
                </div>
                ''', unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Season Statistics Overview
        st.markdown("### 📊 Season Statistics Overview")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                label="🏁 Total Races",
                value=st.session_state.races_completed
            )
        
        with col2:
            # Most successful driver
            if sorted_driver_standings:
                most_successful_driver = sorted_driver_standings[0][0]
                driver_team = next(d['team'] for d in drivers if d['driver'] == most_successful_driver)
                st.metric(
                    label="🏆 Championship Leader",
                    value=f"{most_successful_driver}",
                    delta=f"({driver_team})"
                )
        
        with col3:
            # Most successful constructor
            if sorted_team_standings:
                most_successful_team = sorted_team_standings[0][0]
                st.metric(
                    label="🏗️ Constructor Leader",
                    value=f"{most_successful_team}",
                    delta=f"{sorted_team_standings[0][1]} pts"
                )
        
        with col4:
            # Total points awarded
            total_points_awarded = sum(st.session_state.total_driver_points.values())
            st.metric(
                label="💯 Total Points Awarded",
                value=total_points_awarded
            )
        
        st.markdown("---")
        
        # Race Winners Summary
        st.markdown("### 🏆 Race Winners Summary")
        if st.session_state.race_summaries:
            winners_data = []
            for summary in st.session_state.race_summaries:
                winners_data.append({
                    "Race": summary["Race"],
                    "Winner": summary["P1"],
                    "2nd Place": summary["P2"],
                    "3rd Place": summary["P3"]
                })
            
            winners_df = pd.DataFrame(winners_data)
            st.dataframe(winners_df, use_container_width=True, hide_index=True)
        else:
            st.write("No race winners data available yet.")
        
        st.markdown("---")
        
        # Performance Trends
        st.markdown("### 📈 Championship Points Progression")
        
        if st.session_state.races_completed > 0:
            # Create a simple summary of current standings
            st.markdown("#### Current Championship Standings")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("**🏆 Drivers' Championship**")
                driver_standings_summary = []
                for pos, (driver, points) in enumerate(sorted_driver_standings[:10], 1):
                    team = next(d['team'] for d in drivers if d['driver'] == driver)
                    driver_standings_summary.append({
                        "Pos": pos,
                        "Driver": driver,
                        "Team": team,
                        "Points": points
                    })
                
                driver_summary_df = pd.DataFrame(driver_standings_summary)
                st.dataframe(driver_summary_df, use_container_width=True, hide_index=True)
            
            with col2:
                st.markdown("**🏗️ Constructors' Championship**")
                team_standings_summary = []
                for pos, (team, points) in enumerate(sorted_team_standings, 1):
                    team_standings_summary.append({
                        "Pos": pos,
                        "Constructor": team,
                        "Points": points
                    })
                
                team_summary_df = pd.DataFrame(team_standings_summary)
                st.dataframe(team_summary_df, use_container_width=True, hide_index=True)
        
        # Championship Visualization
        st.markdown("### 🎯 Championship Battle Visualization")
        
        # Driver points comparison (top 10)
        top_10_drivers = sorted_driver_standings[:10]
        if top_10_drivers:
            driver_comparison_data = []
            for driver, points in top_10_drivers:
                team = next(d['team'] for d in drivers if d['driver'] == driver)
                driver_comparison_data.append({
                    "Driver": f"{driver} ({team})",
                    "Points": points,
                    "Color": driver_colors[driver]
                })
            
            driver_comp_df = pd.DataFrame(driver_comparison_data)
            
            fig_drivers = px.bar(
                driver_comp_df,
                x="Points",
                y="Driver",
                orientation='h',
                title="Top 10 Drivers - Championship Points",
                color="Driver",
                color_discrete_map={row["Driver"]: row["Color"] for _, row in driver_comp_df.iterrows()}
            )
            
            fig_drivers.update_layout(
                height=500,
                showlegend=False,
                yaxis_title="Driver",
                xaxis_title="Championship Points"
            )
            
            # Add point values on bars
            fig_drivers.update_traces(
                text=[f"{points}" for points in driver_comp_df["Points"]],
                textposition="outside"
            )
            
            st.plotly_chart(fig_drivers, use_container_width=True)
        
        # Constructor points comparison
        if sorted_team_standings:
            team_comparison_data = []
            for team, points in sorted_team_standings:
                team_comparison_data.append({
                    "Constructor": team,
                    "Points": points,
                    "Color": team_colors[team]
                })
            
            team_comp_df = pd.DataFrame(team_comparison_data)
            
            fig_teams = px.bar(
                team_comp_df,
                x="Points",
                y="Constructor",
                orientation='h',
                title="Constructors' Championship Points",
                color="Constructor",
                color_discrete_map={row["Constructor"]: row["Color"] for _, row in team_comp_df.iterrows()}
            )
            
            fig_teams.update_layout(
                height=400,
                showlegend=False,
                yaxis_title="Constructor",
                xaxis_title="Championship Points"
            )
            
            # Add point values on bars
            # fig_teams.update_traces(
            #     text=[f"{points}" for points in team_comp_df["Points"]],
            #     textposition="outside"
            # )
            for i, trace in enumerate(fig_teams.data):
                  trace.text = [str(points) for points in team_comp_df["Points"]]
                  trace.textposition = "outside"
            
            st.plotly_chart(fig_teams, use_container_width=True)
        
        st.markdown("---")
        
        # 🏅 Expanded Season Awards & Recognition
        st.markdown("### 🏅 Expanded Season Awards & Recognition")
        
        # Major Awards Section
        st.markdown("#### 🎖️ Major Awards")
        
        award_col1, award_col2, award_col3 = st.columns(3)
        
        with award_col1:
            # Most Race Wins (Gold card)
            most_wins_driver = max(st.session_state.driver_wins.items(), key=lambda x: x[1])
            if most_wins_driver[1] > 0:
                driver_team = next(d['team'] for d in drivers if d['driver'] == most_wins_driver[0])
                st.markdown(f'''
                <div class="rating-card rating-card-gold">
                    <div class="rating-header">
                        <div>
                            <div class="driver-name">🏆 Most Race Wins</div>
                            <div class="team-name">{most_wins_driver[0]} ({driver_team})</div>
                        </div>
                        <div class="rating-score">{most_wins_driver[1]}</div>
                    </div>
                    <div class="rating-details">
                        <span>Win Rate: {(most_wins_driver[1]/st.session_state.races_completed)*100:.1f}%</span>
                        <span>Total Points: {st.session_state.total_driver_points[most_wins_driver[0]]}</span>
                    </div>
                </div>
                ''', unsafe_allow_html=True)
            else:
                st.markdown(f'''
                <div class="rating-card rating-card-gold">
                    <div class="rating-header">
                        <div>
                            <div class="driver-name">🏆 Most Race Wins</div>
                            <div class="team-name">No wins yet this season</div>
                        </div>
                        <div class="rating-score">0</div>
                    </div>
                </div>
                ''', unsafe_allow_html=True)
        
        with award_col2:
            # Most Podiums (Silver card)
            most_podiums_driver = max(st.session_state.driver_podiums.items(), key=lambda x: x[1])
            if most_podiums_driver[1] > 0:
                driver_team = next(d['team'] for d in drivers if d['driver'] == most_podiums_driver[0])
                st.markdown(f'''
                <div class="rating-card rating-card-silver">
                    <div class="rating-header">
                        <div>
                            <div class="driver-name">🥇 Most Podiums</div>
                            <div class="team-name">{most_podiums_driver[0]} ({driver_team})</div>
                        </div>
                        <div class="rating-score">{most_podiums_driver[1]}</div>
                    </div>
                    <div class="rating-details">
                        <span>Podium Rate: {(most_podiums_driver[1]/st.session_state.races_completed)*100:.1f}%</span>
                        <span>Total Points: {st.session_state.total_driver_points[most_podiums_driver[0]]}</span>
                    </div>
                </div>
                ''', unsafe_allow_html=True)
            else:
                st.markdown(f'''
                <div class="rating-card rating-card-silver">
                    <div class="rating-header">
                        <div>
                            <div class="driver-name">🥇 Most Podiums</div>
                            <div class="team-name">No podiums yet this season</div>
                        </div>
                        <div class="rating-score">0</div>
                    </div>
                </div>
                ''', unsafe_allow_html=True)
        
        with award_col3:
            # Best Constructor (Bronze card)
            best_constructor = max(st.session_state.total_team_points.items(), key=lambda x: x[1])
            if best_constructor[1] > 0:
                st.markdown(f'''
                <div class="rating-card rating-card-bronze">
                    <div class="rating-header">
                        <div>
                            <div class="driver-name">🏗️ Best Constructor</div>
                            <div class="team-name">{best_constructor[0]}</div>
                        </div>
                        <div class="rating-score">{best_constructor[1]} pts</div>
                    </div>
                    <div class="rating-details">
                        <span>Wins: {st.session_state.team_wins[best_constructor[0]]}</span>
                        <span>Podiums: {st.session_state.team_podiums[best_constructor[0]]}</span>
                    </div>
                </div>
                ''', unsafe_allow_html=True)
            else:
                st.markdown(f'''
                <div class="rating-card rating-card-bronze">
                    <div class="rating-header">
                        <div>
                            <div class="driver-name">🏗️ Best Constructor</div>
                            <div class="team-name">No points yet this season</div>
                        </div>
                        <div class="rating-score">0 pts</div>
                    </div>
                </div>
                ''', unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Special Recognition Section
        st.markdown("#### ⭐ Special Recognition")
        
        special_col1, special_col2 = st.columns(2)
        
        with special_col1:
            # Most Consistent - Driver with most points but no wins
            consistent_driver = None
            for driver, points in sorted_driver_standings:
                if st.session_state.driver_wins[driver] == 0 and points > 0:
                    consistent_driver = driver
                    break
            
            if consistent_driver:
                driver_team = next(d['team'] for d in drivers if d['driver'] == consistent_driver)
                consistent_points = st.session_state.total_driver_points[consistent_driver]
                consistent_podiums = st.session_state.driver_podiums[consistent_driver]
                
                st.markdown(f'''
                <div class="rating-card">
                    <div class="rating-header">
                        <div>
                            <div class="driver-name">🎯 Most Consistent</div>
                            <div class="team-name">{consistent_driver} ({driver_team})</div>
                        </div>
                        <div class="rating-score">{consistent_points} pts</div>
                    </div>
                    <div class="rating-details">
                        <span>No wins, but {consistent_points} points</span>
                        <span>Podiums: {consistent_podiums}</span>
                    </div>
                </div>
                ''', unsafe_allow_html=True)
            else:
                st.markdown(f'''
                <div class="rating-card">
                    <div class="rating-header">
                        <div>
                            <div class="driver-name">🎯 Most Consistent</div>
                            <div class="team-name">All scorers have wins!</div>
                        </div>
                    </div>
                </div>
                ''', unsafe_allow_html=True)
            
            # Most Balanced Team - Team with smallest gap between drivers
            smallest_gap = float('inf')
            most_balanced_team = None
            
            for team, team_drivers in teams_drivers.items():
                driver1, driver2 = team_drivers
                driver1_points = st.session_state.total_driver_points[driver1]
                driver2_points = st.session_state.total_driver_points[driver2]
                gap = abs(driver1_points - driver2_points)
                
                if gap < smallest_gap and (driver1_points > 0 or driver2_points > 0):
                    smallest_gap = gap
                    most_balanced_team = team
            
            if most_balanced_team:
                driver1, driver2 = teams_drivers[most_balanced_team]
                driver1_points = st.session_state.total_driver_points[driver1]
                driver2_points = st.session_state.total_driver_points[driver2]
                
                st.markdown(f'''
                <div class="rating-card">
                    <div class="rating-header">
                        <div>
                            <div class="driver-name">🤝 Most Balanced Team</div>
                            <div class="team-name">{most_balanced_team}</div>
                        </div>
                        <div class="rating-score">{smallest_gap} pts gap</div>
                    </div>
                    <div class="rating-details">
                        <span>{driver1}: {driver1_points} pts</span>
                        <span>{driver2}: {driver2_points} pts</span>
                    </div>
                </div>
                ''', unsafe_allow_html=True)
        
        with special_col2:
            # Best Underdog - Top performer with low upgrade settings
            best_underdog = None
            best_underdog_efficiency = 0
            
            for driver, points in sorted_driver_standings:
                if points > 0:
                    headstart = st.session_state.driver_headstarts.get(driver, 1)
                    efficiency = points / headstart  # Points per headstart percentage
                    if efficiency > best_underdog_efficiency:
                        best_underdog_efficiency = efficiency
                        best_underdog = driver
            
            if best_underdog:
                driver_team = next(d['team'] for d in drivers if d['driver'] == best_underdog)
                underdog_points = st.session_state.total_driver_points[best_underdog]
                underdog_headstart = st.session_state.driver_headstarts.get(best_underdog, 1)
                
                st.markdown(f'''
                <div class="rating-card">
                    <div class="rating-header">
                        <div>
                            <div class="driver-name">🌟 Best Underdog</div>
                            <div class="team-name">{best_underdog} ({driver_team})</div>
                        </div>
                        <div class="rating-score">{best_underdog_efficiency:.1f}</div>
                    </div>
                    <div class="rating-details">
                        <span>{underdog_points} pts with {underdog_headstart}% headstart</span>
                        <span>Efficiency: {best_underdog_efficiency:.1f} pts/headstart%</span>
                    </div>
                </div>
                ''', unsafe_allow_html=True)
            
            # Speed Demon - Best points-to-headstart efficiency
            speed_demon = None
            best_efficiency = 0
            
            for driver, points in sorted_driver_standings:
                if points > 0:
                    headstart = st.session_state.driver_headstarts.get(driver, 1)
                    efficiency = points / headstart
                    if efficiency > best_efficiency:
                        best_efficiency = efficiency
                        speed_demon = driver
            
            if speed_demon:
                driver_team = next(d['team'] for d in drivers if d['driver'] == speed_demon)
                demon_points = st.session_state.total_driver_points[speed_demon]
                demon_headstart = st.session_state.driver_headstarts.get(speed_demon, 1)
                
                st.markdown(f'''
                <div class="rating-card">
                    <div class="rating-header">
                        <div>
                            <div class="driver-name">⚡ Speed Demon</div>
                            <div class="team-name">{speed_demon} ({driver_team})</div>
                        </div>
                        <div class="rating-score">{best_efficiency:.1f}</div>
                    </div>
                    <div class="rating-details">
                        <span>Best points-to-headstart ratio</span>
                        <span>{demon_points} pts / {demon_headstart}% = {best_efficiency:.1f}</span>
                    </div>
                </div>
                ''', unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Fun Statistics Section
        st.markdown("#### 📊 Fun Statistics")
        
        fun_col1, fun_col2 = st.columns(2)
        
        with fun_col1:
            # Most Podium Appearances
            total_podium_appearances = sum(st.session_state.driver_podiums.values())
            
            # Different Race Winners count
            different_winners = sum(1 for wins in st.session_state.driver_wins.values() if wins > 0)
            
            st.markdown("**📊 Most Podium Appearances**")
            if total_podium_appearances > 0:
                st.write(f"Total podium appearances across all drivers: **{total_podium_appearances}**")
                st.write(f"Average podiums per race: **{total_podium_appearances/st.session_state.races_completed:.1f}**")
            else:
                st.write("No podium appearances yet!")
            
            st.markdown("")
            st.markdown("**🏆 Different Race Winners**")
            if different_winners > 0:
                st.write(f"Number of different race winners: **{different_winners}**")
                winner_diversity = (different_winners / st.session_state.races_completed) * 100
                st.write(f"Winner diversity: **{winner_diversity:.1f}%**")
            else:
                st.write("No race winners yet!")
        
        with fun_col2:
            # Most Dominant Team
            most_dominant_team = None
            highest_team_percentage = 0
            
            if total_points_awarded > 0:
                for team, points in sorted_team_standings:
                    team_percentage = (points / total_points_awarded) * 100
                    if team_percentage > highest_team_percentage:
                        highest_team_percentage = team_percentage
                        most_dominant_team = team
            
            st.markdown("**👑 Most Dominant Team**")
            if most_dominant_team:
                st.write(f"**{most_dominant_team}** - {highest_team_percentage:.1f}% of all points")
                st.write(f"Points: {st.session_state.total_team_points[most_dominant_team]} / {total_points_awarded}")
            else:
                st.write("No dominant team yet!")
            
            st.markdown("")
            st.markdown("**📈 Championship Gap**")
            if len(sorted_driver_standings) >= 2:
                leader_points = sorted_driver_standings[0][1]
                last_points = sorted_driver_standings[-1][1]
                championship_gap = leader_points - last_points
                
                st.write(f"Gap between 1st and last: **{championship_gap} points**")
                
                # Gap between 1st and 2nd
                if len(sorted_driver_standings) >= 2:
                    second_points = sorted_driver_standings[1][1]
                    leader_gap = leader_points - second_points
                    st.write(f"Gap between 1st and 2nd: **{leader_gap} points**")
            else:
                st.write("Need more data for championship gaps!")
    
    else:
        st.markdown("### 🏁 No Season Data Available")
        st.write("Complete some races to see the season summary!")
        st.markdown("---")
        st.markdown("### 📋 Ready to Race")
        st.write("Head to the **'Race & Results'** tab to start your first race and begin tracking season statistics.")
        
        # Show preview of what will be available
        st.markdown("### 📊 What You'll See Here After Racing:")
        st.write("- 🏆 Championship leaders with beautiful cards")
        st.write("- 📈 Points progression charts")
        st.write("- 🏁 Race winners summary")
        st.write("- 🏅 Major awards (Most Wins, Most Podiums, Best Constructor)")
        st.write("- ⭐ Special recognition (Most Consistent, Best Underdog, etc.)")
        st.write("- 📊 Fun statistics and comprehensive analysis")
