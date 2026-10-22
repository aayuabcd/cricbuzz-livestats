"""Cricbuzz LiveStats: cinematic cricket intelligence app backed by local SQLite."""
from __future__ import annotations

import base64
import sqlite3
from pathlib import Path

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from utils.cricket_api import get_current_matches, format_scores, CricketAPIError
from utils.db_connection import fetch_all, fetch_one, get_table_counts
from utils.crud import create_team, update_team, delete_team, create_player, update_player, delete_player

ROOT = Path(__file__).resolve().parent
st.set_page_config(page_title="Cricbuzz LiveStats | Cricket, Decoded", page_icon="🏏", layout="wide", initial_sidebar_state="collapsed")


def image_css() -> str:
    path = ROOT / "assets" / "stadium_atmosphere.jpg"
    if not path.exists():
        return ""
    encoded = base64.b64encode(path.read_bytes()).decode("ascii")
    return f"background-image:linear-gradient(90deg,rgba(5,12,26,.94) 0%,rgba(6,14,28,.76) 48%,rgba(6,13,25,.34) 100%),url('data:image/jpeg;base64,{encoded}');"


st.markdown("""<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&family=Rajdhani:wght@600;700&family=JetBrains+Mono:wght@400;600&display=swap');
:root {color-scheme:dark;}
html,body,[class*="css"],[data-testid="stApp"]{font-family:'Space Grotesk',sans-serif}
.stApp{background:#080f1e;color:#eaf7ff}
[data-testid="stHeader"]{background:transparent;height:2.6rem}
[data-testid="stToolbar"]{right:0}
.block-container{max-width:1500px;padding-top:1.1rem;padding-bottom:3rem}
[data-testid="stSidebar"]{background:#0d1828}
[data-testid="stSidebar"] *{color:#eaf7ff}
h1,h2,h3{font-family:'Rajdhani',sans-serif!important;letter-spacing:.3px}
h2{color:#f6fcff!important}
.stButton>button{background:linear-gradient(110deg,#17ef98,#22c55e);border:0;border-radius:11px;color:#071a17;font-weight:800;min-height:46px;box-shadow:0 0 22px #12e99735;transition:.2s}
.stButton>button:hover{background:#7affcb;color:#061911;transform:translateY(-2px);box-shadow:0 0 30px #22c55e77}
.stButton>button:focus{color:#071a17}
button[kind="secondary"]{background:rgba(11,28,45,.94)!important;color:#d4e9f5!important;border:1px solid #28546b!important;box-shadow:none!important}
button[kind="secondary"]:hover{border-color:#22f4a4!important;color:#22f4a4!important;transform:none!important}
[data-testid="stMetric"]{background:linear-gradient(145deg,rgba(18,41,58,.95),rgba(10,25,41,.95));border:1px solid #28526a;border-radius:16px;padding:18px}
[data-testid="stMetricLabel"] *{color:#b7d0e0!important}
[data-testid="stMetricValue"]{color:#2cf5ad!important;font-family:'JetBrains Mono',monospace}
[data-testid="stDataFrame"]{border:1px solid #29506a;border-radius:12px}
[data-testid="stTabs"] button{font-weight:700}
.stSelectbox label,.stTextArea label{color:#c7deee!important}
.brand{font-family:'Rajdhani',sans-serif;font-weight:700;font-size:26px;color:white;letter-spacing:.5px}
.brand span{color:#20f3a4}
.navline{background:rgba(8,20,36,.8);border:1px solid #285069;border-radius:16px;padding:13px 20px;backdrop-filter:blur(15px);color:#cde6f3;font-size:13px;margin-bottom:13px}
.navline b{color:#25f6a9}
.hero{position:relative;overflow:hidden;min-height:460px;border:1px solid #2b5669;border-radius:25px;padding:60px 5%;background-position:center center;background-size:cover;box-shadow:0 22px 70px #0008}
.hero:before{content:'';position:absolute;inset:0;background:radial-gradient(circle at 77% 38%,transparent 0%,rgba(0,15,29,.45) 70%);pointer-events:none}
.hero>*{position:relative;z-index:1}
.kicker{color:#3af4b4;font:600 11px 'JetBrains Mono',monospace;letter-spacing:3px;margin-bottom:16px}
.hero h1{font-family:'Rajdhani',sans-serif!important;color:white;font-size:clamp(52px,6vw,95px);line-height:.92;letter-spacing:-1px;font-style:italic;margin:0 0 20px;font-weight:700;max-width:850px;text-shadow:0 5px 24px #0009}
.hero h1 em{color:#27f3a7;font-style:italic;text-shadow:0 0 34px #00ff9955}
.hero p{font-size:17px;max-width:620px;line-height:1.7;color:#c4ddec}
.tag{display:inline-block;background:#0c382e;border:1px solid #17865f;color:#80ffcc;border-radius:99px;padding:7px 13px;font:600 11px 'JetBrains Mono',monospace;margin-top:17px}
.card{background:linear-gradient(145deg,rgba(17,40,59,.95),rgba(9,22,39,.97));border:1px solid #28546b;border-radius:19px;padding:23px;min-height:185px;box-shadow:0 12px 34px #0003;transition:transform .2s,border-color .2s}
.card:hover{transform:translateY(-4px);border-color:#29dcb0}
.card h3{font-size:24px;color:#fff;margin:0 0 9px}
.card p{font-size:13px;color:#b6cedf;line-height:1.7;margin:0}
.card .icon{font-size:31px;margin-bottom:12px}
.card.green{border-top:3px solid #22f4a4}.card.blue{border-top:3px solid #00cfff}.card.purple{border-top:3px solid #c37dff}.card.gold{border-top:3px solid #ffc04a}
.section-tag{font:600 11px 'JetBrains Mono',monospace;color:#29e9ac;letter-spacing:2px;margin-top:26px}
.status{background:rgba(15,40,52,.8);border:1px solid #326178;border-radius:11px;padding:10px 15px;color:#c4dce8;font-size:12px;margin:14px 0}
.scorecard{background:linear-gradient(135deg,#122b3c,#0c192d);border:1px solid #286278;border-radius:17px;padding:23px;margin:14px 0}
.scorecard .teams{font-family:'Rajdhani',sans-serif;font-size:28px;font-weight:700;color:white}
.scorecard .sub{color:#a8c5d7;font-size:13px}
.codehint{font-family:'JetBrains Mono',monospace;color:#40e7bd;font-size:12px}
[data-testid="stAlert"]{border-radius:12px}
@media(max-width:800px){.hero{min-height:360px;padding:40px 25px}.hero h1{font-size:52px}.block-container{padding-left:1rem;padding-right:1rem}}
</style>""", unsafe_allow_html=True)


