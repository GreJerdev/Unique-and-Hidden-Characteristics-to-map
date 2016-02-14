CREATE DEFINER=`root`@`localhost` PROCEDURE `csp_get_features_by_items_id`(list_of_items_ids varchar(250) )
BEGIN

select feature,feature_rest_db.id as 'id',count(1) as 'count'
from sentences_rest_db inner join feature_to_sentences_rest_db
on sentences_id = sentences_rest_db.id
inner join feature_rest_db on
feature_id = feature_rest_db.id
where FIND_IN_SET(sentences_rest_db.restaurant_id, list_of_items_ids)
group by feature,feature_rest_db.id
order by count(1) ;

END