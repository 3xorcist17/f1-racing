import streamlit as st
import random
import time
import pandas as pd
import plotly.express as px

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
    "Racing Bulls": "hsl(198, 99.6%, 93.8%)",
    "Red Bull": "hsl(247, 99.6%, 24.1%)",
    "Sauber": "hsl(124, 99.6%, 31.4%)",
    "Williams": "hsl(201, 99.6%, 32.2%)"
}

# Driver colors with slight variation (±5% lightness)
driver_colors = {}
for team, drivers in teams_drivers.items():
    color_parts = team_colors[team].replace('hsl(', '').replace(')', '').split(',')
    hue = float(color_parts[0])
    saturation = float(color_parts[1].replace('%', ''))
    lightness = float(color_parts[2].replace('%', ''))
    driver_colors[drivers[0]] = f"hsl({hue}, {saturation}%, {min(100, lightness + 5)}%)"
    driver_colors[drivers[1]] = f"hsl({hue}, {saturation}%, {max(0, lightness - 5)}%)"

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
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "Race & Results",
    "Drivers' Championship",
    "Constructors' Championship",
    "Team & Driver Stats",
    "Driver Upgrades"
])

# Tab 1: Race and Current Results (Podium)
with tab1:
    col1, col2 = st.columns([2, 1])
    
    with col1:
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

        # Display initial headstarts before race simulation
        if st.session_state.race_started and not st.session_state.race_finished:
            # st.markdown("### Initial Headstarts")
            # headstart_display = [
            #     {"Driver": driver_info['driver'], "Team": driver_info['team'], "Headstart (%)": st.session_state.progress_values[i]}
            #     for i, driver_info in enumerate(drivers)
            # ]
            # st.dataframe(pd.DataFrame(headstart_display), use_container_width=True, hide_index=True)
            # st.markdown("---")

            cols = [st.columns([1, 3]) for _ in range(20)]
            progress_bars = []
            for i in range(20):
                with cols[i][0]:
                    st.write(f"**{drivers[i]['driver']} ({drivers[i]['team']})**")
                with cols[i][1]:
                    progress_bars.append(st.progress(st.session_state.progress_values[i] / 100))

            leaderboard_placeholder = col2.empty()
            
            current_leaderboard = get_current_leaderboard()
            with leaderboard_placeholder.container():
                st.markdown("### 🏁 Live Leaderboard")
                st.markdown('<div class="leaderboard">', unsafe_allow_html=True)
                
                for pos, driver_info in enumerate(current_leaderboard, 1):
                    progress = driver_info['progress']
                    driver = driver_info['driver']
                    team = driver_info['team']
                    is_finished = driver_info.get('finished', False)
                    
                    position_class = ""
                    medal = ""
                    if pos == 1:
                        position_class = "position-1"
                        medal = "🥇 "
                    elif pos == 2:
                        position_class = "position-2"
                        medal = "🥈 "
                    elif pos == 3:
                        position_class = "position-3"
                        medal = "🥉 "
                    
                    if is_finished:
                        progress_display = "FINISHED"
                        if st.session_state.race_finished:
                            points = points_system.get(pos, 0)
                            if pos <= 10:
                                progress_display = f"FINISHED ({points} pts)"
                    else:
                        progress_display = f"{progress:.1f}%"
                    
                    st.markdown(f'''
                    <div class="leaderboard-item {position_class}">
                        <span><strong>{medal}P{pos}: {driver}</strong> ({team})</span>
                        <span><strong>{progress_display}</strong></span>
                    </div>
                    ''', unsafe_allow_html=True)
                
                st.markdown('</div>', unsafe_allow_html=True)

            # Brief pause to show initial headstarts
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
                        progress_bars[i].progress(st.session_state.progress_values[i] / 100)
                
                    current_leaderboard = get_current_leaderboard()
                    with leaderboard_placeholder.container():
                        st.markdown("### 🏁 Live Leaderboard")
                        st.markdown('<div class="leaderboard">', unsafe_allow_html=True)
                        
                        for pos, driver_info in enumerate(current_leaderboard, 1):
                            progress = driver_info['progress']
                            driver = driver_info['driver']
                            team = driver_info['team']
                            is_finished = driver_info.get('finished', False)
                            
                            position_class = ""
                            medal = ""
                            if pos == 1:
                                position_class = "position-1"
                                medal = "🥇 "
                            elif pos == 2:
                                position_class = "position-2"
                                medal = "🥈 "
                            elif pos == 3:
                                position_class = "position-3"
                                medal = "🥉 "
                            
                            if is_finished:
                                progress_display = "🏁 FINISHED"
                            else:
                                progress_display = f"{progress:.1f}%"
                            
                            st.markdown(f'''
                            <div class="leaderboard-item {position_class}">
                                <span><strong>{medal}P{pos}: {driver}</strong> ({team})</span>
                                <span><strong>{progress_display}</strong></span>
                            </div>
                            ''', unsafe_allow_html=True)
                        
                        st.markdown('</div>', unsafe_allow_html=True)
                
                if len(st.session_state.finish_order) == 20:
                    st.session_state.race_finished = True
                    st.session_state.races_completed += 1
                    st.session_state.race_started = False
                    
                    current_leaderboard = get_current_leaderboard()
                    with leaderboard_placeholder.container():
                        st.markdown("### 🏁 Leaderboard")
                        st.markdown('<div class="leaderboard">', unsafe_allow_html=True)
                        
                        for pos, driver_info in enumerate(current_leaderboard, 1):
                            driver = driver_info['driver']
                            team = driver_info['team']
                            points = points_system.get(pos, 0)
                            
                            position_class = ""
                            medal = ""
                            if pos == 1:
                                position_class = "position-1"
                                medal = "🥇 "
                            elif pos == 2:
                                position_class = "position-2"
                                medal = "🥈 "
                            elif pos == 3:
                                position_class = "position-3"
                                medal = "🥉 "
                            
                            if pos <= 10:
                                progress_display = f"{points} pts"
                            else:
                                progress_display = "0 pts"
                            
                            st.markdown(f'''
                            <div class="leaderboard-item {position_class}">
                                <span><strong>{medal}P{pos}: {driver}</strong> ({team})</span>
                                <span><strong>{progress_display}</strong></span>
                            </div>
                            ''', unsafe_allow_html=True)
                        
                        st.markdown('</div>', unsafe_allow_html=True)
                    
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

    with col2:
        if not st.session_state.race_started and not st.session_state.race_finished:
            st.markdown("### 🏁 Leaderboard")
            #st.write("Click '🏁 Start Race' to begin!")

    if st.session_state.race_finished:
        st.markdown("---")
        st.subheader("🏆 Podium")
        for position, driver_info in enumerate(st.session_state.finish_order, 1):
            points = points_system.get(position, 0)
            driver = driver_info['driver']
            team = driver_info['team']
            if position == 1:
                st.write(f"🥇 **P1: {driver} ({team})** - {points} points")
            elif position == 2:
                st.write(f"🥈 **P2: {driver} ({team})** - {points} points")
            elif position == 3:
                st.write(f"🥉 **P3: {driver} ({team})** - {points} points")
            elif position <= 10:
                pass
            else:
                pass

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
    driver_standings_data = []
    for pos, (driver, points) in enumerate(sorted_driver_standings, 1):
        team = next(d['team'] for d in drivers if d['driver'] == driver)
        driver_standings_data.append({"Position": pos, "Driver": driver, "Team": team, "Total Points": points})
    driver_df = pd.DataFrame(driver_standings_data)
    st.dataframe(driver_df, use_container_width=True, hide_index=True)

    st.markdown("### Drivers' Points Distribution")
    # Prepare data for grouped bar chart, sorted by team and points within team
    team_driver_data = []
    for team in teams_drivers.keys():
        driver1, driver2 = teams_drivers[team]
        driver1_points = st.session_state.total_driver_points.get(driver1, 0)
        driver2_points = st.session_state.total_driver_points.get(driver2, 0)
        # Sort drivers within team by points (highest first)
        drivers_data = sorted([
            {"Driver": driver1, "Points": driver1_points, "Color": driver_colors[driver1]},
            {"Driver": driver2, "Points": driver2_points, "Color": driver_colors[driver2]}
        ], key=lambda x: x["Points"], reverse=True)
        for driver_data in drivers_data:
            team_driver_data.append({"Team": team, "Driver": driver_data["Driver"], "Points": driver_data["Points"], "Color": driver_data["Color"]})

    if team_driver_data:
        team_driver_df = pd.DataFrame(team_driver_data)
        # Sort teams by total points of their drivers (sum of both)
        team_points = {team: sum(d["Points"] for d in [d for d in team_driver_data if d["Team"] == team]) for team in teams_drivers}
        team_driver_df['TeamOrder'] = team_driver_df['Team'].map(lambda x: team_points[x])
        team_driver_df = team_driver_df.sort_values(by=['TeamOrder', 'Points'], ascending=[False, False]).drop(columns=['TeamOrder'])

        # Debug: Display the DataFrame to verify structure
        st.write("Debug: DataFrame for Bar Chart")
        st.dataframe(team_driver_df, use_container_width=True, hide_index=True)

        # Create grouped bar chart with team grouping and driver colors
        fig = px.bar(
            team_driver_df,
            x="Team",
            y="Points",
            color="Driver",
            barmode="group",
            text="Points",
            color_discrete_map={row["Driver"]: row["Color"] for _, row in team_driver_df.iterrows()}
        )
        fig.update_traces(textposition="outside", texttemplate="%{text:.0f}", width=0.6)  # Maintain wide bars
        fig.update_layout(
            height=600,
            width=1000,
            xaxis_title="Team",
            yaxis_title="Points",
            legend_title="Driver",
            bargap=0.2,  # Gap between team groups
            bargroupgap=0.1,  # Gap between driver bars within team
            font=dict(size=12),
            title="Driver Points by Team",
            title_font_size=16
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.write("No points data available yet. Please complete a race in the 'Race & Results' tab.")

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
            
            # Update colors and add driver name labels
            for i, trace in enumerate(fig_bar.data):
                driver_name = trace.name
                trace.marker.color = driver_colors[driver_name]
                
                # Create custom text labels showing driver name and points
                custom_text = []
                for j, value in enumerate(trace.y):
                    if value > 0:  # Only show label if driver has points
                        custom_text.append(f"{driver_name}<br>{value}")
                    else:
                        custom_text.append("")
                
                trace.text = custom_text
                trace.textposition = "inside"
                trace.textfont = dict(size=10, color="white")
            
            fig_bar.update_layout(
                height=500,
                xaxis_title="Team",
                yaxis_title="Points",
                legend_title="Driver",
                barmode="stack",
                showlegend=True
            )
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
