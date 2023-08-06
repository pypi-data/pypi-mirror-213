DROP VIEW IF EXISTS {tracking_history_view};
CREATE VIEW {tracking_history_view} AS
SELECT
	h.id
	,h.entity_type_id
	,t.app_label||'.'||t.model_name AS entity_type
	,h.entity_id
	,h."data" 
	,h.data_saved
	,h.created 
	,o.user_id AS origin_user_id
	,u.username AS origin_user_name
    ,o.address AS origin_address
    ,o.endpoint AS origin_endpoint
    ,o.auth AS origin_auth
    ,o.details AS origin_details
FROM {tracking_history} h
INNER JOIN {tracking_entitytype} t ON t.id = h.entity_type_id
LEFT OUTER JOIN {tracking_origin} o ON o.id = h.origin_id 
LEFT OUTER JOIN {user} u ON u.id = o.user_id
