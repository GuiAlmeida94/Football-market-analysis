-- Creating the events base view to support tactical analysis
DROP VIEW IF EXISTS vw_game_events_base CASCADE;

CREATE OR REPLACE VIEW vw_game_events_base AS
SELECT 
    game_event_id,
    game_id,
    player_id,
    player_in_id, -- Key for substitution analysis
    player_assist_id,
    date AS event_date,
    -- Standardizing season_year for our Master View joins
    EXTRACT(YEAR FROM date)::INT AS season_year,
    minute,
    type, -- 'subst', 'goals', 'cards', etc.
    description
FROM game_events
WHERE date >= '2010-01-01' 
  AND date <= '2025-12-31';