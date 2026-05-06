-- 1. Drop existing view due to table dependencies
DROP VIEW IF EXISTS vw_clubs_base CASCADE;

-- 2. Re-creating the temporal club view 
CREATE OR REPLACE VIEW vw_clubs_base AS
WITH daily_club_sums AS (
    -- Grouping market value by month snapshots (Feb and Sep)
    SELECT 
        current_club_id,
        date::DATE AS valuation_date,
        SUM(market_value_in_eur) AS total_market_value
    FROM player_valuations
    WHERE EXTRACT(MONTH FROM date::DATE) IN (2, 9)
    GROUP BY current_club_id, date::DATE
)
SELECT DISTINCT ON (ds.current_club_id, EXTRACT(YEAR FROM ds.valuation_date), EXTRACT(MONTH FROM ds.valuation_date))
    c.club_id,
    c.name AS club_name,
    c.domestic_competition_id AS competition_id,
    ds.valuation_date AS snapshot_date,
    ds.total_market_value,
    c.squad_size,
    c.stadium_seats,
    c.last_season
FROM clubs c
JOIN daily_club_sums ds ON c.club_id = ds.current_club_id
WHERE c.last_season >= 2010
ORDER BY 
    ds.current_club_id, 
    EXTRACT(YEAR FROM ds.valuation_date), 
    EXTRACT(MONTH FROM ds.valuation_date), 
    ds.valuation_date DESC;