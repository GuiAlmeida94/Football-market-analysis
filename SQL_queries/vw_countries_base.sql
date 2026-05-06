-- 1. Removendo a view anterior
DROP VIEW IF EXISTS vw_countries_base CASCADE;

-- 2. Criando a base de países com as colunas REAIS e o mapeamento de continente
CREATE OR REPLACE VIEW vw_countries_base AS
SELECT 
    country_id,
    country_name, -- Corrigido conforme o print
    country_code AS country_code,
    -- Criando a coluna continente via lógica de mapeamento (Bruce's Data Engineering)
    CASE 
        WHEN country_name IN ('England', 'Germany', 'Spain', 'Italy', 'France', 'Portugal', 'Netherlands', 'Belgium', 'Scotland', 'Austria', 'Turkey', 'Greece', 'Denmark', 'Russia', 'Ukraine') THEN 'Europe'
        WHEN country_name IN ('Brazil', 'Argentina', 'Uruguay', 'Colombia', 'Chile', 'Ecuador', 'Paraguay', 'Peru') THEN 'South America'
        WHEN country_name IN ('United States', 'Mexico', 'Canada') THEN 'North America'
        WHEN country_name IN ('Japan', 'South Korea', 'China', 'Saudi Arabia', 'United Arab Emirates', 'Qatar') THEN 'Asia'
        WHEN country_name IN ('Egypt', 'Morocco', 'Algeria', 'Senegal', 'Nigeria', 'South Africa', 'Ghana', 'Ivory Coast') THEN 'Africa'
        WHEN country_name IN ('Australia', 'New Zealand') THEN 'Oceania'
        ELSE 'Other/Unknown' 
    END AS continent,
    url
FROM countries;