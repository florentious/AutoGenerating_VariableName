package com.AGVN.dao;

import java.util.List;

import com.AGVN.dto.ProjectDto;

public interface ProjectDao {
	List<ProjectDto> selectProject(ProjectDto param) throws Exception;

}
