$(document).ready(function() {
	
	// File Upload Listener Function
	// if input other files(ex. txt..), can't use Convert btn
	$("#fileInput").on('change',function() {

		let ext = $(this).val().split('.').pop().toLowerCase();
		$("#fileInputLabel").text($("#fileInput").val().split('\\').pop());

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
			$("#outputDiv").hide();
			$("#errorDiv").hide();
			$("#loadBar").show();
			// Prevent Repetitively Click
			$("#checkFile").val("no");
			fileUpload();
			
		} 
	});
	
	
	// file Upload
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
				console.log("success_upload_logs");
				// if success -> socket(java to python)
				conveySocket(res.path);
				
			},
			error : function(json) {
				var res = JSON.parse(json)
				console.log(res.result);
				console.log("error_upload_logs");
				$("#loadBar").hide();
				$("#errorDiv").show();
			}

		});
	};
	
	// connect python TCP/IP Socket Server
	function conveySocket(path) {
		let isUse = false;
		let modelName = 'konlpy';
		if($("input[name=useDefdict]:checked").attr('id') == "useDefdictYes") {
			isUse = true;
		}
		if($("input[name=useModel]:checked").attr('id') == "useModelSP") {
			modelName = 'self_product'
		}
		
		var data = {
				"type" : "predict",
				"isUse": isUse,
				"path" : path,
				"model": modelName
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
			success     : function(json) {
				if(json.status) {
					$("#loadBar").hide();
					$("#outputName").val(json.output_path);
					console.log("success_convey_logs");
					$("#outputDiv").show();					
				} else {
					console.log("fail_python_logs");
					$("#loadBar").hide();
					$("#errorDiv").show();
				}
				
			},
			error       : function(json) {
				$("#loadBar").hide();
				console.log("fail_convey_logs");
				$("#errorDiv").show();
				
			}
		});
	}
	
	

})