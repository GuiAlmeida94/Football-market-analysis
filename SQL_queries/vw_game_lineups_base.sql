-- 1. Removing the view to allow table alterations
DROP VIEW IF EXISTS vw_game_lineups_base CASCADE;

-- 2. Creating the tactical lineups base view with the Anchor Column
CREATE OR REPLACE VIEW vw_game_lineups_base AS
SELECT 
    game_lineups_id,
    game_id,
    player_id,
    club_id,
    player_name,
    date AS lineup_date, 
    -- ADDING: The season_year anchor for Master View joins
    EXTRACT(YEAR FROM date)::INT AS season_year,
    type AS lineup_type, 
    position AS tactical_position,
    number AS shirt_number,
    team_captain::BOOLEAN AS is_captain -- Ensuring boolean type
FROM game_lineups
WHERE date >= '2010-01-01' 
  AND date <= '2025-12-31';