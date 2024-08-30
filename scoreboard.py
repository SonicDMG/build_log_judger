import streamlit as st

def display_scoreboard(scoreboard):
    # Add a table-like structure for the scoreboard
    st.markdown("""
    <style>
    .leaderboard-container {
        font-family: 'Arial', sans-serif;
        margin: 20px 0;
    }
    .leaderboard-table {
        width: 100%;
        border-collapse: collapse;
        margin: 20px 0;
        font-size: 18px;
        text-align: left;
    }
    .leaderboard-table th, .leaderboard-table td {
        border: 1px solid #ddd;
        padding: 12px 15px;
    }
    .leaderboard-table th {
        background-color: #f4f4f4;
        color: #333;
        text-transform: uppercase;
    }
    .leaderboard-table td {
        background-color: #fff;
        color: #333;
    }
    .leaderboard-link {
        color: #0070f3;
        text-decoration: none;
    }
    .leaderboard-link:hover {
        text-decoration: underline;
    }
    .leaderboard-rank {
        font-weight: bold;
        color: #0070f3;
        width: 10%;
    }
    .leaderboard-file-name {
        width: 60%;
    }
    .leaderboard-score {
        width: 30%;
    }
    .leaderboard-table tr:hover {
        background-color: #f1f1f1;
    }
    </style>
    """, unsafe_allow_html=True)

    # Create the table header
    st.markdown("""
    <div class="leaderboard-container">
    <table class="leaderboard-table">
        <thead>
            <tr>
                <th class='leaderboard-rank'>Rank</th>
                <th class='leaderboard-file-name'>File Name</th>
                <th class='leaderboard-score'>Score</th>
            </tr>
        </thead>
        <tbody>
    """, unsafe_allow_html=True)

    # Populate the table with file names and scores
    for rank, (file_name, final_score) in enumerate(scoreboard, start=1):
        st.markdown(f"""
        <tr>
            <td class='leaderboard-rank'>{rank}</td>
            <td class='leaderboard-file-name'><a href='#{file_name}' class='leaderboard-link'>{file_name}</a></td>
            <td class='leaderboard-score'><strong>{final_score}</strong></td>
        </tr>
        """, unsafe_allow_html=True)

    # Close the table
    st.markdown("""
        </tbody>
    </table>
    </div>
    """, unsafe_allow_html=True)