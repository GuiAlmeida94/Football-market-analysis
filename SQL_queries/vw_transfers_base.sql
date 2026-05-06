DROP VIEW IF EXISTS vw_transfers_base CASCADE;

CREATE OR REPLACE VIEW vw_transfers_base AS
WITH latest_player_valuation AS (
    SELECT DISTINCT ON (player_id)
        player_id,
        market_value_in_eur,
        date
    FROM player_valuations
    ORDER BY player_id, date DESC
)
SELECT 
    t.player_id,
    t.player_name,
    t.transfer_date,
    -- NEW: Standardizing season_year for Master Join
    EXTRACT(YEAR FROM t.transfer_date)::INT AS season_year,
    t.transfer_season,
    t.from_club_id,
    t.to_club_id,
    t.from_club_name,
    t.to_club_name,
    t.transfer_fee,
    COALESCE(t.market_value_in_eur, lv.market_value_in_eur) AS market_value_at_transfer,
    (t.transfer_fee - COALESCE(t.market_value_in_eur, lv.market_value_in_eur)) AS fee_diff
FROM transfers t
LEFT JOIN latest_player_valuation lv ON t.player_id = lv.player_id
WHERE t.transfer_date >= '2010-01-01' 
  AND t.transfer_date <= '2025-12-31'
  AND t.player_id IS NOT NULL;