-- Rental yield by city (houses only)
-- Yield = (monthly rent per Marla * 12) / sale price per Marla
-- Medians are used instead of averages so a few extreme listings do not distort the result.
-- Note: prices are asking prices, and yield ignores maintenance, tax and vacancy.

with sale as (
    select
        city,
        percentile_cont(0.5) within group (order by price / area_marla) as sale_per_marla
    from clean.property
    where purpose = 'For Sale'
      and property_type = 'House'
      and price is not null
      and area_marla is not null
    group by city
    having count(*) >= 500
),
rent as (
    select
        city,
        percentile_cont(0.5) within group (order by price / area_marla) as rent_per_marla
    from clean.property
    where purpose = 'For Rent'
      and property_type = 'House'
      and price is not null
      and area_marla is not null
    group by city
    having count(*) >= 200
)
select
    s.city,
    round(s.sale_per_marla::numeric) as sale_per_marla,
    round(r.rent_per_marla::numeric) as monthly_rent_per_marla,
    round((100 * 12 * r.rent_per_marla / s.sale_per_marla)::numeric, 2) as yearly_yield_percent
from sale s
join rent r on r.city = s.city
order by yearly_yield_percent desc;