def df(sql: str, params: tuple = ()) -> pd.DataFrame:
    return pd.DataFrame([dict(r) for r in fetch_all(sql, params)])


def chart(fig):
    fig.update_layout(template="plotly_dark",paper_bgcolor="rgba(0,0,0,0)",plot_bgcolor="rgba(0,0,0,0)",font_color="#d5e8f6",margin=dict(l=10,r=10,t=35,b=15))
    st.plotly_chart(fig,use_container_width=True)


def show_table(data: pd.DataFrame):
    if data.empty:
        st.info("No records available yet.")
    else:
        st.dataframe(data,use_container_width=True,hide_index=True)


try:
    counts = get_table_counts()
    row = fetch_one("SELECT COALESCE(SUM(total_runs),0) AS total FROM innings")
    total_runs = int(row["total"]) if row else 0
    matches = df("""SELECT m.match_id,m.match_date AS Date,m.match_type AS Format,m.status AS Status,
       a.team_name AS Team_1,b.team_name AS Team_2,COALESCE(v.venue_name,'Venue pending') AS Venue,
       COALESCE(m.result_text,'No result recorded') AS Result
       FROM matches m JOIN teams a ON a.team_id=m.team1_id JOIN teams b ON b.team_id=m.team2_id
       LEFT JOIN venues v ON v.venue_id=m.venue_id ORDER BY m.match_date DESC,m.match_id DESC""")
    batting = df("""SELECT p.full_name AS Player,COALESCE(t.team_name,'Unassigned') AS Team,
       SUM(s.runs) AS Runs,SUM(s.balls_faced) AS Balls,SUM(s.fours) AS Fours,SUM(s.sixes) AS Sixes
       FROM batting_stats s JOIN players p ON p.player_id=s.player_id
       LEFT JOIN teams t ON t.team_id=p.team_id GROUP BY p.player_id,p.full_name,t.team_name ORDER BY Runs DESC""")
    bowling = df("""SELECT p.full_name AS Player,COALESCE(t.team_name,'Unassigned') AS Team,
       SUM(s.wickets) AS Wickets,SUM(s.runs_conceded) AS Runs_Conceded
       FROM bowling_stats s JOIN players p ON p.player_id=s.player_id
       LEFT JOIN teams t ON t.team_id=p.team_id GROUP BY p.player_id,p.full_name,t.team_name
       ORDER BY Wickets DESC,Runs_Conceded ASC""")
