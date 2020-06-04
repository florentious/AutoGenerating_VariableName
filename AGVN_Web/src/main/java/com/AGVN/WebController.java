package com.AGVN;


import java.io.File;
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.IOException;
import java.io.InputStream;
import java.io.OutputStream;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;

import com.AGVN.dao.ProjectDao;
import com.AGVN.dao.WordDictDao;
import com.AGVN.dto.ProjectDto;
import com.AGVN.dto.WordDictDto;
import com.google.gson.JsonObject;

import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

import org.mybatis.spring.annotation.MapperScan;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestMethod;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.ResponseBody;
import org.springframework.web.multipart.MultipartFile;
import org.springframework.web.multipart.MultipartHttpServletRequest;


@Controller
@MapperScan(basePackages="com.AGVN.dao")
public class WebController {
	
	@Autowired
	private WordDictDao wordDictDao;
	
	@Autowired
	private ProjectDao projectDao;
	
	// Main Page
	@RequestMapping("/")
	public String jspPage(Model model) {
		model.addAttribute("explain", "img/explain.jpg");
		model.addAttribute("load","img/load_spiner2.gif");
		return "main";
	}
	
	// ProjectIndex Page
	@RequestMapping("/project")
	public String jspProjectPage(Model model) throws Exception {
		final List<ProjectDto> projectList = projectDao.selectProject();
		model.addAttribute("projectList", projectList);
		System.out.println(projectList.get(0));
		return "project";
	}
	
