-- 1. Removing the view to apply table alterations and column mapping
DROP VIEW IF EXISTS vw_competitions_base CASCADE;

-- 2. Creating the standardized competitions base view
CREATE OR REPLACE VIEW vw_competitions_base AS
SELECT 
    competition_id,
    competition_code,
    name AS league_name,
    type AS competition_type,
    sub_type AS competition_sub_type,
    country_name AS league_country,
    -- Mapping German terms to International/English standards (UEFA, AFC, etc.)
    CASE 
        WHEN confederation = 'europa' THEN 'UEFA'
        WHEN confederation = 'amerika' THEN 'America (CONMEBOL/CONCACAF)'
        WHEN confederation = 'asien' THEN 'AFC (Asia)'
        WHEN confederation = 'afrika' THEN 'CAF (Africa)'
        WHEN confederation = 'fifa' THEN 'FIFA'
        ELSE INITCAP(confederation) 
    END AS confederation_name,
    total_clubs
FROM competitions;