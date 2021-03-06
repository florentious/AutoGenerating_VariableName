<%@ page language="java" contentType="text/html; charset=utf-8"
	pageEncoding="utf-8"%>
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
	img {
		max-width : 150%;
		height: auto !important;
	}
</style>

</head>
<body>
	<!-- navbar start -->
	<nav class="navbar navbar-expand-lg navbar-light bg-light"> 
		<a class="navbar-brand" href="/">AutoGenerating VariableName</a>
		<button class="navbar-toggler" type="button" data-toggle="collapse"
			data-target="#navbarNav" aria-controls="navbarNav"
			aria-expanded="false" aria-label="Toggle navigation">
		<span class="navbar-toggler-icon"></span>
		</button>
		<div class="collapse navbar-collapse" id="navbarNav">
			<ul class="navbar-nav">
				<li class="nav-item active">
					<a class="nav-link" href="/">Home<span class="sr-only">(current)</span></a>
				</li>
				<li class="nav-item">
					<a class="nav-link" href="/word">WordDictionary</a>
				</li>
			</ul>
		</div>
	</nav>
	<!-- navbar end -->

	<!-- Header -->

	<div class="container">

		<div class="col-sm-12">
			<br>
			<h3>Input Excel Files</h3>
			<br>
			<!-- isUse default dictionary -->
			<div class="col-sm-12 row">
				<div class="col-sm-5">
					<h5>Use Default Dictionary </h5>
				</div>
				<div class="col-sm-1">
					<h5> : </h5>
				</div>
				
				<div class="col-sm-6">
					<div class="btn-group btn-group-toggle" data-toggle="buttons">
						<label class="btn btn-secondary active"> 
							<input type="radio" name="useDefdict" id="useDefdictYes" checked>Yes
						</label> 
						<label class="btn btn-secondary"> 
							<input type="radio" name="useDefdict" id="useDefdictNo"> No
						</label>
					</div>				
				</div>
			</div>
			<br>
			<!-- how use spacing model -->
			<div class="col-sm-12 row">
				<div class="col-sm-5">
					<h5>Use Spacing Model </h5>
				</div>
				<div class="col-sm-1">
					<h5> : </h5>
				</div>
				<div class="col-sm-6">
					<div class="btn-group btn-group-toggle" data-toggle="buttons">
						<label class="btn btn-secondary active"> 
							<input type="radio" name="useModel" id="useModelKonlpy" checked>Konlpy
						</label> 
						<label class="btn btn-secondary"> 
							<input type="radio" name="useModel" id="useModelSP"> Self-Product
						</label>
					</div>
				</div>
			</div>
			<!-- blank count -->
			<br>

			<!-- File-upLoad -->
			<div class="col-sm-12 row">
				<div class="col-sm-5">				
					<h5>Input Data <br>(Press Convert Btn) </h5>
				</div>
				<div class="col-sm-1">
					<h5> : </h5>
				</div>
				<div class="col-sm-6">
					<div class="input-group mb-3">
						<div class="custom-file">
							<form method="post" enctype="multipart/form-data" id="uploadForm">
								<input type="file" class="custom-file-input" id="fileInput" name="fileInput">
								<label class="custom-file-label" for="fileInput" id="fileInputLabel">Choose file</label>
							</form> 
						</div>
						<div class="input-group-append">
							<span type="button" class="input-group-text" id="convert">Convert</span>
						</div>
					</div>
					<div id="fileInputMsg"></div>
					<input type="hidden" name="checkFile" id="checkFile" value="no" />				
				</div>
			
			</div>
			<br>
			<!-- Explain Template -->
			<!-- File-upLoad -->
			<div class="col-sm-12 row">
				<div class="col-sm-5">				
					<h5>Explain Upload Files </h5>
				</div>
				<div class="col-sm-1">
					<h5> : </h5>
				</div>
				<div class="col-sm-6">
					<img src="${explain}" style="width:1300px" >
					<br>
					<h5><a class="btn btn-secondary" href="/templateDownload.do">Template</a></h5>
				</div>
			</div>
			
		</div>

		<br>
		<br>
		<br>
		<!-- load page -->
		<div class="col-sm-12 row" id="loadBar" style="display:none">
			<div class="col-sm-3"></div>
			<div class="col-sm-3">
				<img src="${load }" style="width:200px;">
			</div>
			<div class="col-sm-6">
				<br><br>
				<h5>로딩중입니다.<br><br> 파이썬의 연산은 꽤나 깁니다.</h5>
			</div>
			
		</div>
		
		<!-- error page -->

		<div class="col-sm-12 row" id="errorDiv" style="display:none">
			<div class="col-sm-3"></div>
			<div class="col-sm-6">
				<br><br>
				<h5> 에러났습니다.<br> 컬럼이름 등을 확인해 재시도 부탁드립니다. </h5>
			</div>
			
		</div>

		<!-- output -->
		<div class="col-sm-12" id="outputDiv" style="display:none">
			<h3>Output Excel File</h3>
			<br>
			<!-- Need to ajax change disable -->
			
			<div class="col-sm-12 row">
				<div class="col-sm-5">
					<h5>Generated File Download</h5>
				</div>
				<div class="col-sm-1">
					<h5> : </h5>
				</div>
				<div class="col-sm-6">					
					<form method="post" enctype="multipart/form-data" id="downloadForm" action="fileDownload.do">
						<input type="hidden" name="outputName" id="outputName" value="" />							
						<input type="submit" class="btn btn-secondary" id="downloadFile" value="Download">
					</form>
				</div>
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


