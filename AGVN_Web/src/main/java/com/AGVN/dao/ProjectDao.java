package com.AGVN.dao;


import java.util.List;


import com.AGVN.dto.ProjectDto;

/*
import org.springframework.data.jpa.repository.JpaRepository;

public interface ProjectDao extends JpaRepository <ProjectDto, Integer>{

}

*/

public interface ProjectDao {
	List<ProjectDto> selectProject( ) throws Exception; 
	boolean addProject(ProjectDto projectDto) throws Exception;
	boolean updateProject(ProjectDto projectDto) throws Exception;
	boolean deleteProject(int proj_id) throws Exception;
	
	
	
}