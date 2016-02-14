CREATE DEFINER=`root`@`localhost` PROCEDURE `csp_get_feature_sentence_by_review_id`(in_feature_id int(6),in_review_id int(6))
BEGIN
select sentences_rest_db.* ,feature_to_sentences_rest_db.tf_idf
	from sentences_rest_db inner join feature_to_sentences_rest_db
	on sentences_rest_db.id = feature_to_sentences_rest_db.sentences_id
	where feature_to_sentences_rest_db.feature_id = in_feature_id
    and sentences_rest_db.review_id = in_review_id
	order by review_id, order_in_review;
END