except (sqlite3.Error, OSError, KeyError) as error:
    st.error(f"Could not load database: {error}")
    st.info("Run `python database/init_db.py` from the project root and check the database seed.")
    st.stop()

# Native Streamlit navigation buttons: every click updates the active section.
PAGES = ["🏟️ Command Center", "🏏 Match Center", "👤 Player Matrix", "💻 SQL Intelligence", "📊 Team Analytics", "🛠️ Data Manager"]
if st.session_state.get("active_page") not in PAGES:
    st.session_state["active_page"] = PAGES[0]

st.markdown('<div class="brand">🏏 Cricbuzz <span>LiveStats</span></div>', unsafe_allow_html=True)
nav_columns = st.columns(len(PAGES), gap="small")
for nav_col, nav_page in zip(nav_columns, PAGES):
    with nav_col:
        if st.button(
            nav_page,
            key="nav_" + str(PAGES.index(nav_page)),
            use_container_width=True,
            type="primary" if st.session_state["active_page"] == nav_page else "secondary",
        ):
            st.session_state["active_page"] = nav_page
            st.rerun()
page = st.session_state["active_page"]
st.markdown('<div class="navline"><b>● CRICKET INTELLIGENCE PLATFORM</b> &nbsp; / &nbsp; INTERACTIVE SPORTS ANALYTICS &nbsp; / &nbsp; LOCAL DEMO DATABASE</div>',unsafe_allow_html=True)

