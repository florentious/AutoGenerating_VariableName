package com.AGVN.dao;
/*
import org.springframework.data.jpa.repository.JpaRepository;

import com.AGVN.dto.WordDictDto;

public interface WordDictDao extends JpaRepository <WordDictDto, Integer>{

}
*/

import java.util.List;

import com.AGVN.dto.WordDictDto;

public interface WordDictDao {
	List<WordDictDto> selectWordDict( ) throws Exception; 
	boolean addWordDict(WordDictDto wordDictDto) throws Exception;
	boolean updateWordDict(WordDictDto wordDictDto) throws Exception;
	boolean deleteWordDict(int word_id) throws Exception;
	
	
	
}