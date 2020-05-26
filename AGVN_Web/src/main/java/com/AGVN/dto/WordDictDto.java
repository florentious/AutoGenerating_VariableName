package com.AGVN.dto;


import lombok.AllArgsConstructor;
import lombok.Getter;
import lombok.Setter;


@AllArgsConstructor
@Getter
@Setter
public class WordDictDto {
	private int word_id;
	private int proj_id;
	private String word_kor;
	private String word_eng;
	private String word_abr;
	private String word_def;

}