if page == "🏟️ Command Center":
    st.markdown(f'<section class="hero" style="{image_css()}"><div class="kicker">THE NEXT GENERATION OF CRICKET ANALYTICS</div><h1>CRICKET,<br><em>DECODED</em> VIA CODE.</h1><p>Explore match intelligence, player performance, advanced visualizations and SQL-powered cricket analytics in one immersive command center.</p><div class="tag">● SYNTHETIC DEMO DATA · LIVE API COMING LATER</div></section>',unsafe_allow_html=True)
    c1,c2,c3 = st.columns([1.15,1.15,2.7])
    with c1:
        if st.button("⚡ LAUNCH INTELLIGENCE",use_container_width=True):
            st.session_state["active_page"] = "🏏 Match Center"
            st.rerun()
    with c2:
        if st.button("⌘ QUERY DATABASE",use_container_width=True):
            st.session_state["active_page"] = "💻 SQL Intelligence"
            st.rerun()
    with c3:
        st.caption("Real database statistics below · all current records are synthetic examples")
    st.markdown('<div class="section-tag">01 / CRICKET COMMAND CENTER</div>',unsafe_allow_html=True)
    st.subheader("Your match intelligence, at a glance")
    a,b,c,d=st.columns(4)
    a.metric("🏆 TOTAL MATCHES",counts["matches"])
    b.metric("👥 TOTAL PLAYERS",counts["players"])
    c.metric("🌐 TOTAL TEAMS",counts["teams"])
    d.metric("⚡ TOTAL RUNS",f"{total_runs:,}")
    st.markdown('<div class="section-tag">02 / EXPLORE THE PLATFORM</div>',unsafe_allow_html=True)
    x,y,z,w=st.columns(4)
    cards=[("green","🏟️","MATCH INTELLIGENCE","Match scorecards, innings breakdowns and cricket performance trends."),
           ("blue","👤","PLAYER MATRIX","Batting and bowling leaderboards, rankings and interactive comparisons."),
           ("purple","⌘","SQL INTELLIGENCE LAB","Run verified SQL recipes, explore query results and export CSV files."),
           ("gold","🏆","TEAM ANALYTICS","Explore teams, match records and data-driven head-to-head comparisons.")]
    for col,(tone,emoji,title,desc) in zip((x,y,z,w),cards):
        with col:
            st.markdown(f'<div class="card {tone}"><div class="icon">{emoji}</div><h3>{title}</h3><p>{desc}</p></div>',unsafe_allow_html=True)
    st.markdown('<div class="section-tag">03 / PERFORMANCE SNAPSHOT</div>',unsafe_allow_html=True)
    a,b=st.columns(2)
    with a:
        st.subheader("Leading run scorers")
        if not batting.empty:
            fig=px.bar(batting.head(8),x="Runs",y="Player",orientation="h",color="Runs",color_continuous_scale=["#115b63","#22f5aa"])
            fig.update_layout(yaxis=dict(categoryorder="total ascending"),coloraxis_showscale=False)
            chart(fig)
        else: st.info("No batting data available.")
    with b:
        st.subheader("Wicket-taking leaders")
        if not bowling.empty:
            fig=px.bar(bowling.head(8),x="Wickets",y="Player",orientation="h",color="Wickets",color_continuous_scale=["#14516b","#00cfff"])
            fig.update_layout(yaxis=dict(categoryorder="total ascending"),coloraxis_showscale=False)
            chart(fig)
        else: st.info("No bowling data available.")

elif page == "🏏 Match Center":
    st.markdown('<div class="section-tag">MATCH INTELLIGENCE / SCORECARDS</div>',unsafe_allow_html=True)
    st.title("MATCH CENTER")
    st.caption("Browse stored matches and inspect innings. Current records are synthetic, not live.")
    if matches.empty: st.info("No matches stored.")
    else:
        formats=["All formats"]+sorted(matches["Format"].dropna().unique().tolist())
        selected=st.selectbox("Match format",formats)
        filtered=matches if selected=="All formats" else matches[matches["Format"]==selected]
        show_table(filtered.drop(columns=["match_id"]))
        if not filtered.empty:
            opts={int(r.match_id):f"{r.Team_1} vs {r.Team_2} — {r.Date}" for r in filtered.itertuples()}
            match_id=st.selectbox("Inspect match",list(opts),format_func=lambda i:opts[i])
            m=filtered[filtered["match_id"]==match_id].iloc[0]
            st.markdown(f'<div class="scorecard"><div class="teams">{m["Team_1"]} &nbsp; VS &nbsp; {m["Team_2"]}</div><div class="sub">{m["Format"]} · {m["Date"]} · {m["Venue"]} · {m["Status"]}</div></div>',unsafe_allow_html=True)
            st.write(m["Result"])
            innings=df("""SELECT i.innings_number AS Innings,t.team_name AS Team,i.total_runs AS Runs,
              i.wickets AS Wickets,i.overs AS Overs,i.extras AS Extras FROM innings i
              JOIN teams t ON t.team_id=i.batting_team_id WHERE i.match_id=? ORDER BY i.innings_number""",(match_id,))
            show_table(innings)
            if not innings.empty:
                fig=px.bar(innings,x="Team",y="Runs",color="Team",title="Runs by innings")
                chart(fig)

