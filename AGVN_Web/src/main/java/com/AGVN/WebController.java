package com.AGVN;


import java.io.File;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;

import javax.servlet.http.HttpServletRequest;

import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestMethod;
import org.springframework.web.bind.annotation.ResponseBody;
import org.springframework.web.multipart.MultipartFile;
import org.springframework.web.multipart.MultipartHttpServletRequest;
import org.springframework.web.multipart.MultipartRequest;


@Controller
public class WebController {
	@RequestMapping("/")
	@ResponseBody
	public String indexPage() {
		return "hello";
	}
	
	@RequestMapping("/index")
	public String jspPage(Model model) {
		model.addAttribute("explain", "Explain Template");
		return "index";
	}
	
	/*
	@RequestMapping(value = "/uploadFile.do", method = RequestMethod.POST)
	@ResponseBody
	public ResponseEntity<?> uploadFile(@RequestParam("uploadFile") MultipartFile uploadFile) {
		
		try {
			//FileUpload Ajax
			String filename = uploadFile.getOriginalFilename();
			String directory = "var/temp_uploads/";
			String filepath = Paths.get(directory,filename).toString();
			
			BufferedOutputStream stream = new BufferedOutputStream(new FileOutputStream(new File(filepath)));
			
			stream.write(uploadFile.getBytes());
			stream.close();			
			
		} catch(Exception e) {
			System.out.println(e.getMessage());
			return new ResponseEntity<>(HttpStatus.BAD_REQUEST);
		}
		
		return new ResponseEntity<>(HttpStatus.OK);
	}
	*/
	
	/*
	@RequestMapping(value = "/fileUpload.do", method= RequestMethod.POST, produces = "application/json")
	@ResponseBody
	public ResponseEntity<String> fileUpload(MultipartFile file) {
		
		
		try {
			String UPLOAD_DIR = "opt/uploads/";
			
			Path path = Paths.get(UPLOAD_DIR,file.getOriginalFilename());
			
			Files.write(path, file.getBytes());
		} catch (Exception e) {
			e.printStackTrace();
			return new ResponseEntity<>("Invalid file format!!", HttpStatus.BAD_REQUEST);
		}
		
		return new ResponseEntity<>("File uploaded!!", HttpStatus.OK);
	}
	*/
	
	
	@RequestMapping(value="/fileupload.do", method = RequestMethod.POST,produces="application/json")
	@ResponseBody
	public String upload(HttpServletRequest request) throws IOException {
		MultipartHttpServletRequest multipartRequest = (MultipartHttpServletRequest) request;
		
		MultipartFile file = multipartRequest.getFile("fileInput");
		
		boolean       isSuccess = false;
		
		
		
		// Default Construct File
		String UPLOAD_DIR = "opt/uploads/";
		File   dir        = new File(UPLOAD_DIR);
		
		if(!dir.exists()) {
			dir.mkdirs();
		}
		
		String fileName = file.getOriginalFilename();
		
//		Path path = Paths.get(UPLOAD_DIR,file.getOriginalFilename());
//		Files.write(path, file.getBytes());
		
		
		return "tmp_return";
		
	}
	
	
	
}

