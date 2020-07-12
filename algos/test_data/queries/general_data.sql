SELECT hour as timestamp, platform, browser, country, continent, visit_buyer_type as user_type,
       CASE WHEN country = 'US' THEN 1 ELSE 0 END as is_new_user,
       CASE WHEN platform = 'web' THEN TRUE ELSE FALSE END as used_web,
       SUM(gig_page_views) visits,
       SUM(registrations) registrations,
       SUM(orders) as purchases,
       SUM(impressions) imps
FROM `dwh.hourly_kpis`
WHERE _PARTITIONTIME >= '2020-01-01' AND _PARTITIONTIME < '2020-03-01'
  AND country = 'US'
GROUP BY 1,2,3,4,5,6,7,8
ORDER BY 1