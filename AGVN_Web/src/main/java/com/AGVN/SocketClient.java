package com.AGVN;

import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.OutputStreamWriter;
import java.net.Socket;
import java.net.UnknownHostException;

import com.google.gson.Gson;
import com.google.gson.JsonObject;



public class SocketClient {
	private String ip;
	private int port;
	
	public SocketClient(String ip, int port) {
		super();
		this.ip = ip;
		this.port = port;
	}
	
	
	public JsonObject run(String type, boolean isUse, String path, String model) {
		Socket socket = null;
		
		BufferedWriter bw = null;
		BufferedReader br = null;
		
		JsonObject jo = null;
		JsonObject outJo = null;
		
		try {
			socket = new Socket(ip, port);
			
			
			jo = new JsonObject();
			jo.addProperty("type",  type );
			jo.addProperty("isUse", isUse);
			jo.addProperty("path",  path );
			jo.addProperty("model", model);
			
			bw = new BufferedWriter(new OutputStreamWriter(socket.getOutputStream()));
			
			String str2json = jo.toString();
			
			bw.write(str2json.toCharArray());
			bw.write("\n");
			bw.flush();
			
			
			br = new BufferedReader(new InputStreamReader(socket.getInputStream()));
			String content = br.readLine();
			
			outJo = (JsonObject) new Gson().fromJson(content,JsonObject.class);
			
			
			
		} catch (UnknownHostException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		} catch (IOException e) {
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
		
		
		return outJo;
	}
}
