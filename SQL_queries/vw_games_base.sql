-- 1. Removing the view to allow table alterations
DROP VIEW IF EXISTS vw_games_base CASCADE;

-- 2. Creating the games base view
CREATE OR REPLACE VIEW vw_games_base AS
SELECT 
    game_id,
    competition_id,
    season,
    round,
    date AS game_date,
    home_club_id,
    away_club_id,
    home_club_goals,
    away_club_goals,
    stadium,
    attendance,
    competition_type
FROM games
WHERE date >= '2010-01-01' 
  AND date <= '2025-12-31';