create or replace function slugify(input text)
returns text as $$
    with "unaccented" as (
		select unaccent(input) as value
    ),
    "clarified" as (
		select regexp_replace(lower(value), '[^\w\s-]', '', 'g') as value
	      from "unaccented"
    ),
    "hyphenated" as (
		select trim(both '-_' from regexp_replace(value, '[-\s]+', '-', 'g')) as value
		from "clarified"
    )
    select coalesce(value, 'none') from "hyphenated";
$$ language sql immutable;