elif page == "👤 Player Matrix":
    st.markdown('<div class="section-tag">PERFORMANCE / PLAYER INTELLIGENCE</div>',unsafe_allow_html=True)
    st.title("PLAYER MATRIX")
    profiles=df("""SELECT p.full_name AS Player,COALESCE(t.team_name,'Unassigned') AS Team,
       p.country AS Country,p.role AS Role,COALESCE(p.batting_style,'—') AS Batting_Style
       FROM players p LEFT JOIN teams t ON t.team_id=p.team_id ORDER BY p.full_name""")
    tabs=st.tabs(["🏏 Batting", "🎯 Bowling", "👥 Player Profiles"])
    with tabs[0]:
        show_table(batting)
        if not batting.empty:
            selected=st.selectbox("Select player",batting["Player"].tolist(),key="bat_player")
            r=batting[batting["Player"]==selected].iloc[0]
            a,b,c=st.columns(3)
            a.metric("Runs",int(r["Runs"]));b.metric("Balls",int(r["Balls"]));c.metric("Strike rate",f"{100*r['Runs']/r['Balls']:.1f}" if r["Balls"] else "N/A")
    with tabs[1]:
        show_table(bowling)
    with tabs[2]:
        show_table(profiles)

elif page == "💻 SQL Intelligence":
    st.markdown('<div class="section-tag">ENGINEERING / QUERY WORKSPACE</div>',unsafe_allow_html=True)
    st.title("SQL INTELLIGENCE LAB")
    st.caption("Safe, read-only SQL analytics backed by your project's actual SQLite tables.")
    # Load all 25 version-controlled, read-only SQL recipes from disk.
    query_folder = ROOT / "database" / "queries"
    query_files = sorted(query_folder.glob("*.sql"))
    recipes = {
        path.stem.replace("_", " ").title(): path.read_text(encoding="utf-8-sig")
        for path in query_files
    }
    if not recipes:
        st.error("No SQL recipes found in database/queries. Restore the 25 .sql files.")
        st.stop()
    st.caption(f"{len(recipes)} SQL recipes available · Executed against local SQLite")
    left,right=st.columns([1.05,1.2])
    with left:
        choice=st.selectbox("Query recipe",list(recipes))
        st.code(recipes[choice],language="sql")
        run=st.button("▶ RUN SQL QUERY",use_container_width=True)
    with right:
        st.markdown("#### Query results")
        if run:
            try:
                result=df(recipes[choice])
                st.session_state["query_result"]=result
                st.session_state["query_title"]=choice
            except sqlite3.Error as error:
                st.error(f"SQL error: {error}")
        if "query_result" in st.session_state:
            result=st.session_state["query_result"]
            st.caption(st.session_state.get("query_title","Query"))
            show_table(result)
            if not result.empty:
                st.download_button("⬇ EXPORT CSV",data=result.to_csv(index=False).encode("utf-8"),file_name="cricket_query_results.csv",mime="text/csv")
                nums=result.select_dtypes(include="number").columns.tolist()
                if nums and len(result.columns)>1:
                    category=next((c for c in result.columns if c not in nums),None)
                    if category:
                        chart(px.bar(result.head(20),x=category,y=nums[0],title="Query visualization"))
        else: st.info("Choose a SQL recipe and click Run SQL Query.")
    st.markdown('<div class="status">🔐 Queries are predefined, read-only recipes. Arbitrary SQL execution and database modifications are disabled in this initial version.</div>',unsafe_allow_html=True)

