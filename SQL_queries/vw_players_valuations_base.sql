-- 1. Removing dependent views to allow alterations
DROP VIEW IF EXISTS vw_players_base CASCADE;
DROP VIEW IF EXISTS vw_clubs_base CASCADE;

-- 2. Creating a base view for raw valuations
CREATE OR REPLACE VIEW vw_player_valuations_base AS
SELECT 
    player_id,
    date AS valuation_date,
    market_value_in_eur,
    current_club_id
FROM player_valuations
WHERE date >= '2010-01-01' 
  AND date <= '2025-12-31';