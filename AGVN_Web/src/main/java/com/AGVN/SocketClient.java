package com.AGVN;
import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.OutputStreamWriter;
import java.io.PrintWriter;
import java.io.StringWriter;
import java.net.Socket;
import java.net.UnknownHostException;

import org.json.simple.JSONObject;
import org.json.simple.JSONValue;
import org.json.simple.parser.JSONParser;
import org.json.simple.parser.ParseException;



public class SocketClient {
	private String ip;
	private int port;
	
	public SocketClient(String ip, int port) {
		super();
		this.ip = ip;
		this.port = port;
	}
	
	public void run() {
		Socket socket = null;
		
		PrintWriter pw = null;
		BufferedWriter bw = null;
		BufferedReader br = null;
		
		JSONObject jo = null;
		JSONParser parser = null;
		Object obj = null;
		JSONObject outJo = null;
		
		try {
			socket = new Socket(ip, port);
			
			// �깉濡쒖슫 JSONObject �깮�꽦�빐�꽌 �꽔�뼱�꽌 蹂대궡�뒗 �옉�뾽
			jo = new JSONObject();
			jo.put("input_path", "input/test.xlsx");
			jo.put("isUseInputDict", "False");
			jo.put("inputDict", "");
			jo.put("isUseDefautDict", "True");
			
//			StringWriter sw = new StringWriter();
			
//			pw = new PrintWriter(new OutputStreamWriter(socket.getOutputStream()));
			bw = new BufferedWriter(new OutputStreamWriter(socket.getOutputStream()));
			
			String str2json = JSONValue.toJSONString(jo.toString());
			
//			pw.println(str2json);
//			pw.flush();
			
			bw.write(str2json.toCharArray());
			bw.write("\n");
			bw.flush();
			
			
			br = new BufferedReader(new InputStreamReader(socket.getInputStream()));
			String content = br.readLine();
			System.out.println(content);
			
			parser = new JSONParser();
			obj = parser.parse(content);
			outJo = (JSONObject) obj;
			
			System.out.println(outJo.get("status"));
			System.out.println(outJo.get("output_path"));
			System.out.println(outJo.get("newDict_path"));
			
			
		} catch (UnknownHostException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		} catch (ParseException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		} finally {
			try {
				if(socket != null) socket.close();
			} catch (IOException e) {
				// TODO Auto-generated catch block
				e.printStackTrace();
			}
		}
		
	}
}
