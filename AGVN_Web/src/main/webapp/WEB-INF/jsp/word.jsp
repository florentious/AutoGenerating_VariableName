<%@ page language="java" contentType="text/html; charset=utf-8"
	pageEncoding="utf-8"%>
<!-- jstl -->
<%@ taglib uri="http://java.sun.com/jsp/jstl/core" prefix="c"%>

<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">
<html>
<head>
<!-- Required meta tags -->
<meta charset="utf-8">
<meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
<meta name="viewport"
	content="width=device-width, initial-scale=1, shrink-to-fit=no">

<!-- Bootstrap CSS -->
<link rel="stylesheet"
	href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.0/css/bootstrap.min.css"
	integrity="sha384-9aIt2nRpC12Uk9gS9baDl411NQApFmC26EwAOH8WgZl5MYYxFfc+NcPb1dKGj7Sk"
	crossorigin="anonymous">

<link rel="icon" href="img/ai.ico" type="image/x-icon">

<title>AutoGenerating VariableName</title>

<style>
</style>

</head>
<body>
	<!-- navbar start -->
	<nav class="navbar navbar-expand-lg navbar-light bg-light"> <a
		class="navbar-brand" href="/">AutoGenerating VariableName</a>
	<button class="navbar-toggler" type="button" data-toggle="collapse"
		data-target="#navbarNav" aria-controls="navbarNav"
		aria-expanded="false" aria-label="Toggle navigation">
		<span class="navbar-toggler-icon"></span>
	</button>
	<div class="collapse navbar-collapse" id="navbarNav">
		<ul class="navbar-nav">
			<li class="nav-item"><a class="nav-link" href="/">Home</a></li>
			<li class="nav-item active"><a class="nav-link" href="/word">WordDictionary<span
					class="sr-only">(current)</span></a></li>
		</ul>
	</div>
	</nav>
	<!-- navbar end -->

	<!-- Header end -->

	<!-- main start -->
	<div class="col-sm-12">
		
		<div class="col-sm-12 row">
		
		
		<div class="col-sm-2">
		
		</div>
	
		<div class="col-sm-8">
			<table class="table table-hover">
				<colgroup>
					<col width="5%" />
					<col width="10%"/>
					<col width="15%"/>
					<col width="15%"/>
					<col width="55%"/>
				</colgroup>
				<thead>
					<tr>
						<th scope="col">Id</th>
						<th scope="col">Abr</th>
						<th scope="col">Kor</th>
						<th scope="col">Eng</th>
						<th scope="col">Def</th>
						
					</tr>
				</thead>
				<tbody>
					
					<c:forEach var="dictList" items="${wordDictList }">
						<tr>
							<th scope="row">${dictList.word_id }</th>
							<td>${dictList.word_abr }</td>
							<td>${dictList.word_kor }</td>
							<td>${dictList.word_eng }</td>
							<td>${dictList.word_def }</td>
						</tr>
					</c:forEach>
				</tbody>
			</table>
		
		</div>
		</div>

	</div>




	<!-- main end -->



	<!-- footer -->

	<!-- Bootstrap JS -->
	<script src="https://code.jquery.com/jquery-3.5.1.slim.min.js"
		integrity="sha384-DfXdz2htPH0lsSSs5nCTpuj/zy4C+OGpamoFVy38MVBnE+IbbVYUew+OrCXaRkfj"
		crossorigin="anonymous"></script>
	<script
		src="https://cdn.jsdelivr.net/npm/popper.js@1.16.0/dist/umd/popper.min.js"
		integrity="sha384-Q6E9RHvbIyZFJoft+2mJbHaEWldlvI9IOYy5n3zV9zzTtmI3UksdQRVvoxMfooAo"
		crossorigin="anonymous"></script>
	<script
		src="https://stackpath.bootstrapcdn.com/bootstrap/4.5.0/js/bootstrap.min.js"
		integrity="sha384-OgVRvuATP1z7JjHLkuOU7Xw704+h835Lr+6QL9UvYjZE3Ipu6Tp75j7Bh/kR0JKI"
		crossorigin="anonymous"></script>

	<!-- jquery.js // Need to use Ajax -->
	<script src="/js/jquery-3.5.1.js"></script>
	<!-- index.jsp -> script code -->
	<script src="/js/personal.js"></script>
</body>
</html>
