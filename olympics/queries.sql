SELECT * FROM noc_regions 
ORDER BY noc_regions.NOC;

SELECT DISTINCT olympian_athletes.id, olympian_athletes.name FROM olympian_athletes, per_olympic_athlete_data
WHERE per_olympic_athlete_data.noc = '107'
AND per_olympic_athlete_data.olympian_id = olympian_athletes.id;

SELECT olympics.year, olympic_events.event, olympic_event_results.medal FROM olympic_event_results, olympics, olympic_events
WHERE olympic_event_results.olympian_id = '71665' 
AND olympic_event_results.medal = 'Gold' 
AND olympic_event_results.olympic_id = olympics.id 
AND olympic_event_results.olympic_event_id = olympic_events.id 
ORDER BY olympics.year ASC;

SELECT noc_regions.noc, COUNT(olympic_event_results.medal) FROM olympic_event_results, noc_regions, per_olympic_athlete_data 
WHERE olympic_event_results.medal = 'Gold'
AND olympic_event_results.olympian_id = per_olympic_athlete_data.olympian_id
AND CAST(per_olympic_athlete_data.noc AS integer) = noc_regions.id
GROUP BY noc_regions.noc
ORDER BY COUNT(olympic_event_results.medal) DESC;