$(document).ready(function() {
	
	// File Upload Listener Function
	$("#fileInput").on('change',function() {

				let ext = $(this).val().split('.').pop().toLowerCase();
				$("#fileInputLabel").text($("#fileInput").val())

				if ($.inArray(ext, [ 'xlsx', 'xls' ]) == -1) {
					$("#fileInputMsg").html("<span class='text-danger'>파일타입을 확인해주세요</span>");
					$("#checkFile").val("no");
				} else {
					$("#fileInputMsg").html("<span class='text-success'>사용할 수 있습니다.</span>");
					$("#checkFile").val("yes");
				}

			});

	// Upload & Convert Button event(before check file)
	$("#convert").click(function(event) {
		
		event.preventDefault();
		
		if ($("#checkFile").val() == "yes") {
			fileUpload();
			//conveySocket('upload/input/template.xlsx');

		} else {
			

		}
	})
	
	function fileUpload() {
		var form = $("#uploadForm")[0];
		var data = new FormData(form);
		
		$.ajax({
			type        : "post",
			enctype     : "multipart/form-data",
			url         : "/fileupload.do",
			data        : data,
			processData : false,
			contentType : false,
			dataType    : 'text',
			cache       : false,
			success     : function(json) {
				var res = JSON.parse(json)
				console.log(res.result);
				console.log(res.path);
				console.log("success_upload_logs");
				// if success -> socket(java to python)
				conveySocket(res.path);
				
			},
			error : function(json) {
				var res = JSON.parse(json)
				console.log(res.result);
				console.log("error_upload_logs");
			}

		});
	}
	
	function conveySocket(path) {
		let isUse = false;
		if($("input[name=useDefdict]:checked").attr('id') == "useDefdictYes") {
			isUse = true;
		}
		
		var data = {
				"type" : "predict",
				"isUse": isUse,
				"path" : path,
				"model": "konlpy"
		}
		
		$.ajax({
			type        : "post",
			enctype     : "multipart/form-data",
			url         : "/conveySocket.do",
			data        : JSON.stringify(data),
			datatype    : "text",
			processData : false,
			contentType : "application/json",
			cache       : false,
			success     : function(res) {
				console.log(res);
				console.log("success_convey_logs");
			},
			error       : function(res) {
				console.log(res);
				console.log("fail_convey_logs");
				
			}
		});
	}
	

})