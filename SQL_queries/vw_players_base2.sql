-- Updating the player base to include season_year as a formal column
CREATE OR REPLACE VIEW vw_players_base AS
SELECT DISTINCT ON (p.player_id, EXTRACT(YEAR FROM pv.date))
    p.player_id,
    p.name AS player_name,
    p.current_club_id,
    p.last_season,
    p.country_of_citizenship,
    p.date_of_birth,
    EXTRACT(YEAR FROM AGE('2025-12-31'::DATE, p.date_of_birth))::INT AS player_age,
    EXTRACT(YEAR FROM AGE(pv.date, p.date_of_birth))::INT AS age_at_valuation,
    p.position,
    p.sub_position,
    p.foot,
    p.height_in_cm,
    pv.market_value_in_eur AS market_value,
    p.highest_market_value_in_eur,
    pv.date AS snapshot_date,
    -- NEW COLUMN: The anchor for all our seasonal joins
    EXTRACT(YEAR FROM pv.date)::INT AS season_year
FROM players p
JOIN player_valuations pv ON p.player_id = pv.player_id
WHERE p.last_season >= 2010
  AND pv.date BETWEEN '2010-01-01' AND '2025-12-31'
ORDER BY 
    p.player_id, 
    EXTRACT(YEAR FROM pv.date) DESC, 
    pv.date DESC;