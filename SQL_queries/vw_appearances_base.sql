-- 1. Remove VIEW if it exists
DROP VIEW IF EXISTS vw_appearances_base CASCADE;

-- 2. Recreat VIEW
CREATE OR REPLACE VIEW vw_appearances_base AS
SELECT 
    appearance_id,
    game_id,
    player_id,
    player_club_id,
    player_current_club_id,
    date, 
    player_name,
    competition_id,
    yellow_cards,
    red_cards,
    goals,
    assists,
    minutes_played
FROM appearances
WHERE date >= '2010-01-01' 
  AND date <= '2025-12-31';