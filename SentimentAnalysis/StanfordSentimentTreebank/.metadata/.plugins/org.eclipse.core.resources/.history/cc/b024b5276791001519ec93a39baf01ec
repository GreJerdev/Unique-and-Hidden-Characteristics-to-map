
package Default;

import java.io.*;
import java.net.*;
import java.nio.ByteBuffer;
import java.nio.CharBuffer;


public class Main {
	
	protected static StanfordCoreNLPSentiment m_StanfordCoreNLPSentiment;
	static String clientSentence;  
	static String capitalizedSentence;
	static ServerSocket welcomeSocket = null;
	public static void main(String[] args) throws IOException {
		
		m_StanfordCoreNLPSentiment = new StanfordCoreNLPSentiment();
		welcomeSocket = new ServerSocket(6789);
		
    	while(true) { 
    		try
    		{
    			ByteBuffer bf = ByteBuffer.allocate(300000);
	    		Socket connectionSocket = welcomeSocket.accept(); 
	        	//BufferedReader inFromClient = new BufferedReader(new InputStreamReader(connectionSocket.getInputStream()));
	    		//InputStreamReader inFromClient = new InputStreamReader(connectionSocket.getInputStream());
	    		
	    		DataInputStream is = new DataInputStream(connectionSocket.getInputStream());
	    		
	    		DataOutputStream outToClient = new DataOutputStream(connectionSocket.getOutputStream()); 
	        	//System.out.println("Before Receiving data");  
	        	Boolean haveMessage = true;
	        	String receivedData = "";
	        	while (haveMessage)
	        	{
	        		int ch = is.read();
	        	//	System.out.println("Received: " + String.valueOf((char)ch)); 
	        		receivedData += String.valueOf((char)ch);
	        		String[]messages = receivedData.split("!@@!");
	        		if ( receivedData.endsWith("!@@!") )
	        		{
	        			receivedData = "";
	        			clientSentence = messages[0];
	        			haveMessage = false;
	        		}
	        	}
	            
	        	
	        	//clientSentence = inFromClient.readLine();  
	        	System.out.println("Received: " + clientSentence);  
		    	String message = m_StanfordCoreNLPSentiment.ProccessData(clientSentence);
		    	String messageSize = Integer.toString(message.length()); 
		    	outToClient.writeBytes(messageSize+"|"+message);
		    	outToClient.flush();
    		}
    		catch(Exception ex)
    		{
    			System.out.println("******************Exception: " + ex.getMessage());  
    		}
		}
	
	 		
	}
	
	

}
