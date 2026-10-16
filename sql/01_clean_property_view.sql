-- Cleaning view for Zameen property data
-- Raw table is never changed. All cleaning happens in this view.

create schema if not exists clean;

drop view if exists clean.property;

create view clean.property as
select
    property_id,
    property_type,
    -- Price: sale below 5 lakh or rent below 1000 is treated as bad data
    case
        when purpose = 'For Sale' and price < 500000 then null
        when purpose = 'For Rent' and price < 1000 then null
        else price
    end as price,
    city,
    province_name,
    purpose,
    -- Area: convert Kanal to Marla (1 Kanal = 20 Marla), keep 1 to 2000 Marla only
    case
        when t.area_calc < 1 or t.area_calc > 2000 then null
        else t.area_calc
    end as area_marla,
    -- Bedrooms: 0 is missing data, except for Flat and Room (studios are real)
    case
        when bedrooms = 0 and baths = 0 then null
        when bedrooms = 0 and property_type not in ('Flat', 'Room') then null
        else bedrooms
    end as bedrooms,
    case when bedrooms = 0 and baths = 0 then null else baths end as baths
from (
    select
        *,
        case
            when split_part(area, ' ', 2) = 'Kanal'
                then replace(split_part(area, ' ', 1), ',', '')::numeric * 20
            else replace(split_part(area, ' ', 1), ',', '')::numeric
        end as area_calc
    from raw.property
) t;