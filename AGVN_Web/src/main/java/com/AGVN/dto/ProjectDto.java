package com.AGVN.dto;

import javax.persistence.Column;
import javax.persistence.Entity;
import javax.persistence.GeneratedValue;
import javax.persistence.Id;
import javax.persistence.Table;

import lombok.AllArgsConstructor;
import lombok.Getter;
import lombok.Setter;


@Table(name="PROJECT")
@Entity
@AllArgsConstructor
@Getter
@Setter
public class ProjectDto {
	@GeneratedValue
	@Id
	@Column(name="PROJ_ID")
	private int id;
	@Column(name="PROJ_NM")	
	private String nm;
	@Column(name="PROJ_MNG")
	private String mng;

}
