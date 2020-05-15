package com.AGVN;

import java.io.BufferedOutputStream;
import java.io.File;
import java.io.FileOutputStream;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.ArrayList;
import java.util.List;
import java.util.Map;

import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestMethod;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.ResponseBody;
import org.springframework.web.multipart.MultipartFile;
import org.springframework.web.multipart.MultipartHttpServletRequest;

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
	

	@PostMapping("/fileUpload.do")
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
	
	
	
	
}

