-- 1. Creating a simple base view for national teams
CREATE OR REPLACE VIEW vw_national_teams_base AS
SELECT 
    national_team_id,
    name AS country_name,
    team_code,
    confederation,
    fifa_ranking,
    total_market_value AS national_squad_value,
    last_season
FROM national_teams
WHERE last_season >= 2010;