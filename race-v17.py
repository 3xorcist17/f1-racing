import streamlit as st
import random
import time
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.title("Formula 1 Racing 🏎️🏁🚥🏆")
st.set_page_config(page_title="Formula 1", layout="wide")

# Updated CSS with grey/ash colors changed to black
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
        color: #000000;
    }
    .position-1 { border-left-color: #FFD700; }
    .position-2 { border-left-color: #C0C0C0; }
    .position-3 { border-left-color: #CD7F32; }
    
    .race-container {
        background: linear-gradient(135deg, #e74c3c 0%, #000000 100%);
        border-radius: 15px;
        padding: 20px;
        margin: 10px 0;
        box-shadow: 0 8px 32px rgba(102, 126, 234, 0.3);
        color: #000000;
    }
    
    .rating-card {
        background: linear-gradient(135deg, #e74c3c 0%, #000000 100%);
        border-radius: 15px;
        padding: 20px;
        margin: 10px 0;
        color: #000000;
        box-shadow: 0 8px 32px rgba(102, 126, 234, 0.3);
        border: 1px solid rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
    }
    
    .rating-card-gold {
        background: linear-gradient(135deg, #FFD700 0%, #FFA500 100%);
        color: #000000;
    }
    
    .rating-card-silver {
        background: linear-gradient(135deg, #C0C0C0 0%, #A8A8A8 100%);
        color: #000000;
    }
    
    .rating-card-bronze {
        background: linear-gradient(135deg, #CD7F32 0%, #B8860B 100%);
        color: #000000;
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
        color: #000000;
    }
    
    .rating-details {
        display: flex;
        justify-content: space-between;
        font-size: 0.9em;
        opacity: 0.9;
        color: #000000;
    }
    
    .driver-name {
        font-size: 1.3em;
        font-weight: bold;
        color: #000000;
    }
    
    .team-name {
        font-size: 1em;
        opacity: 0.8;
        color: #000000;
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
        color: #000000;
        text-shadow: 0 1px 2px rgba(0, 0, 0, 0.3);
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
        color: #000000;
    }
    
    .status-subtext {
        font-size: 11px;
        color: #000000;
        margin-top: 2px;
    }
    
    .finished-row {
        background: rgba(255, 255, 255, 0.95);
        color: #000000;
    }
    
    .finished-row .driver-name,
    .finished-row .team-name,
    .finished-row .status-text,
    .finished-row .progress-text {
        color: #000000;
        text-shadow: 0 1px 2px rgba(0, 0, 0, 0.3);
    }
    
    .position-indicator {
        font-size: 18px;
        font-weight: bold;
        margin-right: 10px;
        min-width: 40px;
        text-align: center;
        color: #000000;
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
        color: #000000;
    }
    </style>
""", unsafe_allow_html=True)

# Team and driver data (unchanged from original)
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

# Team colors (unchanged)
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

# Driver colors (unchanged)
driver_colors = {}
for team, drivers_list in teams_drivers.items():
    color_parts = team_colors[team].replace('hsl(', '').replace(')', '').split(',')
    hue = float(color_parts[0])
    saturation = float(color_parts[1].replace('%', ''))
    lightness = float(color_parts[2].replace('%', ''))
    driver_colors[drivers_list[0]] = f"hsl({hue}, {saturation}%, {min(100, lightness + 5)}%)"
    driver_colors[drivers_list[1]] = f"hsl({hue}, {saturation}%, {max(0, lightness - 5)}%)"

# Flatten drivers list (unchanged)
drivers = []
for team, driver_list in teams_drivers.items():
    for driver in driver_list:
        drivers.append({"driver": driver, "team": team})

# Points system (unchanged)
points_system = {1: 25, 2: 18, 3: 15, 4: 12, 5: 10, 6: 8, 7: 6, 8: 4, 9: 2, 10: 1}

# Initialize session state (unchanged)
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

# Functions (unchanged)
def calculate_driver_rating(driver):
    points = st.session_state.total_driver_points[driver]
    wins = st.session_state.driver_wins[driver]
    podiums = st.session_state.driver_podiums[driver]
    races = st.session_state.races_completed
    
    if races == 0:
        return 5.0
    
    max_possible_points = races * 25
    points_ratio = min(points / max_possible_points, 1.0) if max_possible_points > 0 else 0
    win_ratio = wins / races if races > 0 else 0
    podium_ratio = podiums / races if races > 0 else 0
    
    rating = (points_ratio * 5.0) + (win_ratio * 3.0) + (podium_ratio * 2.0)
    return min(max(rating, 0.0), 10.0)

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

# Create tabs - removed "Driver Ratings" tab
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "Race & Results",
    "Drivers' Championship",
    "Constructors' Championship",
    "Team & Driver Stats",
    "Driver Upgrades",
    "Season Summary"
])

# Tab 1: Race & Results (unchanged from original, affected by CSS updates)
with tab1:
    if st.button("🏁 Start Race"):
        st.session_state.progress_values = [0] * 20
        for i, driver_info in enumerate(drivers):
            driver = driver_info['driver']
            headstart = st.session_state.driver_headstarts.get(driver, 1)
            st.session_state.progress_values[i] = min(100, headstart)
        st.session_state.finish_order = []
        st.session_state.race_finished = False
        st.session_state.race_started = True
        st.rerun()

    if st.session_state.race_started and not st.session_state.race_finished:
        st.markdown('<div class="race-container">', unsafe_allow_html=True)
        st.markdown("### 🏎️ Live Race Progress")
        
        progress_placeholders = []
        current_leaderboard = get_current_leaderboard()
        
        for pos, driver_info in enumerate(current_leaderboard, 1):
            progress = driver_info['progress']
            driver = driver_info['driver']
            team = driver_info['team']
            is_finished = driver_info.get('finished', False)
            
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
            
            position_emoji = "🥇" if pos == 1 else "🥈" if pos == 2 else "🥉" if pos == 3 else f"P{pos}"
            
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
            
            speed_kmh = int(200 + (progress / 100) * 150 + (pos * -5))
            
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

        time.sleep(1)

        while (st.session_state.race_started and 
               any(value < 100 for value in st.session_state.progress_values) and 
               not st.session_state.race_finished):
            
            for i in range(20):
                if st.session_state.progress_values[i] < 100:
                    increment = random.randint(0, 4)
                    st.session_state.progress_values[i] = min(100, st.session_state.progress_values[i] + increment)
                    if st.session_state.progress_values[i] == 100 and drivers[i]['driver'] not in [d['driver'] for d in st.session_state.finish_order]:
                        st.session_state.finish_order.append(drivers[i])
            
            current_leaderboard = get_current_leaderboard()
            
            for idx, (placeholder, _) in enumerate(progress_placeholders):
                if idx < len(current_leaderboard):
                    driver_info = current_leaderboard[idx]
                    pos = idx + 1
                    progress = driver_info['progress']
                    driver = driver_info['driver']
                    team = driver_info['team']
                    is_finished = driver_info.get('finished', False)
                    
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
                    
                    position_emoji = "🥇" if pos == 1 else "🥈" if pos == 2 else "🥉" if pos == 3 else f"P{pos}"
                    
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
                    
                    speed_kmh = int(max(180, min(350, 200 + (progress / 100) * 150 + (pos * -3) + random.randint(-10, 10))))
                    
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
                
                for idx, (placeholder, _) in enumerate(progress_placeholders):
                    if idx < len(current_leaderboard):
                        driver_info = current_leaderboard[idx]
                        pos = idx + 1
                        driver = driver_info['driver']
                        team = driver_info['team']
                        base_color = driver_colors.get(driver, '#3498db')
                        
                        position_emoji = "🥇" if pos == 1 else "🥈" if pos == 2 else "🥉" if pos == 3 else f"P{pos}"
                        
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
        if len(st.session_state.finish_order) >= 3:
            st.markdown("### 🏆 Race Podium")
            
            podium_positions = [
                (st.session_state.finish_order[0], 1, "🥇", "rating-card-gold", "1st"),
                (st.session_state.finish_order[1], 2, "🥈", "rating-card-silver", "2nd"),
                (st.session_state.finish_order[2], 3, "🥉", "rating-card-bronze", "3rd")
            ]
            
            for driver_info, position, medal, card_class, position_text in podium_positions:
                points = points_system.get(position, 0)
                driver_name = driver_info['driver']
                team_name = driver_info['team']
                
                total_points = st.session_state.total_driver_points[driver_name]
                total_wins = st.session_state.driver_wins[driver_name]
                total_podiums = st.session_state.driver_podiums[driver_name]
                
                st.markdown(f'''
                <div class="rating-card {card_class}">
                    <div class="rating-header">
                        <div>
                            <div class="driver-name">{medal} {position_text} - {driver_name}</div>
                            <div class="team-name">{team_name}</div>
                        </div>
                        <div class="rating-score">{points} pts</div>
                    </div>
                    <div class="rating-details">
                        <span>Championship: {total_points} pts</span>
                        <span>Wins: {total_wins}</span>
                        <span>Podiums: {total_podiums}</span>
                    </div>
                </div>
                ''', unsafe_allow_html=True)

        st.markdown("---")
        st.markdown('<div class="race-container">', unsafe_allow_html=True)
        st.markdown("### 🏁 Race Summary")
        st.markdown(f"**Races Completed: {st.session_state.races_completed}**")
        race_summary_data = []
        for summary in st.session_state.race_summaries:
            race_summary_data.append({
                "Race": summary["Race"],
                "P1": summary["P1"],
                "P2": summary["P2"],
                "P3": summary["P3"]
            })
        if race_summary_data:
            st.markdown('<div class="leaderboard">', unsafe_allow_html=True)
            for idx, summary in enumerate(race_summary_data):
                card_class = "position-1" if idx == 0 else ""
                st.markdown(f'''
                <div class="leaderboard-item {card_class}">
                    <span>Race {summary['Race']}</span>
                    <span>P1: {summary['P1']} | P2: {summary['P2']} | P3: {summary['P3']}</span>
                </div>
                ''', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="rating-card">', unsafe_allow_html=True)
            st.write("No races completed yet.")
            st.markdown('</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)


# Tab 2: Drivers' Championship Standings and Chart - FIXED teammate battles
with tab2:
    st.markdown('<div class="race-container">', unsafe_allow_html=True)
    st.markdown("### 🏆 Drivers' Championship Standings")
    st.markdown(f"**Races Completed: {st.session_state.races_completed}**")
    
    # Top 3 Drivers with Rating Cards
    sorted_driver_standings = sorted(st.session_state.total_driver_points.items(), key=lambda x: x[1], reverse=True)
    if sorted_driver_standings:
        st.markdown("#### Top 3 Drivers")
        for pos, (driver, points) in enumerate(sorted_driver_standings[:3], 1):
            team = next(d['team'] for d in drivers if d['driver'] == driver)
            card_class = "rating-card-gold" if pos == 1 else "rating-card-silver" if pos == 2 else "rating-card-bronze"
            medal = "🥇" if pos == 1 else "🥈" if pos == 2 else "🥉"
            position = "1st" if pos == 1 else "2nd" if pos == 2 else "3rd"
            
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
                    <span>Wins: {st.session_state.driver_wins[driver]}</span>
                    <span>Podiums: {st.session_state.driver_podiums[driver]}</span>
                    <span>Rating: {calculate_driver_rating(driver):.1f}/10</span>
                </div>
            </div>
            ''', unsafe_allow_html=True)
    
    # Enhanced Driver Standings Table with Teammate Comparison
    st.markdown("#### 📊 Full Standings")
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
        gap_display = f"+{points_gap}" if points_gap > 0 else str(points_gap) if points_gap < 0 else "0"
        
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
    st.markdown('<div class="leaderboard">', unsafe_allow_html=True)
    for idx, row in driver_df.iterrows():
        card_class = "position-1" if row["Position"] == 1 else "position-2" if row["Position"] == 2 else "position-3" if row["Position"] == 3 else ""
        st.markdown(f'''
        <div class="leaderboard-item {card_class}">
            <span>{row["Position"]}. {row["Driver"]} ({row["Team"]})</span>
            <span>{row["Total Points"]} pts (vs {row["Teammate"]}: {row["Gap to Teammate"]} pts)</span>
        </div>
        ''', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Fixed Teammate Comparison Section
    st.markdown("### 🤝 Teammate Battles")
    if st.session_state.races_completed > 0:
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
                total_team_points = leading_points + trailing_points
                leading_percentage = 50 if total_team_points == 0 else (leading_points / total_team_points) * 100
                trailing_percentage = 100 - leading_percentage
                
                # Create comparison visualization
                col1, col2 = st.columns([1, 1])
                with col1:
                    st.markdown(f"#### {team}")
                    st.markdown(f'''
                    <div style="margin-bottom: 15px;">
                        <div style="display: flex; justify-content: space-between; margin-bottom: 5px;">
                            <span style="font-weight: bold; color: {driver_colors[leading_driver]};">🥇 {leading_driver}</span>
                            <span style="font-weight: bold; color: #000000;">{leading_points} pts</span>
                        </div>
                        <div style="background-color: #f0f0f0; border-radius: 10px; height: 20px; overflow: hidden;">
                            <div style="background-color: {driver_colors[leading_driver]}; height: 100%; width: {leading_percentage}%; display: flex; align-items: center; justify-content: center; color: #000000; font-size: 12px; font-weight: bold;">
                                {leading_percentage:.0f}%
                            </div>
                        </div>
                    </div>
                    <div style="margin-bottom: 15px;">
                        <div style="display: flex; justify-content: space-between; margin-bottom: 5px;">
                            <span style="font-weight: bold; color: {driver_colors[trailing_driver]};">🥈 {trailing_driver}</span>
                            <span style="font-weight: bold; color: #000000;">{trailing_points} pts</span>
                        </div>
                        <div style="background-color: #f0f0f0; border-radius: 10px; height: 20px; overflow: hidden;">
                            <div style="background-color: {driver_colors[trailing_driver]}; height: 100%; width: {trailing_percentage}%; display: flex; align-items: center; justify-content: center; color: #000000; font-size: 12px; font-weight: bold;">
                                {trailing_percentage:.0f}%
                            </div>
                        </div>
                    </div>
                    <div style="text-align: center; font-size: 14px; color: #000000;">
                        <strong>Gap: {gap} points</strong>
                    </div>
                    ''', unsafe_allow_html=True)
                teams_processed.add(team)
    
    else:
        st.markdown('<div class="rating-card">', unsafe_allow_html=True)
        st.write("Complete some races to see teammate battles!")
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Driver Points Visualization
    st.markdown("### 📊 Drivers' Points Visualization")
    driver_chart_data = []
    for driver, points in sorted_driver_standings:
        team = next(d['team'] for d in drivers if d['driver'] == driver)
        driver_chart_data.append({"Driver": driver, "Team": team, "Points": points})
    
    if driver_chart_data:
        driver_df_chart = pd.DataFrame(driver_chart_data)
        fig = px.bar(
            driver_df_chart,
            x="Driver",
            y="Points",
            color="Team",
            text="Points",
            color_discrete_map=team_colors
        )
        fig.update_traces(textposition="outside", texttemplate="%{text:.0f}", width=0.6)
        fig.update_layout(
            height=600,
            width=1000,
            xaxis_title="Driver",
            yaxis_title="Points",
            legend_title="Team",
            bargap=0.2,
            font=dict(size=12, color="#000000"),
            title="Driver Points in Descending Order",
            title_font_size=16,
            plot_bgcolor='rgba(240, 242, 246, 0.95)',
            paper_bgcolor='rgba(240, 242, 246, 0.95)'
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.markdown('<div class="rating-card">', unsafe_allow_html=True)
        st.write("No points data available yet. Please complete a race in the 'Race & Results' tab.")
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# Tab 3: Constructors' Championship Standings and Chart - REMOVED team member contribution section
with tab3:
    st.markdown('<div class="race-container">', unsafe_allow_html=True)
    st.markdown("### 🏗️ Constructors' Championship Standings")
    st.markdown(f"**Races Completed: {st.session_state.races_completed}**")
    
    sorted_team_standings = sorted(st.session_state.total_team_points.items(), key=lambda x: x[1], reverse=True)
    if sorted_team_standings and st.session_state.races_completed > 0:
        st.markdown("#### 🥇 Top 3 Constructors")
        for pos, (team, points) in enumerate(sorted_team_standings[:3], 1):
            wins = st.session_state.team_wins[team]
            podiums = st.session_state.team_podiums[team]
            driver1, driver2 = teams_drivers[team]
            driver1_points = st.session_state.total_driver_points[driver1]
            driver2_points = st.session_state.total_driver_points[driver2]
            card_class = "rating-card-gold" if pos == 1 else "rating-card-silver" if pos == 2 else "rating-card-bronze"
            medal = "🥇" if pos == 1 else "🥈" if pos == 2 else "🥉"
            position = "1st" if pos == 1 else "2nd" if pos == 2 else "3rd"
            
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
    else:
        st.markdown('<div class="rating-card">', unsafe_allow_html=True)
        st.markdown("#### 🏁 No Data Available")
        st.write("Complete some races to see championship standings!")
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("---")
    
    st.markdown('<div class="leaderboard">', unsafe_allow_html=True)
    st.markdown("#### 📊 Complete Constructors' Standings")
    team_standings_data = []
    for pos, (team, points) in enumerate(sorted_team_standings, 1):
        team_standings_data.append({"Position": pos, "Team": team, "Total Points": points})
        card_class = "position-1" if pos == 1 else "position-2" if pos == 2 else "position-3" if pos == 3 else ""
        st.markdown(f'''
        <div class="leaderboard-item {card_class}">
            <span>{pos}. {team}</span>
            <span>{points} pts</span>
        </div>
        ''', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("#### 🥧 Constructors' Points Distribution")
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
        fig.update_layout(
            height=600,
            legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5),
            font=dict(color="#000000"),
            plot_bgcolor='rgba(240, 242, 246, 0.95)',
            paper_bgcolor='rgba(240, 242, 246, 0.95)'
        )
        st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("---")
        st.markdown("#### 👥 Team Member Contributions")
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
            fig_bar = px.bar(
                contrib_df,
                x="Team",
                y=[col for col in contrib_df.columns if col not in ["Team", "Total"]],
                title="Points Contribution by Team Members",
                labels={"value": "Points", "variable": "Driver"},
                text_auto=True
            )
            
            for i, trace in enumerate(fig_bar.data):
                team_idx = i // 2
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
                barmode="stack",
                font=dict(color="#000000"),
                plot_bgcolor='rgba(240, 242, 246, 0.95)',
                paper_bgcolor='rgba(240, 242, 246, 0.95)'
            )
            fig_bar.update_traces(textposition="inside", textfont_size=10)
            st.plotly_chart(fig_bar, use_container_width=True)
    else:
        st.markdown('<div class="rating-card">', unsafe_allow_html=True)
        st.write("No points data available yet. Please complete a race in the 'Race & Results' tab.")
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# Tab 4: Constructors' and Drivers' Stats
with tab4:
    st.markdown('<div class="race-container">', unsafe_allow_html=True)
    st.markdown("### 🏆 Constructor Statistics")
    st.markdown(f"**Races Completed: {st.session_state.races_completed}**")
    
    st.markdown('<div class="leaderboard">', unsafe_allow_html=True)
    constructor_stats_data = []
    sorted_team_stats = sorted(
        st.session_state.team_wins.items(),
        key=lambda x: (st.session_state.team_wins[x[0]], st.session_state.team_podiums[x[0]]),
        reverse=True
    )
    for pos, (team, wins) in enumerate(sorted_team_stats, 1):
        podiums = st.session_state.team_podiums[team]
        constructor_stats_data.append({"Position": pos, "Team": team, "Wins": wins, "Podiums": podiums})
        card_class = "position-1" if pos == 1 else "position-2" if pos == 2 else "position-3" if pos == 3 else ""
        st.markdown(f'''
        <div class="leaderboard-item {card_class}">
            <span>{pos}. {team}</span>
            <span>Wins: {wins} | Podiums: {podiums}</span>
        </div>
        ''', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("### 🏆 Driver Statistics")
    st.markdown(f"**Races Completed: {st.session_state.races_completed}**")
    
    st.markdown('<div class="leaderboard">', unsafe_allow_html=True)
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
        card_class = "position-1" if pos == 1 else "position-2" if pos == 2 else "position-3" if pos == 3 else ""
        st.markdown(f'''
        <div class="leaderboard-item {card_class}">
            <span>{pos}. {driver} ({team})</span>
            <span>Wins: {wins} | Podiums: {podiums}</span>
        </div>
        ''', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# Tab 5: Driver Upgrades
# Tab 5: Driver Upgrades
with tab5:
    st.markdown('<div class="race-container">', unsafe_allow_html=True)
    st.markdown("### 🛠️ Driver Performance Tuning Center")
    st.markdown("Fine-tune each driver's starting advantage with interactive sliders. Higher values give drivers better race starts!")
    
    # Quick preset buttons
    st.markdown("#### ⚡ Quick Presets")
    preset_col1, preset_col2, preset_col3, preset_col4 = st.columns(4)
    
    with preset_col1:
        if st.button("🟰 Equal Field (All 5%)", use_container_width=True):
            for driver_info in drivers:
                st.session_state.driver_headstarts[driver_info['driver']] = 5
            st.rerun()
    
    with preset_col2:
        if st.button("🎲 Randomize All", use_container_width=True):
            import random
            for driver_info in drivers:
                st.session_state.driver_headstarts[driver_info['driver']] = random.randint(1, 9)
            st.rerun()
    
    with preset_col3:
        if st.button("🔄 Reset to Default (All 1%)", use_container_width=True):
            for driver_info in drivers:
                st.session_state.driver_headstarts[driver_info['driver']] = 1
            st.rerun()
    
    with preset_col4:
        if st.button("⚡ Boost Mode (All 9%)", use_container_width=True):
            for driver_info in drivers:
                st.session_state.driver_headstarts[driver_info['driver']] = 9
            st.rerun()
    
    st.markdown("---")
    st.markdown("#### 🏎️ Individual Driver Tuning")
    
    # Group drivers by team for better organization
    team_columns = st.columns(2)
    team_list = list(teams_drivers.keys())
    
    for i, (team, team_drivers) in enumerate(teams_drivers.items()):
        with team_columns[i % 2]:
            st.markdown(f'''
            <div class="rating-card" style="background: linear-gradient(135deg, {team_colors[team]}, {team_colors[team]}40); margin-bottom: 20px;">
                <div class="rating-header">
                    <div>
                        <div class="driver-name" style="font-size: 1.4em;">🏁 {team}</div>
                    </div>
                </div>
            </div>
            ''', unsafe_allow_html=True)
            
            for driver in team_drivers:
                current_headstart = st.session_state.driver_headstarts.get(driver, 1)
                
                # Create a unique key for each slider
                slider_key = f"headstart_slider_{driver}_{team}"
                
                # Custom slider with visual feedback
                st.markdown(f"**{driver}** - Current: {current_headstart}%")
                
                new_headstart = st.slider(
                    f"Performance Boost for {driver}",
                    min_value=1,
                    max_value=9,
                    value=current_headstart,
                    step=1,
                    key=slider_key,
                    help=f"Adjust {driver}'s starting advantage. Higher values = better race start!"
                )
                
                st.session_state.driver_headstarts[driver] = new_headstart
                
                # Visual progress bar for headstart
                progress_width = (new_headstart / 9) * 100
                boost_level = "🟢 Conservative" if new_headstart <= 3 else "🟡 Moderate" if new_headstart <= 6 else "🔴 Aggressive"
                
                st.markdown(f'''
                <div style="margin-bottom: 15px;">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 5px;">
                        <span style="font-size: 12px; color: #000000;"><strong>{driver}</strong></span>
                        <span style="font-size: 12px; color: #000000;">{boost_level}</span>
                    </div>
                    <div style="background-color: #f0f0f0; border-radius: 15px; height: 20px; overflow: hidden; box-shadow: inset 0 2px 4px rgba(0, 0, 0, 0.1);">
                        <div style="background: linear-gradient(90deg, {driver_colors.get(driver, '#3498db')}, {driver_colors.get(driver, '#3498db')}80); height: 100%; width: {progress_width}%; border-radius: 15px; position: relative; transition: width 0.3s ease;">
                            <div style="position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); font-size: 11px; font-weight: bold; color: #000000;">
                                {new_headstart}% Boost
                            </div>
                        </div>
                    </div>
                </div>
                ''', unsafe_allow_html=True)
                
                st.markdown("---")
    
    # Summary section with enhanced visuals
    st.markdown("#### 📊 Performance Summary & Analysis")
    
    # Calculate statistics
    headstart_values = list(st.session_state.driver_headstarts.values())
    avg_headstart = sum(headstart_values) / len(headstart_values)
    max_headstart = max(headstart_values)
    min_headstart = min(headstart_values)
    
    # Summary metrics
    summary_col1, summary_col2, summary_col3, summary_col4 = st.columns(4)
    
    with summary_col1:
        st.metric(
            label="🎯 Average Boost",
            value=f"{avg_headstart:.1f}%",
            help="Average headstart across all drivers"
        )
    
    with summary_col2:
        st.metric(
            label="⚡ Highest Boost",
            value=f"{max_headstart}%",
            help="Maximum headstart given to any driver"
        )
    
    with summary_col3:
        st.metric(
            label="🐌 Lowest Boost",
            value=f"{min_headstart}%",
            help="Minimum headstart given to any driver"
        )
    
    with summary_col4:
        boost_range = max_headstart - min_headstart
        st.metric(
            label="📈 Boost Range",
            value=f"{boost_range}%",
            help="Difference between highest and lowest headstart"
        )
    
    # Top boosted drivers
    st.markdown("---")
    #st.markdown("#### 🏆 Most Boosted Drivers")
    
    # Sort drivers by headstart
    sorted_headstarts = sorted(
        [(driver, headstart, next(d['team'] for d in drivers if d['driver'] == driver)) 
         for driver, headstart in st.session_state.driver_headstarts.items()],
        key=lambda x: x[1],
        reverse=True
    )
    
    boost_col1, boost_col2 = st.columns(2)
    
    with boost_col1:
        st.markdown("##### 🥇 Highest Performance Boosts")
        st.markdown('<div class="leaderboard">', unsafe_allow_html=True)
        for pos, (driver, headstart, team) in enumerate(sorted_headstarts[:10], 1):
            card_class = "position-1" if pos == 1 else "position-2" if pos == 2 else "position-3" if pos == 3 else ""
            medal = "🥇" if pos == 1 else "🥈" if pos == 2 else "🥉" if pos == 3 else f"{pos}."
            
            st.markdown(f'''
            <div class="leaderboard-item {card_class}">
                <span>{medal} {driver} ({team})</span>
                <span>{headstart}% Boost</span>
            </div>
            ''', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with boost_col2:
        st.markdown("##### 🐌 Most Conservative Setups")
        st.markdown('<div class="leaderboard">', unsafe_allow_html=True)
        conservative_drivers = sorted_headstarts[-10:][::-1]  # Get bottom 10, reverse for display
        for pos, (driver, headstart, team) in enumerate(conservative_drivers, 1):
            st.markdown(f'''
            <div class="leaderboard-item">
                <span>{pos}. {driver} ({team})</span>
                <span>{headstart}% Boost</span>
            </div>
            ''', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # # Team performance analysis
    # st.markdown("---")
    # st.markdown("#### 🏗️ Team Performance Analysis")
    
    # team_analysis_data = []
    # for team, team_drivers in teams_drivers.items():
    #     driver1, driver2 = team_drivers
    #     driver1_boost = st.session_state.driver_headstarts.get(driver1, 1)
    #     driver2_boost = st.session_state.driver_headstarts.get(driver2, 1)
    #     avg_team_boost = (driver1_boost + driver2_boost) / 2
    #     boost_balance = abs(driver1_boost - driver2_boost)
        
    #     team_analysis_data.append({
    #         'team': team,
    #         'avg_boost': avg_team_boost,
    #         'balance': boost_balance,
    #         'driver1': driver1,
    #         'driver1_boost': driver1_boost,
    #         'driver2': driver2,
    #         'driver2_boost': driver2_boost
    #     })
    
    # # Sort by average boost
    # team_analysis_data.sort(key=lambda x: x['avg_boost'], reverse=True)
    
    # team_analysis_col1, team_analysis_col2 = st.columns(2)
    
    # with team_analysis_col1:
    #     st.markdown("##### 🚀 Highest Team Average Boost")
    #     for i, team_data in enumerate(team_analysis_data[:5]):
    #         card_class = "rating-card-gold" if i == 0 else "rating-card-silver" if i == 1 else "rating-card-bronze" if i == 2 else "rating-card"
    #         medal = "🥇" if i == 0 else "🥈" if i == 1 else "🥉" if i == 2 else f"{i+1}."
            
    #         st.markdown(f'''
    #         <div class="{card_class}">
    #             <div class="rating-header">
    #                 <div>
    #                     <div class="driver-name">{medal} {team_data['team']}</div>
    #                     <div class="team-name">{team_data['driver1']}: {team_data['driver1_boost']}% | {team_data['driver2']}: {team_data['driver2_boost']}%</div>
    #                 </div>
    #                 <div class="rating-score">{team_data['avg_boost']:.1f}%</div>
    #             </div>
    #             <div class="rating-details">
    #                 <span>Balance Gap: {team_data['balance']}%</span>
    #                 <span>Team Strategy: {"Balanced" if team_data['balance'] <= 1 else "Focused" if team_data['balance'] <= 3 else "Uneven"}</span>
    #             </div>
    #         </div>
    #         ''', unsafe_allow_html=True)
    
    # with team_analysis_col2:
    #     st.markdown("##### ⚖️ Most Balanced Teams")
    #     balanced_teams = sorted(team_analysis_data, key=lambda x: x['balance'])
    #     for i, team_data in enumerate(balanced_teams[:5]):
    #         balance_icon = "⚖️" if team_data['balance'] == 0 else "📊" if team_data['balance'] <= 1 else "📈" if team_data['balance'] <= 2 else "📉"
            
    #         st.markdown(f'''
    #         <div class="rating-card">
    #             <div class="rating-header">
    #                 <div>
    #                     <div class="driver-name">{balance_icon} {team_data['team']}</div>
    #                     <div class="team-name">{team_data['driver1']}: {team_data['driver1_boost']}% | {team_data['driver2']}: {team_data['driver2_boost']}%</div>
    #                 </div>
    #                 <div class="rating-score">{team_data['balance']}%</div>
    #             </div>
    #             <div class="rating-details">
    #                 <span>Avg Boost: {team_data['avg_boost']:.1f}%</span>
    #                 <span>Balance: {"Perfect" if team_data['balance'] == 0 else "Excellent" if team_data['balance'] <= 1 else "Good" if team_data['balance'] <= 2 else "Uneven"}</span>
    #             </div>
    #         </div>
    #         ''', unsafe_allow_html=True)
    
    # Strategy recommendations
    st.markdown("---")
    st.markdown("#### 💡 Strategy Recommendations")
    
    strategy_col1, strategy_col2, strategy_col3 = st.columns(3)
    
    with strategy_col1:
        st.markdown(f'''
        <div class="rating-card" style="background: linear-gradient(135deg, #2ecc71 0%, #27ae60 100%); color: #000000;">
            <div class="rating-header">
                <div>
                    <div class="driver-name">🟢 Conservative (1-3%)</div>
                    <div class="team-name">Realistic Racing</div>
                </div>
            </div>
            <div style="font-size: 13px; line-height: 1.4; margin-top: 10px; color: #000000;">
                • Minimal advantage<br>
                • Pure skill-based racing<br>
                • Unpredictable outcomes<br>
                • Great for close competition
            </div>
        </div>
        ''', unsafe_allow_html=True)
    
    with strategy_col2:
        st.markdown(f'''
        <div class="rating-card" style="background: linear-gradient(135deg, #f39c12 0%, #e67e22 100%); color: #000000;">
            <div class="rating-header">
                <div>
                    <div class="driver-name">🟡 Moderate (4-6%)</div>
                    <div class="team-name">Balanced Approach</div>
                </div>
            </div>
            <div style="font-size: 13px; line-height: 1.4; margin-top: 10px; color: #000000;">
                • Noticeable but fair advantage<br>
                • Rewards driver favorites<br>
                • Still allows comebacks<br>
                • Good for storylines
            </div>
        </div>
        ''', unsafe_allow_html=True)
    
    with strategy_col3:
        st.markdown(f'''
        <div class="rating-card" style="background: linear-gradient(135deg, #e74c3c 0%, #c0392b 100%); color: #000000;">
            <div class="rating-header">
                <div>
                    <div class="driver-name">🔴 Aggressive (7-9%)</div>
                    <div class="team-name">Dominant Performance</div>
                </div>
            </div>
            <div style="font-size: 13px; line-height: 1.4; margin-top: 10px; color: #000000;">
                • Significant head start<br>
                • Favors top drivers heavily<br>
                • More predictable results<br>
                • Creates clear favorites
            </div>
        </div>
        ''', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# Tab 6: Season Summary - Enhanced with More Awards
with tab6:
    st.markdown('<div class="race-container">', unsafe_allow_html=True)
    st.markdown("### 🏁 Season Summary")
    st.markdown(f"**Races Completed: {st.session_state.races_completed}**")
    
    if st.session_state.races_completed > 0:
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 🏆 Drivers' Championship Leaders")
            sorted_driver_standings = sorted(st.session_state.total_driver_points.items(), key=lambda x: x[1], reverse=True)
            for i, (driver, points) in enumerate(sorted_driver_standings[:3]):
                team = next(d['team'] for d in drivers if d['driver'] == driver)
                wins = st.session_state.driver_wins[driver]
                podiums = st.session_state.driver_podiums[driver]
                
                card_class = "rating-card-gold" if i == 0 else "rating-card-silver" if i == 1 else "rating-card-bronze"
                medal = "🥇" if i == 0 else "🥈" if i == 1 else "🥉"
                position = "1st" if i == 0 else "2nd" if i == 1 else "3rd"
                
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
            st.markdown("#### 🏗️ Constructors' Championship Leaders")
            sorted_team_standings = sorted(st.session_state.total_team_points.items(), key=lambda x: x[1], reverse=True)
            for i, (team, points) in enumerate(sorted_team_standings[:3]):
                wins = st.session_state.team_wins[team]
                podiums = st.session_state.team_podiums[team]
                driver1, driver2 = teams_drivers[team]
                driver1_points = st.session_state.total_driver_points[driver1]
                driver2_points = st.session_state.total_driver_points[driver2]
                
                card_class = "rating-card-gold" if i == 0 else "rating-card-silver" if i == 1 else "rating-card-bronze"
                medal = "🥇" if i == 0 else "🥈" if i == 1 else "🥉"
                position = "1st" if i == 0 else "2nd" if i == 1 else "3rd"
                
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
        st.markdown("#### 📊 Season Statistics Overview")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                label="🏁 Total Races",
                value=st.session_state.races_completed
            )
        
        with col2:
            if sorted_driver_standings:
                most_successful_driver = sorted_driver_standings[0][0]
                driver_team = next(d['team'] for d in drivers if d['driver'] == most_successful_driver)
                st.metric(
                    label="🏆 Championship Leader",
                    value=f"{most_successful_driver}",
                    delta=f"({driver_team})"
                )
        
        with col3:
            if sorted_team_standings:
                most_successful_team = sorted_team_standings[0][0]
                st.metric(
                    label="🏗️ Constructor Leader",
                    value=f"{most_successful_team}",
                    delta=f"{sorted_team_standings[0][1]} pts"
                )
        
        with col4:
            total_points_awarded = sum(st.session_state.total_driver_points.values())
            st.metric(
                label="💯 Total Points Awarded",
                value=total_points_awarded
            )
        
        st.markdown("---")
        st.markdown("#### 🏆 Race Winners Summary")
        if st.session_state.race_summaries:
            winners_data = []
            for summary in st.session_state.race_summaries:
                winners_data.append({
                    "Race": summary["Race"],
                    "Winner": summary["P1"],
                    "2nd Place": summary["P2"],
                    "3rd Place": summary["P3"]
                })
            
            st.markdown('<div class="leaderboard">', unsafe_allow_html=True)
            for idx, summary in enumerate(winners_data):
                card_class = "position-1" if idx == 0 else ""
                st.markdown(f'''
                <div class="leaderboard-item {card_class}">
                    <span>Race {summary['Race']}</span>
                    <span>Winner: {summary['Winner']} | 2nd: {summary['2nd Place']} | 3rd: {summary['3rd Place']}</span>
                </div>
                ''', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="rating-card">', unsafe_allow_html=True)
            st.write("No race winners data available yet.")
            st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown("---")
        st.markdown("#### 🎖️ Major Awards & Recognitions")
        
        # Row 1: Top Performance Awards
        award_col1, award_col2, award_col3 = st.columns(3)
        
        with award_col1:
            most_wins_driver = max(st.session_state.driver_wins.items(), key=lambda x: x[1])
            if most_wins_driver[1] > 0:
                driver_team = next(d['team'] for d in drivers if d['driver'] == most_wins_driver[0])
                st.markdown(f'''
                <div class="rating-card" style="background: linear-gradient(135deg, #e74c3c 0%, #c0392b 100%); color: #000000;">
                    <div class="rating-header">
                        <div>
                            <div class="driver-name">🏆 Race Winner King</div>
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
                <div class="rating-card" style="background: linear-gradient(135deg, #e74c3c 0%, #c0392b 100%); color: #000000;">
                    <div class="rating-header">
                        <div>
                            <div class="driver-name">🏆 Race Winner King</div>
                            <div class="team-name">No wins yet this season</div>
                        </div>
                        <div class="rating-score">0</div>
                    </div>
                </div>
                ''', unsafe_allow_html=True)
        
        with award_col2:
            most_podiums_driver = max(st.session_state.driver_podiums.items(), key=lambda x: x[1])
            if most_podiums_driver[1] > 0:
                driver_team = next(d['team'] for d in drivers if d['driver'] == most_podiums_driver[0])
                st.markdown(f'''
                <div class="rating-card" style="background: linear-gradient(135deg, #9b59b6 0%, #8e44ad 100%); color: #000000;">
                    <div class="rating-header">
                        <div>
                            <div class="driver-name">🥇 Podium Master</div>
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
                <div class="rating-card" style="background: linear-gradient(135deg, #9b59b6 0%, #8e44ad 100%); color: #000000;">
                    <div class="rating-header">
                        <div>
                            <div class="driver-name">🥇 Podium Master</div>
                            <div class="team-name">No podiums yet this season</div>
                        </div>
                        <div class="rating-score">0</div>
                    </div>
                </div>
                ''', unsafe_allow_html=True)
        
        with award_col3:
            best_constructor = max(st.session_state.total_team_points.items(), key=lambda x: x[1])
            if best_constructor[1] > 0:
                st.markdown(f'''
                <div class="rating-card" style="background: linear-gradient(135deg, #f39c12 0%, #e67e22 100%); color: #000000;">
                    <div class="rating-header">
                        <div>
                            <div class="driver-name">🏗️ Constructor Champion</div>
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
                <div class="rating-card" style="background: linear-gradient(135deg, #f39c12 0%, #e67e22 100%); color: #000000;">
                    <div class="rating-header">
                        <div>
                            <div class="driver-name">🏗️ Constructor Champion</div>
                            <div class="team-name">No points yet this season</div>
                        </div>
                        <div class="rating-score">0 pts</div>
                    </div>
                </div>
                ''', unsafe_allow_html=True)
        
        # Row 2: Performance Excellence Awards
        st.markdown("---")
        award_col4, award_col5, award_col6 = st.columns(3)
        
        with award_col4:
            # Most Consistent Driver (no wins but points)
            consistent_driver = None
            consistent_points = 0
            for driver, points in sorted_driver_standings:
                if st.session_state.driver_wins[driver] == 0 and points > consistent_points:
                    consistent_driver = driver
                    consistent_points = points
            
            if consistent_driver:
                driver_team = next(d['team'] for d in drivers if d['driver'] == consistent_driver)
                podiums = st.session_state.driver_podiums[consistent_driver]
                st.markdown(f'''
                <div class="rating-card" style="background: linear-gradient(135deg, #27ae60 0%, #229954 100%); color: #000000;">
                    <div class="rating-header">
                        <div>
                            <div class="driver-name">🌟 Mr. Reliable</div>
                            <div class="team-name">{consistent_driver} ({driver_team})</div>
                        </div>
                        <div class="rating-score">{consistent_points} pts</div>
                    </div>
                    <div class="rating-details">
                        <span>No Wins, All Points</span>
                        <span>Podiums: {podiums}</span>
                    </div>
                </div>
                ''', unsafe_allow_html=True)
            else:
                st.markdown(f'''
                <div class="rating-card" style="background: linear-gradient(135deg, #27ae60 0%, #229954 100%); color: #000000;">
                    <div class="rating-header">
                        <div>
                            <div class="driver-name">🌟 Mr. Reliable</div>
                            <div class="team-name">No reliable driver yet</div>
                        </div>
                        <div class="rating-score">0 pts</div>
                    </div>
                </div>
                ''', unsafe_allow_html=True)
        
        with award_col5:
            # Highest Rated Driver
            highest_rated_driver = max(
                [(d['driver'], calculate_driver_rating(d['driver'])) for d in drivers],
                key=lambda x: x[1]
            )
            driver_team = next(d['team'] for d in drivers if d['driver'] == highest_rated_driver[0])
            rating = highest_rated_driver[1]
            points = st.session_state.total_driver_points[highest_rated_driver[0]]
            
            st.markdown(f'''
            <div class="rating-card" style="background: linear-gradient(135deg, #3498db 0%, #2980b9 100%); color: #000000;">
                <div class="rating-header">
                    <div>
                        <div class="driver-name">⭐ Highest Rated</div>
                        <div class="team-name">{highest_rated_driver[0]} ({driver_team})</div>
                    </div>
                    <div class="rating-score">{rating:.1f}/10</div>
                </div>
                <div class="rating-details">
                    <span>Points: {points}</span>
                    <span>Elite Performance</span>
                </div>
            </div>
            ''', unsafe_allow_html=True)
        
        with award_col6:
            # Best Rookie (driver with least experience/points but still competitive)
            rookie_candidates = [(driver, points) for driver, points in sorted_driver_standings if points < 50 and points > 0]
            if rookie_candidates:
                best_rookie = max(rookie_candidates, key=lambda x: x[1])
                driver_team = next(d['team'] for d in drivers if d['driver'] == best_rookie[0])
                st.markdown(f'''
                <div class="rating-card" style="background: linear-gradient(135deg, #e67e22 0%, #d35400 100%); color: #000000;">
                    <div class="rating-header">
                        <div>
                            <div class="driver-name">🌱 Rising Star</div>
                            <div class="team-name">{best_rookie[0]} ({driver_team})</div>
                        </div>
                        <div class="rating-score">{best_rookie[1]} pts</div>
                    </div>
                    <div class="rating-details">
                        <span>Promising Talent</span>
                        <span>Future Champion</span>
                    </div>
                </div>
                ''', unsafe_allow_html=True)
            else:
                st.markdown(f'''
                <div class="rating-card" style="background: linear-gradient(135deg, #e67e22 0%, #d35400 100%); color: #000000;">
                    <div class="rating-header">
                        <div>
                            <div class="driver-name">🌱 Rising Star</div>
                            <div class="team-name">No rising star yet</div>
                        </div>
                        <div class="rating-score">0 pts</div>
                    </div>
                </div>
                ''', unsafe_allow_html=True)
        
        # Row 3: Special Recognition Awards
        st.markdown("---")
        award_col7, award_col8, award_col9 = st.columns(3)
        
        with award_col7:
            # Most Improved Team (based on recent performance)
            if len(st.session_state.race_summaries) >= 3:
                recent_winners = [summary["P1"].split(' (')[1].replace(')', '') for summary in st.session_state.race_summaries[-3:]]
                team_recent_wins = {}
                for team_name in recent_winners:
                    team_recent_wins[team_name] = team_recent_wins.get(team_name, 0) + 1
                
                if team_recent_wins:
                    most_improved_team = max(team_recent_wins.items(), key=lambda x: x[1])
                    team_total_wins = st.session_state.team_wins[most_improved_team[0]]
                    st.markdown(f'''
                    <div class="rating-card" style="background: linear-gradient(135deg, #16a085 0%, #138d75 100%); color: #000000;">
                        <div class="rating-header">
                            <div>
                                <div class="driver-name">📈 Most Improved Team</div>
                                <div class="team-name">{most_improved_team[0]}</div>
                            </div>
                            <div class="rating-score">{most_improved_team[1]}/3</div>
                        </div>
                        <div class="rating-details">
                            <span>Recent Form</span>
                            <span>Total Wins: {team_total_wins}</span>
                        </div>
                    </div>
                    ''', unsafe_allow_html=True)
                else:
                    st.markdown(f'''
                    <div class="rating-card" style="background: linear-gradient(135deg, #16a085 0%, #138d75 100%); color: #000000;">
                        <div class="rating-header">
                            <div>
                                <div class="driver-name">📈 Most Improved Team</div>
                                <div class="team-name">Need more races</div>
                            </div>
                            <div class="rating-score">0</div>
                        </div>
                    </div>
                    ''', unsafe_allow_html=True)
            else:
                st.markdown(f'''
                <div class="rating-card" style="background: linear-gradient(135deg, #16a085 0%, #138d75 100%); color: #000000;">
                    <div class="rating-header">
                        <div>
                            <div class="driver-name">📈 Most Improved Team</div>
                            <div class="team-name">Need more races</div>
                        </div>
                        <div class="rating-score">0</div>
                    </div>
                </div>
                ''', unsafe_allow_html=True)
        
        with award_col8:
            # Point Scoring Machine (most points per race average)
            best_avg_driver = None
            best_avg = 0
            for driver, points in sorted_driver_standings:
                if points > 0:
                    avg = points / st.session_state.races_completed
                    if avg > best_avg:
                        best_avg = avg
                        best_avg_driver = driver
            
            if best_avg_driver:
                driver_team = next(d['team'] for d in drivers if d['driver'] == best_avg_driver)
                total_points = st.session_state.total_driver_points[best_avg_driver]
                st.markdown(f'''
                <div class="rating-card" style="background: linear-gradient(135deg, #8e44ad 0%, #7d3c98 100%); color: #000000;">
                    <div class="rating-header">
                        <div>
                            <div class="driver-name">⚡ Point Scoring Machine</div>
                            <div class="team-name">{best_avg_driver} ({driver_team})</div>
                        </div>
                        <div class="rating-score">{best_avg:.1f}</div>
                    </div>
                    <div class="rating-details">
                        <span>Avg/Race</span>
                        <span>Total: {total_points} pts</span>
                    </div>
                </div>
                ''', unsafe_allow_html=True)
            else:
                st.markdown(f'''
                <div class="rating-card" style="background: linear-gradient(135deg, #8e44ad 0%, #7d3c98 100%); color: #000000;">
                    <div class="rating-header">
                        <div>
                            <div class="driver-name">⚡ Point Scoring Machine</div>
                            <div class="team-name">No points yet</div>
                        </div>
                        <div class="rating-score">0</div>
                    </div>
                </div>
                ''', unsafe_allow_html=True)
        
        with award_col9:
            # Underdog Hero (lowest headstart but good performance)
            underdog_candidates = []
            for driver_info in drivers:
                driver = driver_info['driver']
                headstart = st.session_state.driver_headstarts.get(driver, 1)
                points = st.session_state.total_driver_points[driver]
                if points > 0:
                    efficiency_score = points / headstart
                    underdog_candidates.append((driver, efficiency_score, points, headstart))
            
            if underdog_candidates:
                best_underdog = max(underdog_candidates, key=lambda x: x[1])
                driver_team = next(d['team'] for d in drivers if d['driver'] == best_underdog[0])
                st.markdown(f'''
                <div class="rating-card" style="background: linear-gradient(135deg, #d35400 0%, #ba4a00 100%); color: #000000;">
                    <div class="rating-header">
                        <div>
                            <div class="driver-name">🦾 Underdog Hero</div>
                            <div class="team-name">{best_underdog[0]} ({driver_team})</div>
                        </div>
                        <div class="rating-score">{best_underdog[1]:.1f}</div>
                    </div>
                    <div class="rating-details">
                        <span>Efficiency Score</span>
                        <span>{best_underdog[2]} pts @ {best_underdog[3]}%</span>
                    </div>
                </div>
                ''', unsafe_allow_html=True)
            else:
                st.markdown(f'''
                <div class="rating-card" style="background: linear-gradient(135deg, #d35400 0%, #ba4a00 100%); color: #000000;">
                    <div class="rating-header">
                        <div>
                            <div class="driver-name">🦾 Underdog Hero</div>
                            <div class="team-name">No underdog yet</div>
                        </div>
                        <div class="rating-score">0</div>
                    </div>
                </div>
                ''', unsafe_allow_html=True)
        
        # Row 4: Team Excellence Awards
        st.markdown("---")
        award_col10, award_col11, award_col12 = st.columns(3)
        
        with award_col10:
            # Best Teammate Partnership (smallest gap between teammates)
            best_partnership = None
            smallest_gap = float('inf')
            for team, team_drivers in teams_drivers.items():
                driver1, driver2 = team_drivers
                driver1_points = st.session_state.total_driver_points[driver1]
                driver2_points = st.session_state.total_driver_points[driver2]
                gap = abs(driver1_points - driver2_points)
                total_team_points = driver1_points + driver2_points
                
                if total_team_points > 0 and gap < smallest_gap:
                    smallest_gap = gap
                    best_partnership = (team, gap, total_team_points)
            
            if best_partnership:
                st.markdown(f'''
                <div class="rating-card" style="background: linear-gradient(135deg, #2ecc71 0%, #27ae60 100%); color: #000000;">
                    <div class="rating-header">
                        <div>
                            <div class="driver-name">🤝 Best Partnership</div>
                            <div class="team-name">{best_partnership[0]}</div>
                        </div>
                        <div class="rating-score">{best_partnership[1]} pts</div>
                    </div>
                    <div class="rating-details">
                        <span>Gap Between Teammates</span>
                        <span>Team Total: {best_partnership[2]} pts</span>
                    </div>
                </div>
                ''', unsafe_allow_html=True)
            else:
                st.markdown(f'''
                <div class="rating-card" style="background: linear-gradient(135deg, #2ecc71 0%, #27ae60 100%); color: #000000;">
                    <div class="rating-header">
                        <div>
                            <div class="driver-name">🤝 Best Partnership</div>
                            <div class="team-name">No partnerships yet</div>
                        </div>
                        <div class="rating-score">0</div>
                    </div>
                </div>
                ''', unsafe_allow_html=True)
        
        with award_col11:
            # Giant Killer (driver who beats highly rated teammates)
            giant_killer = None
            best_teammate_beating_ratio = 0
            for team, team_drivers in teams_drivers.items():
                driver1, driver2 = team_drivers
                driver1_points = st.session_state.total_driver_points[driver1]
                driver2_points = st.session_state.total_driver_points[driver2]
                driver1_headstart = st.session_state.driver_headstarts.get(driver1, 1)
                driver2_headstart = st.session_state.driver_headstarts.get(driver2, 1)
                
                if driver1_headstart < driver2_headstart and driver1_points > driver2_points:
                    ratio = driver1_points / driver2_points if driver2_points > 0 else 1
                    if ratio > best_teammate_beating_ratio:
                        best_teammate_beating_ratio = ratio
                        giant_killer = (driver1, team, driver1_points, driver2_points)
                elif driver2_headstart < driver1_headstart and driver2_points > driver1_points:
                    ratio = driver2_points / driver1_points if driver1_points > 0 else 1
                    if ratio > best_teammate_beating_ratio:
                        best_teammate_beating_ratio = ratio
                        giant_killer = (driver2, team, driver2_points, driver1_points)
            
            if giant_killer:
                st.markdown(f'''
                <div class="rating-card" style="background: linear-gradient(135deg, #e74c3c 0%, #cb4335 100%); color: #000000;">
                    <div class="rating-header">
                        <div>
                            <div class="driver-name">🗡️ Giant Killer</div>
                            <div class="team-name">{giant_killer[0]} ({giant_killer[1]})</div>
                        </div>
                        <div class="rating-score">{best_teammate_beating_ratio:.1f}x</div>
                    </div>
                    <div class="rating-details">
                        <span>Beat Favored Teammate</span>
                        <span>{giant_killer[2]} vs {giant_killer[3]} pts</span>
                    </div>
                </div>
                ''', unsafe_allow_html=True)
            else:
                st.markdown(f'''
                <div class="rating-card" style="background: linear-gradient(135deg, #e74c3c 0%, #cb4335 100%); color: #000000;">
                    <div class="rating-header">
                        <div>
                            <div class="driver-name">🗡️ Giant Killer</div>
                            <div class="team-name">No giant killers yet</div>
                        </div>
                        <div class="rating-score">0</div>
                    </div>
                </div>
                ''', unsafe_allow_html=True)
        
        with award_col12:
            # Comeback King (driver who improved most from last position)
            if st.session_state.race_summaries:
                comeback_scores = {}
                for summary in st.session_state.race_summaries:
                    # Count podium finishes for comeback calculation
                    p1_driver = summary["P1"].split(' (')[0]
                    p2_driver = summary["P2"].split(' (')[0]
                    p3_driver = summary["P3"].split(' (')[0]
                    
                    comeback_scores[p1_driver] = comeback_scores.get(p1_driver, 0) + 3
                    comeback_scores[p2_driver] = comeback_scores.get(p2_driver, 0) + 2
                    comeback_scores[p3_driver] = comeback_scores.get(p3_driver, 0) + 1
                
                if comeback_scores:
                    comeback_king = max(comeback_scores.items(), key=lambda x: x[1])
                    driver_team = next(d['team'] for d in drivers if d['driver'] == comeback_king[0])
                    driver_wins = st.session_state.driver_wins[comeback_king[0]]
                    st.markdown(f'''
                    <div class="rating-card" style="background: linear-gradient(135deg, #f1c40f 0%, #f39c12 100%); color: #000000;">
                        <div class="rating-header">
                            <div>
                                <div class="driver-name">👑 Comeback King</div>
                                <div class="team-name">{comeback_king[0]} ({driver_team})</div>
                            </div>
                            <div class="rating-score">{comeback_king[1]}</div>
                        </div>
                        <div class="rating-details">
                            <span>Podium Score</span>
                            <span>Wins: {driver_wins}</span>
                        </div>
                    </div>
                    ''', unsafe_allow_html=True)
                else:
                    st.markdown(f'''
                    <div class="rating-card" style="background: linear-gradient(135deg, #f1c40f 0%, #f39c12 100%); color: #000000;">
                        <div class="rating-header">
                            <div>
                                <div class="driver-name">👑 Comeback King</div>
                                <div class="team-name">No comebacks yet</div>
                            </div>
                            <div class="rating-score">0</div>
                        </div>
                    </div>
                    ''', unsafe_allow_html=True)
            else:
                st.markdown(f'''
                <div class="rating-card" style="background: linear-gradient(135deg, #f1c40f 0%, #f39c12 100%); color: #000000;">
                    <div class="rating-header">
                        <div>
                            <div class="driver-name">👑 Comeback King</div>
                            <div class="team-name">Need more races</div>
                        </div>
                        <div class="rating-score">0</div>
                    </div>
                </div>
                ''', unsafe_allow_html=True)
        
        # Row 5: Specialty Awards
        st.markdown("---")
        award_col13, award_col14, award_col15 = st.columns(3)
        
        with award_col13:
            # Speed Demon (driver with highest headstart who still performs well)
            speed_demons = []
            for driver_info in drivers:
                driver = driver_info['driver']
                headstart = st.session_state.driver_headstarts.get(driver, 1)
                points = st.session_state.total_driver_points[driver]
                if headstart >= 7 and points > 20:
                    speed_demons.append((driver, headstart, points))
            
            if speed_demons:
                best_speed_demon = max(speed_demons, key=lambda x: x[2])
                driver_team = next(d['team'] for d in drivers if d['driver'] == best_speed_demon[0])
                st.markdown(f'''
                <div class="rating-card" style="background: linear-gradient(135deg, #ff6b6b 0%, #ee5a52 100%); color: #000000;">
                    <div class="rating-header">
                        <div>
                            <div class="driver-name">💨 Speed Demon</div>
                            <div class="team-name">{best_speed_demon[0]} ({driver_team})</div>
                        </div>
                        <div class="rating-score">{best_speed_demon[2]} pts</div>
                    </div>
                    <div class="rating-details">
                        <span>High Headstart: {best_speed_demon[1]}%</span>
                        <span>Still Delivers</span>
                    </div>
                </div>
                ''', unsafe_allow_html=True)
            else:
                st.markdown(f'''
                <div class="rating-card" style="background: linear-gradient(135deg, #ff6b6b 0%, #ee5a52 100%); color: #000000;">
                    <div class="rating-header">
                        <div>
                            <div class="driver-name">💨 Speed Demon</div>
                            <div class="team-name">No speed demons yet</div>
                        </div>
                        <div class="rating-score">0</div>
                    </div>
                </div>
                ''', unsafe_allow_html=True)
        
        with award_col14:
            # Dark Horse (surprising performer with low expectations)
            dark_horses = []
            for driver_info in drivers:
                driver = driver_info['driver']
                headstart = st.session_state.driver_headstarts.get(driver, 1)
                points = st.session_state.total_driver_points[driver]
                wins = st.session_state.driver_wins[driver]
                if headstart <= 3 and (points > 30 or wins > 0):
                    dark_horses.append((driver, points, wins, headstart))
            
            if dark_horses:
                best_dark_horse = max(dark_horses, key=lambda x: (x[2], x[1]))
                driver_team = next(d['team'] for d in drivers if d['driver'] == best_dark_horse[0])
                st.markdown(f'''
                <div class="rating-card" style="background: linear-gradient(135deg, #34495e 0%, #2c3e50 100%); color: #ffffff;">
                    <div class="rating-header">
                        <div>
                            <div class="driver-name" style="color: #ffffff;">🐎 Dark Horse</div>
                            <div class="team-name" style="color: #ffffff;">{best_dark_horse[0]} ({driver_team})</div>
                        </div>
                        <div class="rating-score" style="color: #ffffff;">{best_dark_horse[1]} pts</div>
                    </div>
                    <div class="rating-details" style="color: #ffffff;">
                        <span>Low Expectations</span>
                        <span>Wins: {best_dark_horse[2]}</span>
                    </div>
                </div>
                ''', unsafe_allow_html=True)
            else:
                st.markdown(f'''
                <div class="rating-card" style="background: linear-gradient(135deg, #34495e 0%, #2c3e50 100%); color: #ffffff;">
                    <div class="rating-header">
                        <div>
                            <div class="driver-name" style="color: #ffffff;">🐎 Dark Horse</div>
                            <div class="team-name" style="color: #ffffff;">No dark horses yet</div>
                        </div>
                        <div class="rating-score" style="color: #ffffff;">0</div>
                    </div>
                </div>
                ''', unsafe_allow_html=True)
        
        with award_col15:
            # Veteran Excellence (consistent points without being championship leader)
            veterans = []
            championship_leader = sorted_driver_standings[0][0] if sorted_driver_standings else None
            for driver, points in sorted_driver_standings[1:6]:  # Top 2-6 drivers
                if points > 0:
                    consistency_score = points / st.session_state.races_completed
                    podiums = st.session_state.driver_podiums[driver]
                    veterans.append((driver, consistency_score, points, podiums))
            
            if veterans:
                best_veteran = max(veterans, key=lambda x: x[1])
                driver_team = next(d['team'] for d in drivers if d['driver'] == best_veteran[0])
                st.markdown(f'''
                <div class="rating-card" style="background: linear-gradient(135deg, #9c88ff 0%, #8c7ae6 100%); color: #000000;">
                    <div class="rating-header">
                        <div>
                            <div class="driver-name">🎖️ Veteran Excellence</div>
                            <div class="team-name">{best_veteran[0]} ({driver_team})</div>
                        </div>
                        <div class="rating-score">{best_veteran[1]:.1f}</div>
                    </div>
                    <div class="rating-details">
                        <span>Consistent Performer</span>
                        <span>{best_veteran[2]} pts, {best_veteran[3]} podiums</span>
                    </div>
                </div>
                ''', unsafe_allow_html=True)
            else:
                st.markdown(f'''
                <div class="rating-card" style="background: linear-gradient(135deg, #9c88ff 0%, #8c7ae6 100%); color: #000000;">
                    <div class="rating-header">
                        <div>
                            <div class="driver-name">🎖️ Veteran Excellence</div>
                            <div class="team-name">No veterans yet</div>
                        </div>
                        <div class="rating-score">0</div>
                    </div>
                </div>
                ''', unsafe_allow_html=True)
        
        # Row 6: Fun & Special Categories
        st.markdown("---")
        award_col16, award_col17, award_col18 = st.columns(3)
        
        with award_col16:
            # Lucky Charm (driver who gets points despite low performance indicators)
            lucky_charms = []
            for driver_info in drivers:
                driver = driver_info['driver']
                points = st.session_state.total_driver_points[driver]
                wins = st.session_state.driver_wins[driver]
                podiums = st.session_state.driver_podiums[driver]
                if points > 15 and wins == 0 and podiums <= 1:
                    lucky_charms.append((driver, points))
            
            if lucky_charms:
                luckiest_driver = max(lucky_charms, key=lambda x: x[1])
                driver_team = next(d['team'] for d in drivers if d['driver'] == luckiest_driver[0])
                st.markdown(f'''
                <div class="rating-card" style="background: linear-gradient(135deg, #00d2d3 0%, #00a8cc 100%); color: #000000;">
                    <div class="rating-header">
                        <div>
                            <div class="driver-name">🍀 Lucky Charm</div>
                            <div class="team-name">{luckiest_driver[0]} ({driver_team})</div>
                        </div>
                        <div class="rating-score">{luckiest_driver[1]} pts</div>
                    </div>
                    <div class="rating-details">
                        <span>Points Without Glory</span>
                        <span>Solid Finisher</span>
                    </div>
                </div>
                ''', unsafe_allow_html=True)
            else:
                st.markdown(f'''
                <div class="rating-card" style="background: linear-gradient(135deg, #00d2d3 0%, #00a8cc 100%); color: #000000;">
                    <div class="rating-header">
                        <div>
                            <div class="driver-name">🍀 Lucky Charm</div>
                            <div class="team-name">No lucky drivers yet</div>
                        </div>
                        <div class="rating-score">0</div>
                    </div>
                </div>
                ''', unsafe_allow_html=True)
        
        with award_col17:
            # Perfect Storm (team with both drivers performing well)
            perfect_storms = []
            for team, team_drivers in teams_drivers.items():
                driver1, driver2 = team_drivers
                driver1_points = st.session_state.total_driver_points[driver1]
                driver2_points = st.session_state.total_driver_points[driver2]
                min_points = min(driver1_points, driver2_points)
                total_points = driver1_points + driver2_points
                
                if min_points > 20 and total_points > 60:
                    perfect_storms.append((team, total_points, min_points))
            
            if perfect_storms:
                best_storm = max(perfect_storms, key=lambda x: x[2])
                st.markdown(f'''
                <div class="rating-card" style="background: linear-gradient(135deg, #ff9ff3 0%, #f368e0 100%); color: #000000;">
                    <div class="rating-header">
                        <div>
                            <div class="driver-name">⛈️ Perfect Storm</div>
                            <div class="team-name">{best_storm[0]}</div>
                        </div>
                        <div class="rating-score">{best_storm[1]} pts</div>
                    </div>
                    <div class="rating-details">
                        <span>Both Drivers Excel</span>
                        <span>Min: {best_storm[2]} pts</span>
                    </div>
                </div>
                ''', unsafe_allow_html=True)
            else:
                st.markdown(f'''
                <div class="rating-card" style="background: linear-gradient(135deg, #ff9ff3 0%, #f368e0 100%); color: #000000;">
                    <div class="rating-header">
                        <div>
                            <div class="driver-name">⛈️ Perfect Storm</div>
                            <div class="team-name">No perfect storms yet</div>
                        </div>
                        <div class="rating-score">0</div>
                    </div>
                </div>
                ''', unsafe_allow_html=True)
        
        with award_col18:
            # Overachiever (best points-to-headstart ratio)
            overachievers = []
            for driver_info in drivers:
                driver = driver_info['driver']
                headstart = st.session_state.driver_headstarts.get(driver, 1)
                points = st.session_state.total_driver_points[driver]
                if points > 0:
                    ratio = points / headstart
                    overachievers.append((driver, ratio, points, headstart))
            
            if overachievers:
                best_overachiever = max(overachievers, key=lambda x: x[1])
                driver_team = next(d['team'] for d in drivers if d['driver'] == best_overachiever[0])
                st.markdown(f'''
                <div class="rating-card" style="background: linear-gradient(135deg, #48dbfb 0%, #0abde3 100%); color: #000000;">
                    <div class="rating-header">
                        <div>
                            <div class="driver-name">🚀 Overachiever</div>
                            <div class="team-name">{best_overachiever[0]} ({driver_team})</div>
                        </div>
                        <div class="rating-score">{best_overachiever[1]:.1f}</div>
                    </div>
                    <div class="rating-details">
                        <span>Points/Headstart Ratio</span>
                        <span>{best_overachiever[2]} pts @ {best_overachiever[3]}%</span>
                    </div>
                </div>
                ''', unsafe_allow_html=True)
            else:
                st.markdown(f'''
                <div class="rating-card" style="background: linear-gradient(135deg, #48dbfb 0%, #0abde3 100%); color: #000000;">
                    <div class="rating-header">
                        <div>
                            <div class="driver-name">🚀 Overachiever</div>
                            <div class="team-name">No overachievers yet</div>
                        </div>
                        <div class="rating-score">0</div>
                    </div>
                </div>
                ''', unsafe_allow_html=True)
        
        # Row 7: Final Special Recognition
        st.markdown("---")
        award_col19, award_col20, award_col21 = st.columns(3)
        
        with award_col19:
            # Breakthrough Driver (first win of the season)
            if st.session_state.race_summaries:
                first_time_winners = []
                seen_winners = set()
                for summary in st.session_state.race_summaries:
                    winner = summary["P1"].split(' (')[0]
                    if winner not in seen_winners:
                        first_time_winners.append(winner)
                        seen_winners.add(winner)
                
                if first_time_winners:
                    breakthrough_driver = first_time_winners[0]  # First unique winner
                    driver_team = next(d['team'] for d in drivers if d['driver'] == breakthrough_driver)
                    total_wins = st.session_state.driver_wins[breakthrough_driver]
                    st.markdown(f'''
                    <div class="rating-card" style="background: linear-gradient(135deg, #ff6348 0%, #ff3838 100%); color: #000000;">
                        <div class="rating-header">
                            <div>
                                <div class="driver-name">💥 Breakthrough Driver</div>
                                <div class="team-name">{breakthrough_driver} ({driver_team})</div>
                            </div>
                            <div class="rating-score">{total_wins}</div>
                        </div>
                        <div class="rating-details">
                            <span>First Season Winner</span>
                            <span>Made History</span>
                        </div>
                    </div>
                    ''', unsafe_allow_html=True)
                else:
                    st.markdown(f'''
                    <div class="rating-card" style="background: linear-gradient(135deg, #ff6348 0%, #ff3838 100%); color: #000000;">
                        <div class="rating-header">
                            <div>
                                <div class="driver-name">💥 Breakthrough Driver</div>
                                <div class="team-name">No breakthroughs yet</div>
                            </div>
                            <div class="rating-score">0</div>
                        </div>
                    </div>
                    ''', unsafe_allow_html=True)
            else:
                st.markdown(f'''
                <div class="rating-card" style="background: linear-gradient(135deg, #ff6348 0%, #ff3838 100%); color: #000000;">
                    <div class="rating-header">
                        <div>
                            <div class="driver-name">💥 Breakthrough Driver</div>
                            <div class="team-name">No breakthroughs yet</div>
                        </div>
                        <div class="rating-score">0</div>
                    </div>
                </div>
                ''', unsafe_allow_html=True)
        
        with award_col20:
            # Team Harmony (team with most balanced driver contributions)
            harmony_teams = []
            for team, team_drivers in teams_drivers.items():
                driver1, driver2 = team_drivers
                driver1_points = st.session_state.total_driver_points[driver1]
                driver2_points = st.session_state.total_driver_points[driver2]
                total_points = driver1_points + driver2_points
                
                if total_points > 0:
                    balance_score = min(driver1_points, driver2_points) / max(driver1_points, driver2_points) if max(driver1_points, driver2_points) > 0 else 0
                    harmony_teams.append((team, balance_score, total_points, min(driver1_points, driver2_points)))
            
            if harmony_teams:
                most_harmonious = max(harmony_teams, key=lambda x: (x[1], x[3]))
                st.markdown(f'''
                <div class="rating-card" style="background: linear-gradient(135deg, #ffa726 0%, #ff9800 100%); color: #000000;">
                    <div class="rating-header">
                        <div>
                            <div class="driver-name">🎵 Team Harmony</div>
                            <div class="team-name">{most_harmonious[0]}</div>
                        </div>
                        <div class="rating-score">{most_harmonious[1]:.2f}</div>
                    </div>
                    <div class="rating-details">
                        <span>Perfect Balance</span>
                        <span>Total: {most_harmonious[2]} pts</span>
                    </div>
                </div>
                ''', unsafe_allow_html=True)
            else:
                st.markdown(f'''
                <div class="rating-card" style="background: linear-gradient(135deg, #ffa726 0%, #ff9800 100%); color: #000000;">
                    <div class="rating-header">
                        <div>
                            <div class="driver-name">🎵 Team Harmony</div>
                            <div class="team-name">No harmony yet</div>
                        </div>
                        <div class="rating-score">0</div>
                    </div>
                </div>
                ''', unsafe_allow_html=True)
        
        with award_col21:
            # Championship Contender (top 3 in points with multiple podiums)
            contenders = []
            for driver, points in sorted_driver_standings[:5]:
                podiums = st.session_state.driver_podiums[driver]
                wins = st.session_state.driver_wins[driver]
                if points > 25 and podiums >= 2:
                    championship_score = (wins * 3) + (podiums * 2) + (points * 0.1)
                    contenders.append((driver, championship_score, points, wins, podiums))
            
            if contenders:
                top_contender = max(contenders, key=lambda x: x[1])
                driver_team = next(d['team'] for d in drivers if d['driver'] == top_contender[0])
                st.markdown(f'''
                <div class="rating-card" style="background: linear-gradient(135deg, #a55eea 0%, #8854d0 100%); color: #000000;">
                    <div class="rating-header">
                        <div>
                            <div class="driver-name">🏁 Championship Contender</div>
                            <div class="team-name">{top_contender[0]} ({driver_team})</div>
                        </div>
                        <div class="rating-score">{top_contender[1]:.0f}</div>
                    </div>
                    <div class="rating-details">
                        <span>Championship Score</span>
                        <span>{top_contender[3]}W {top_contender[4]}P</span>
                    </div>
                </div>
                ''', unsafe_allow_html=True)
            else:
                st.markdown(f'''
                <div class="rating-card" style="background: linear-gradient(135deg, #a55eea 0%, #8854d0 100%); color: #000000;">
                    <div class="rating-header">
                        <div>
                            <div class="driver-name">🏁 Championship Contender</div>
                            <div class="team-name">No contenders yet</div>
                        </div>
                        <div class="rating-score">0</div>
                    </div>
                </div>
                ''', unsafe_allow_html=True)
    
    else:
        st.markdown('<div class="rating-card">', unsafe_allow_html=True)
        st.markdown("#### 🏁 No Data Available")
        st.write("Complete some races to see the season summary!")
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

#     New Awards Added:

# Mr. Reliable (Green) - Consistent points without wins
# Rising Star (Orange) - Best performing rookie/newcomer
# Giant Killer (Red) - Beats favored teammates
# Comeback King (Yellow) - Strong podium performance
# Speed Demon (Pink-Red) - High headstart performers
# Dark Horse (Dark Blue) - Surprising low-expectation performers
# Veteran Excellence (Purple) - Consistent top performers
# Lucky Charm (Cyan) - Points without glory
# Perfect Storm (Pink) - Teams with both drivers excelling
# Overachiever (Light Blue) - Best points-to-headstart ratio
# Breakthrough Driver (Red-Orange) - First unique winner
# Team Harmony (Orange) - Most balanced teammate performance
# Championship Contender (Purple) - Top championship potential