elif page == "📊 Team Analytics":
    st.markdown('<div class="section-tag">TEAM INTELLIGENCE / COMPARISONS</div>',unsafe_allow_html=True)
    st.title("TEAM ANALYTICS")
    teams=df("""SELECT t.team_name AS Team,t.country AS Country,COUNT(DISTINCT p.player_id) AS Players
      FROM teams t LEFT JOIN players p ON p.team_id=t.team_id GROUP BY t.team_id,t.team_name,t.country ORDER BY t.team_name""")
    show_table(teams)
    if not teams.empty:
        chart(px.bar(teams,x="Team",y="Players",color="Team",title="Registered players by team"))
    st.subheader("Match results")
    show_table(matches[["Team_1","Team_2","Format","Date","Status","Result"]] if not matches.empty else matches)


elif page == "🛠️ Data Manager":
    st.markdown('<div class="section-tag">DATABASE / SECURE RECORD MANAGEMENT</div>', unsafe_allow_html=True)
    st.title("CRICKET DATA MANAGER")
    st.caption("Create, view, update and delete team and player records in your local SQLite database. Changes persist after refresh.")
    entity = st.radio("Manage", ["Teams", "Players"], horizontal=True)
    if entity == "Teams":
        records = df("SELECT team_id, team_name, country FROM teams ORDER BY team_name")
        show_table(records)
        action = st.selectbox("Action", ["Create", "Update", "Delete"], key="team_action")
        if action == "Create":
            with st.form("create_team_form", clear_on_submit=True):
                name = st.text_input("Team name", max_chars=100)
                country = st.text_input("Country", max_chars=100)
                submitted = st.form_submit_button("CREATE TEAM")
            if submitted:
                try:
                    create_team(name, country)
                    st.success("Team created successfully.")
                    st.rerun()
                except (ValueError, sqlite3.IntegrityError) as exc:
                    st.error(str(exc))
        elif not records.empty:
            options = dict(zip(records.team_id.astype(int), records.team_name))
            selected_id = st.selectbox("Choose team", list(options), format_func=lambda i: options[i], key="team_selected")
            current = records[records.team_id == selected_id].iloc[0]
            if action == "Update":
                with st.form("update_team_form"):
                    name = st.text_input("Team name", value=str(current.team_name), max_chars=100)
                    country = st.text_input("Country", value=str(current.country), max_chars=100)
                    submitted = st.form_submit_button("SAVE CHANGES")
                if submitted:
                    try:
                        update_team(selected_id, name, country)
                        st.success("Team updated.")
                        st.rerun()
                    except (ValueError, sqlite3.IntegrityError) as exc:
                        st.error(str(exc))
            else:
                st.warning("Deletion is blocked when a team is referenced by players or matches.")
                confirmed = st.checkbox("I understand this will permanently delete the selected team", key="confirm_team")
                if st.button("DELETE TEAM", disabled=not confirmed):
                    try:
                        delete_team(selected_id)
                        st.success("Team deleted.")
                        st.rerun()
                    except (ValueError, sqlite3.IntegrityError) as exc:
                        st.error(str(exc))
        else:
            st.info("Create a team first.")
    else:
        records = df("""SELECT p.player_id,p.full_name,p.team_id,COALESCE(t.team_name,'Unassigned') AS team,
          p.role,p.country FROM players p LEFT JOIN teams t ON t.team_id=p.team_id ORDER BY p.full_name""")
        show_table(records.drop(columns=["team_id"]))
        teams_list = df("SELECT team_id,team_name FROM teams ORDER BY team_name")
        team_options = {None: "Unassigned"}
        team_options.update({int(r.team_id): str(r.team_name) for r in teams_list.itertuples()})
        action = st.selectbox("Action", ["Create", "Update", "Delete"], key="player_action")
        if action == "Create":
            with st.form("create_player_form", clear_on_submit=True):
                name = st.text_input("Player full name", max_chars=120)
                team_id = st.selectbox("Team", list(team_options), format_func=lambda i: team_options[i])
                role = st.selectbox("Role", ["Batter", "Bowler", "All-rounder", "Wicketkeeper", "Wicketkeeper-batter"])
                country = st.text_input("Country", max_chars=100)
                submitted = st.form_submit_button("CREATE PLAYER")
            if submitted:
                try:
                    create_player(name, team_id, role, country)
                    st.success("Player created.")
                    st.rerun()
                except (ValueError, sqlite3.IntegrityError) as exc:
                    st.error(str(exc))
        elif not records.empty:
            options = dict(zip(records.player_id.astype(int), records.full_name))
            selected_id = st.selectbox("Choose player", list(options), format_func=lambda i: options[i], key="player_selected")
            current = records[records.player_id == selected_id].iloc[0]
            if action == "Update":
                with st.form("update_player_form"):
                    name = st.text_input("Player full name", value=str(current.full_name), max_chars=120)
                    current_team = None if pd.isna(current.team_id) else int(current.team_id)
                    team_id = st.selectbox("Team", list(team_options), index=list(team_options).index(current_team), format_func=lambda i: team_options[i])
                    roles = ["Batter", "Bowler", "All-rounder", "Wicketkeeper", "Wicketkeeper-batter"]
                    if current.role not in roles:
                        roles.insert(0, str(current.role))
                    role = st.selectbox("Role", roles, index=roles.index(current.role))
                    country = st.text_input("Country", value=str(current.country), max_chars=100)
                    submitted = st.form_submit_button("SAVE CHANGES")
                if submitted:
                    try:
                        update_player(selected_id, name, team_id, role, country)
                        st.success("Player updated.")
                        st.rerun()
                    except (ValueError, sqlite3.IntegrityError) as exc:
                        st.error(str(exc))
            else:
                st.warning("Players referenced in batting or bowling statistics cannot be deleted.")
                confirmed = st.checkbox("I understand this permanently deletes the selected player", key="confirm_player")
                if st.button("DELETE PLAYER", disabled=not confirmed):
                    try:
                        delete_player(selected_id)
                        st.success("Player deleted.")
                        st.rerun()
                    except (ValueError, sqlite3.IntegrityError) as exc:
                        st.error(str(exc))
        else:
            st.info("Create a player first.")

