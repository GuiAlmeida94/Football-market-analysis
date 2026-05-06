-- MASTER VIEW: Final Professional Version (Fixed for 2010-2026 data)
DROP VIEW IF EXISTS vw_master_data CASCADE;

CREATE OR REPLACE VIEW vw_master_data AS
WITH substitution_events AS (
    -- Using your vw_game_events_base logic
    SELECT DISTINCT game_id, player_in_id AS player_id
    FROM vw_game_events_base 
    WHERE type = 'subst' AND player_in_id IS NOT NULL
),
annual_performance AS (
    SELECT 
        a.player_id,
        EXTRACT(YEAR FROM a.date)::INT AS season_year,
        COUNT(*) AS games_played,
        SUM(a.minutes_played) AS total_minutes,
        SUM(a.goals) AS goals,
        SUM(a.assists) AS assists,
        SUM(a.yellow_cards) AS yellow_cards,
        SUM(a.red_cards) AS red_cards,
        COUNT(*) FILTER (WHERE cg.opponent_goals = 0 AND a.minutes_played > 60) AS clean_sheets,
        COUNT(*) FILTER (WHERE a.minutes_played = 90) AS full_matches_count,
        COUNT(*) FILTER (WHERE sub.player_id IS NULL) AS games_as_starter
    FROM appearances a
    JOIN club_games cg ON a.game_id = cg.game_id AND a.player_club_id = cg.club_id
    LEFT JOIN substitution_events sub ON a.game_id = sub.game_id AND a.player_id = sub.player_id
    GROUP BY 1, 2
),
annual_leadership AS (
    -- Based on your vw_game_lineups_base
    SELECT 
        player_id,
        season_year,
        COUNT(*) FILTER (WHERE is_captain IS TRUE) AS games_as_captain
    FROM vw_game_lineups_base
    GROUP BY 1, 2
)
SELECT 
    -- 1. IDENTIFICATION (Biometrics from vw_players_base)
    p.player_id,
    p.player_name,
    p.player_age,
    p.age_at_valuation,
    p.position,
    COALESCE(p.sub_position, 'Other') AS sub_position, -- Fix: Null sub-positions
    p.foot,
    p.height_in_cm,
    p.country_of_citizenship AS nationality,
    p.season_year,
    
    -- 2. IDENTITY FALLBACK (Fix: Handling the 211k nulls in clubs/leagues)
    COALESCE(c_static.name, 'Retired/Historical') AS club_name, 
    COALESCE(comp.league_name, 'Unknown/Lower League') AS league_name,
    COALESCE(comp.league_country, 'International') AS league_country,
    COALESCE(comp.confederation_name, 'Other') AS confederation,
    
    -- 3. PERFORMANCE (Fix: COALESCE 0 for all stats)
    COALESCE(perf.games_played, 0) AS games_played,
    COALESCE(perf.total_minutes, 0) AS total_minutes,
    COALESCE(perf.goals, 0) AS total_goals,
    COALESCE(perf.assists, 0) AS total_assists,
    COALESCE(perf.yellow_cards, 0) AS yellow_cards,
    COALESCE(perf.red_cards, 0) AS red_cards,
    COALESCE(perf.clean_sheets, 0) AS clean_sheets,
    COALESCE(perf.full_matches_count, 0) AS full_matches_count,
    
    -- 4. TACTICAL & LEADERSHIP
    COALESCE(perf.games_as_starter, 0) AS games_as_starter,
    -- Fix: Ratio using CASE to avoid division by zero and NULLs
    CASE WHEN COALESCE(perf.games_played, 0) > 0 
         THEN ROUND(COALESCE(perf.games_as_starter, 0)::NUMERIC / perf.games_played, 2) 
         ELSE 0 END AS starter_ratio,
    COALESCE(lead.games_as_captain, 0) AS games_as_captain,
    
    -- 5. FINANCIALS (Verified 0 nulls in previous step)
    p.market_value,
    p.highest_market_value_in_eur AS record_market_value,
    COALESCE(t.transfer_fee, 0) AS last_transfer_fee,
    (p.market_value - COALESCE(t.transfer_fee, 0)) AS transfer_roi_gap,
    COALESCE(t.fee_diff, 0) AS investment_premium,
    
    -- 6. SMART RATIOS (Fix: Handling efficiency nulls)
    CASE WHEN COALESCE(perf.goals, 0) > 0 
         THEN ROUND(perf.total_minutes::NUMERIC / perf.goals, 2) 
         ELSE 0 END AS minutes_per_goal,
         
    CASE WHEN (COALESCE(perf.yellow_cards, 0) + COALESCE(perf.red_cards, 0)) > 0 
         THEN ROUND(perf.total_minutes::NUMERIC / (perf.yellow_cards + (perf.red_cards * 2)), 2) 
         ELSE 0 END AS discipline_ratio

FROM vw_players_base p
LEFT JOIN annual_performance perf ON p.player_id = perf.player_id AND p.season_year = perf.season_year
LEFT JOIN annual_leadership lead ON p.player_id = lead.player_id AND p.season_year = lead.season_year
LEFT JOIN clubs c_static ON p.current_club_id = c_static.club_id
LEFT JOIN vw_competitions_base comp ON c_static.domestic_competition_id = comp.competition_id
LEFT JOIN vw_transfers_base t ON p.player_id = t.player_id AND p.season_year = t.season_year
WHERE p.season_year >= 2010;