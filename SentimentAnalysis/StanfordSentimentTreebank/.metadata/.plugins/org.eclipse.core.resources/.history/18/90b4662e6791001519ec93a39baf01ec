package Default;

import java.util.List;
import java.util.Properties;

import edu.stanford.nlp.ling.CoreAnnotations;
import edu.stanford.nlp.pipeline.Annotation;
import edu.stanford.nlp.pipeline.StanfordCoreNLP;
import edu.stanford.nlp.sentiment.SentimentCoreAnnotations;
import edu.stanford.nlp.util.CoreMap;

public class StanfordCoreNLPSentiment {

	private StanfordCoreNLP m_pipeline = null;
	
	public StanfordCoreNLPSentiment(){
		Properties props = new Properties();
		props.setProperty("annotators", /*" pos, lemma, ner,dcoref,*/"tokenize, ssplit, parse,  sentiment");
		m_pipeline = new StanfordCoreNLP(props);
	}
	
	public String ProccessData(String data ){
		
		Annotation annotation = m_pipeline.process(data);
		List<CoreMap> sentences = annotation.get(CoreAnnotations.SentencesAnnotation.class);
		StringBuilder sb = new StringBuilder(10000);
		
		for (CoreMap sentence : sentences) {
			
			String sentiment = sentence.get(SentimentCoreAnnotations.SentimentClass.class);
			if(sb.length() > 0)
			{
				sb.append(",");
			}
			sb.append(String.format("{'sentence':'%s','sentiment':%s}", sentence,sentiment));
			System.out.println(sentiment + "\t" + sentence);
            //Tree sentiTree = sentence.get(SentimentCoreAnnotations.AnnotatedTree.class);
			//PrintTree(sentiTree);
	    }
		return String.format("[%s]", sb.toString());
	}
	
}
