package com.AGVN;


import java.io.File;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.HashMap;

import com.google.gson.JsonObject;

import javax.servlet.http.HttpServletRequest;

import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestMethod;
import org.springframework.web.bind.annotation.ResponseBody;
import org.springframework.web.multipart.MultipartFile;
import org.springframework.web.multipart.MultipartHttpServletRequest;


@Controller
public class WebController {
	
	@RequestMapping("/")
	public String jspPage(Model model) {
		model.addAttribute("explain", "Explain Template");
		return "index";
	}
	
	// File Upload Ajax
	@RequestMapping(value="/fileupload.do", method = RequestMethod.POST,produces="application/json")
	@ResponseBody
	public String upload(HttpServletRequest request) throws IOException {
		MultipartHttpServletRequest multipartRequest = (MultipartHttpServletRequest) request;
		
		// max file size = 30MB
		JsonObject obj = null;
		
		MultipartFile file = multipartRequest.getFile("fileInput");
		obj = new JsonObject();
		
		// Default Construct File
		String UPLOAD_DIR = "data/upload/";
		File   dir        = new File(UPLOAD_DIR);
		
		if(!dir.exists()) {
			dir.mkdirs();
		}
		
		Path path = Paths.get(UPLOAD_DIR,file.getOriginalFilename());
		
		try {
			
			// default upload
			Files.write(path, file.getBytes());
			
			obj.addProperty("result", "success");
			obj.addProperty("path", path.toString());
			
		} catch(Exception e) {
			e.printStackTrace();
			obj.addProperty("result", "fail");
			return obj.toString();
		}
		
		return obj.toString();
		
	}
	
	@RequestMapping(value="/conveySocket.do", method = RequestMethod.POST, produces="application/json")
	@ResponseBody
	public String conveySocket(@RequestBody HashMap<String, Object> map) {
		
		JsonObject obj = null;
		
//		System.out.println(request);
		
		boolean isUse = (Boolean) map.get("isUse");
		String  path  = (String)  map.get("path");
		String  type  = (String)  map.get("type");
		String  model = (String)  map.get("model");
		
		SocketClient socket = new SocketClient("localhost",9898);
		obj = socket.run(type, isUse, path, model);
		
		/*
		obj = new JsonObject();
		obj.addProperty("type",  type);
		obj.addProperty("path",  path);
		obj.addProperty("isUse", isUse);
		*/
		
		
		System.out.println(obj.toString());
		
		return obj.toString();
		
	}
	
	
	
	
}