	@RequestMapping("/word")
	public String jspWordDictPage(Model model) throws Exception {
		final List<WordDictDto> wordDictList = wordDictDao.selectWordDict();
		
		model.addAttribute("wordDictList", wordDictList);
		
		return "word";
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
		
		// if upload, prevent duplication
		// give system time
		String fileName = file.getOriginalFilename();
		String newFileName = fileName.substring(0,fileName.lastIndexOf("."))+"_"+Long.toString(System.currentTimeMillis())+fileName.substring(fileName.lastIndexOf("."));

		Path path = Paths.get(UPLOAD_DIR,newFileName);
		
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
	
	// send JsonObject to python
	@RequestMapping(value="/conveySocket.do", method = RequestMethod.POST, produces="application/json")
	@ResponseBody
	public String conveySocket(@RequestBody HashMap<String, Object> map) {
		
		JsonObject obj = null;
				
		boolean isUse = (Boolean) map.get("isUse");
		String  path  = (String)  map.get("path");
		String  type  = (String)  map.get("type");
		String  model = (String)  map.get("model");
		
		SocketClient socket = new SocketClient("localhost",9898);
		obj = socket.run(type, isUse, path, model);
		
//		System.out.println(obj.toString());
		
		return obj.toString();
		
	}
	
	
	// download template file
	@RequestMapping(value="/templateDownload.do")
	public void templateDownload(HttpServletRequest request, HttpServletResponse response) throws Exception {
		// use korean
		request.setCharacterEncoding("utf-8");
		
		String       fileUrl  = "data/base/";
		String       fileName = "template.xlsx"; 
		InputStream  is       = null;
		OutputStream os       = null;
		File         file     = null;
		String       client   = "";
		boolean      isHave   = false;
		
		// Read file, and stream
		try {
			file = new File(fileUrl, fileName);
			is   = new FileInputStream(file);
		} catch(FileNotFoundException fe){
			fe.printStackTrace();
			isHave = true;
		}
		
		// 접속환경(ex, IE 등등)별 처리하기 위해서 
		client = request.getHeader("User-Agent");
		
		// Download Header Setting
		response.reset();
		response.setContentType("application/octet-stream");
		response.setHeader("Content-Description", "JSP Generated Data");
		
		// Check File Found
		if(!isHave) {
			//IE
			if (client.indexOf("MSIE") != -1) {
				response.setHeader("Content-Disposition", "attachment; filename=\""
						+ java.net.URLEncoder.encode(fileName, "utf-8").replaceAll("\\+", "\\ ")+ "\"");
				
			//IE 11이상
			} else if (client.indexOf("Trident") != -1) {
                response.setHeader("Content-Disposition", "attachment; filename=\""
                        + java.net.URLEncoder.encode(fileName, "UTF-8").replaceAll("\\+", "\\ ") + "\"");
            } else {
            	// 한글파일명인 경우            	
            	response.setHeader("Content-Disposition",
                        "attachment; filename=\"" + new String(fileName.getBytes("UTF-8"), "ISO8859_1") + "\"");
                response.setHeader("Content-Type", "application/octet-stream; charset=utf-8");
            }
			// stream에 올라와있는것 다운로드 시켜줌
			response.setHeader("Content-Length", "" + file.length());
            os = response.getOutputStream();
            byte b[] = new byte[(int) file.length()];
            int leng = 0;
            while ((leng = is.read(b)) > 0) {
                os.write(b, 0, leng);
            }


		} else {
			response.setContentType("text/html;charset=UTF-8");
			System.out.println("<script langquage='javascript'>alert('파일을 찾을수 없습니다.');</script>");
			
		}
		
		is.close();
		os.close();
		
	}
	
	
	// download output file
	@RequestMapping(value="/fileDownload.do")
	public void fileDownload(HttpServletRequest request, HttpServletResponse response) throws Exception {
		// use korean
		request.setCharacterEncoding("utf-8");
		String path = request.getParameter("outputName");
		
		String       fileUrl  = path.substring(0,path.lastIndexOf('/')+1);
		String       fileName = path.substring(path.lastIndexOf('/')+1,path.length());
		InputStream  is       = null;
		OutputStream os       = null;
		File         file     = null;
		String       client   = "";
		boolean      isHave   = false;
		
		// Read file, and stream
		try {
			file = new File(fileUrl, fileName);
			is   = new FileInputStream(file);
		} catch(FileNotFoundException fe){
			fe.printStackTrace();
			isHave = true;
		}
		
		// 접속환경(ex, IE 등등)별 처리하기 위해서 
		client = request.getHeader("User-Agent");
		
		// Download Header Setting
		response.reset();
		response.setContentType("application/octet-stream");
		response.setHeader("Content-Description", "JSP Generated Data");
		
		// Made Original fileName
		String originFileName = fileName.substring(0,fileName.lastIndexOf('_'))+fileName.substring(fileName.lastIndexOf('.'));
		
		// Check File Found
		if(!isHave) {
			//IE
			if (client.indexOf("MSIE") != -1) {
				response.setHeader("Content-Disposition", "attachment; filename=\""
						+ java.net.URLEncoder.encode(originFileName, "utf-8").replaceAll("\\+", "\\ ")+ "\"");
				
				//IE 11이상
			} else if (client.indexOf("Trident") != -1) {
				response.setHeader("Content-Disposition", "attachment; filename=\""
						+ java.net.URLEncoder.encode(originFileName, "UTF-8").replaceAll("\\+", "\\ ") + "\"");
			} else {
				// 한글파일명인 경우            	
				response.setHeader("Content-Disposition",
						"attachment; filename=\"" + new String(originFileName.getBytes("UTF-8"), "ISO8859_1") + "\"");
				response.setHeader("Content-Type", "application/octet-stream; charset=utf-8");
			}
			// stream에 올라와있는것 다운로드 시켜줌
			response.setHeader("Content-Length", "" + file.length());
			os = response.getOutputStream();
			byte b[] = new byte[(int) file.length()];
			int leng = 0;
			while ((leng = is.read(b)) > 0) {
				os.write(b, 0, leng);
			}
			
			
		} else {
			response.setContentType("text/html;charset=UTF-8");
			System.out.println("<script langquage='javascript'>alert('파일을 찾을수 없습니다.');</script>");
			
		}
		
		is.close();
		os.close();
		
	}
	
	/*
	@RequestMapping("/excelRead.do")
	public void readExcel(@RequestParam("file") MultipartFile file, Model model) throws IOException {
		
		List<WordDictDto> wordList = new ArrayList<>();
		
		String extension = FilenameUtils.getExtension(file.getOriginalFilename());
		
		Workbook workBook = null;
		
		if(extension.equals("xlsx")) {
			workBook = new XSSFWorkbook(file.getInputStream());
		} else if(extension.equals("xls")) {
			workBook = new HSSFWorkbook(file.getInputStream());
		}
		
		Sheet worksheet = workBook.getSheet("단어");
		
		for (int i = 1; i < worksheet.getPhysicalNumberOfRows(); i++) {
			Row row = worksheet.getRow(i);
			
			WordDictDto dto = new WordDictDto();
			
			int idx = 0;
			dto.setWord_kor(row.getCell(idx++).getStringCellValue());
			dto.setWord_eng(row.getCell(idx++).getStringCellValue());
			dto.setWord_abr(row.getCell(idx++).getStringCellValue());
			dto.setWord_def(row.getCell(idx++).getStringCellValue());
			
			wordList.add(dto);
		}
		
		for(WordDictDto dto : wordList) {
			wordDictDao.addWordDict(dto);
		}
		
		
	}
	*/
	
	
	
	
	
}