st.divider()
st.caption("CRICBUZZ LIVESTATS · CINEMATIC CRICKET INTELLIGENCE · SQLITE + STREAMLIT + PLOTLY · SYNTHETIC DEMO DATA · NOT LIVE")


# LIVE_CRICKET_INTEGRATION_V1: API-powered section, independent of SQLite demo data
st.divider()
with st.expander("🔴 LIVE CRICKET SCORES · CricketData API", expanded=False):
    st.caption("Provider-supplied current matches. Separate from synthetic SQLite demo records. Scores may be delayed.")
    if st.button("🔄 Refresh live cricket scores", key="refresh_live_cricket"):
        st.session_state.pop("live_cricket_matches", None)
    if "live_cricket_matches" not in st.session_state:
        try:
            with st.spinner("Fetching current cricket matches..."):
                st.session_state["live_cricket_matches"] = get_current_matches()
            st.session_state.pop("live_cricket_error", None)
        except CricketAPIError as exc:
            st.session_state["live_cricket_error"] = str(exc)
    if st.session_state.get("live_cricket_error"):
        st.warning(st.session_state["live_cricket_error"])
    elif "live_cricket_matches" in st.session_state:
        live_matches = st.session_state["live_cricket_matches"]
        st.caption(f"{len(live_matches)} matches returned by the provider")
        if not live_matches:
            st.info("The provider returned no current matches.")
        for match in live_matches[:20]:
            if not isinstance(match, dict):
                continue
            with st.container(border=True):
                st.subheader(str(match.get("name") or "Cricket match"))
                st.caption(f"{match.get('matchType', 'Format unknown')} · {match.get('venue', 'Venue unknown')}")
                st.write(str(match.get("status") or "Status unavailable"))
                st.markdown("**" + format_scores(match) + "**")
