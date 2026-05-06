-- 1. Removing the view to include the new columns and filters
DROP VIEW IF EXISTS vw_players_base CASCADE;

-- 2. Creating the optimized player view with your original structure + Age Filter + Season Year
CREATE OR REPLACE VIEW vw_players_base AS
SELECT DISTINCT ON (p.player_id, EXTRACT(YEAR FROM pv.date))
    p.player_id,
    p.name AS player_name,
    p.current_club_id,
    p.last_season,
    p.country_of_citizenship,
    p.date_of_birth,
    -- Age at the end of 2025
    EXTRACT(YEAR FROM AGE('2025-12-31'::DATE, p.date_of_birth))::INT AS player_age,
    -- Age specifically at the moment of market value measurement
    EXTRACT(YEAR FROM AGE(pv.date, p.date_of_birth))::INT AS age_at_valuation,
    p.position,
    COALESCE(p.sub_position, 'Unknown') AS sub_position,
    COALESCE(p.foot, 'right') AS foot,
    COALESCE(p.height_in_cm, 180) AS height_in_cm,
    pv.market_value_in_eur AS market_value,
    p.highest_market_value_in_eur,
    pv.date AS snapshot_date,
    -- NEW: The anchor column for the Master View
    EXTRACT(YEAR FROM pv.date)::INT AS season_year
FROM players p
JOIN player_valuations pv ON p.player_id = pv.player_id
WHERE p.last_season >= 2010
  AND pv.date >= '2010-01-01'
  AND pv.date <= '2025-12-31'
  -- 3. Filter: Professionals Only (18+)
  AND EXTRACT(YEAR FROM AGE(pv.date, p.date_of_birth)) >= 18
ORDER BY 
    p.player_id, 
    EXTRACT(YEAR FROM pv.date) DESC, 
    pv.date DESC;