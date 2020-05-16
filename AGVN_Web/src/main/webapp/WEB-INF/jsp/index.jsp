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

<title>AutoGenerating VariableName</title>
</head>
<body>
	<!-- navbar start -->
	<nav class="navbar navbar-expand-lg navbar-light bg-light"> <a
		class="navbar-brand" href="#">AutoGenerating VariableName</a>
	<button class="navbar-toggler" type="button" data-toggle="collapse"
		data-target="#navbarNav" aria-controls="navbarNav"
		aria-expanded="false" aria-label="Toggle navigation">
		<span class="navbar-toggler-icon"></span>
	</button>
	<div class="collapse navbar-collapse" id="navbarNav">
		<ul class="navbar-nav">
			<li class="nav-item active"><a class="nav-link" href="#">Home<span
					class="sr-only">(current)</span></a></li>
			<li class="nav-item"><a class="nav-link" href="#">Board</a></li>
		</ul>
	</div>
	</nav>
	<!-- navbar end -->

	<div class="container">

		<div class="col-sm-12">
			<h3>Input Excel Files</h3>
			<br>
			<!-- isUse default dictionary -->
			<div class="col-sm-12 row">
				<h5>Use Default Dictionary :</h5>
				<div class="btn-group btn-group-toggle" data-toggle="buttons">
					<label class="btn btn-secondary active"> 
						<input type="radio" name="useDefdict" id="useDefdictYes" checked>Yes
					</label> 
					<label class="btn btn-secondary"> 
						<input type="radio" name="useDefdict" id="useDefdictNo"> No
					</label>
				</div>
			</div>
			<!-- blank count -->
			<br>

			<!-- File-upLoad -->
			
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
			<h5>${explain }</h5>
			<input type="hidden" name="checkFile" id="checkFile" value="no" />
			
		</div>

		<br>
		<br>


		<!-- output -->
		<div class="col-sm-12 row">
			<h3>Output Excel File</h3>
			<!-- Need to ajax -->
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
	<script src="/js/index.js"></script>
</body>
</html>


