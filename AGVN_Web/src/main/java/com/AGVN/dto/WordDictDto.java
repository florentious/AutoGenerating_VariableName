package com.AGVN.dto;

import lombok.AllArgsConstructor;
import lombok.Getter;
import lombok.Setter;


@AllArgsConstructor
@Getter
@Setter
public class WordDictDto {
	private int id;
	private int proj_id;
	private String kor;
	private String eng;
	private String abr;
	private String def;

}
