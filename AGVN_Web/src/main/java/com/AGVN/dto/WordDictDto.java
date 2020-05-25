package com.AGVN.dto;

import javax.persistence.Column;
import javax.persistence.Entity;
import javax.persistence.GeneratedValue;
import javax.persistence.Id;
import javax.persistence.Table;

import lombok.AllArgsConstructor;
import lombok.Getter;
import lombok.Setter;


@Table(name="WORDDICT")
@Entity
@AllArgsConstructor
@Getter
@Setter
public class WordDictDto {
	@GeneratedValue
	@Id
	@Column(name="WORD_ID")
	private int id;
	@Column(name="PROJ_ID")
	private int proj_id;
	@Column(name="WORD_KOR")
	private String kor;
	@Column(name="WORD_ENG")
	private String eng;
	@Column(name="WORD_ABR")
	private String abr;
	@Column(name="WORD_DEF")
	private String def;

}
