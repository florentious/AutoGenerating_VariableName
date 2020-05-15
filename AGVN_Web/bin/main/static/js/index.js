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

		} else {

		}
	})
	
	function fileUpload() {
		var form = $("#uploadForm")[0];
		var data = new FormData(form);
		
		console.log(form);
		console.log(data);
		
		$.ajax({
			type : "POST",
			enctype : "multipart/form-data",
			url : "/fileUpload.do",
			data : data,
			processData : false,
			contentType : false,
			// dataType : 'json',
			cache : false,
			success : function(result) {
				console.log("success");
				$('#uploadForm')[0].reset();
			},
			error : function(result) {
				console.log("fail");
			}

		})
	}

})