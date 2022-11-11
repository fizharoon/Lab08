const xhttp = new XMLHttpRequest();
const method = "GET";  // Could be GET, POST, PUT, DELETE, etc.
const url = "http://127.0.0.1:5000"; 
const async = true;   // asynchronous (true) or synchronous (false) – don’t use synchronous

function getTeacherCourses() {
    var newUrl = url + "/getteachercourses";
    xhttp.open("GET", newUrl);
    xhttp.onload = function() {
        data = JSON.parse(this.response);
        // console.log(data);
        var result = "";
        for (i in data){
            
            result += "<tr>";
            result+="<a href=\"{{url_for('courses')}}\">" + data[0] + "</a>";
            for(j in data[i]){
                result += "<td>" + data[i][j] + "</td>";
            }   
            // result += "<td>"+ data[i][data[i].length-2] + '/' + data[i][data[i].length-1] + "</td>"
            result += "</tr>"

        }
        document.getElementById("teacherCourses").innerHTML = result;
    }
    xhttp.send();
}

//function getStudentGrades() {
//    var newUrl = url + '/getstudentgrades/<courseid>';
//    xhttp.open("GET", newUrl);
//    xhttp.onload = function() {
//        data = JSON.parse(this.response);
//        // console.log(data);
//        var result = "";
//        for (i in data){
//            result += "<tr>";
//            for(j=0;j<data[i].length-1;j++){
//                result += "<td>"+data[i][j] + "</td>";
//            }
//            if (data[i][data[i].length-1] == 'enrolled') {
//                result += "<td><button onClick=\"drop(" + i +")\">Drop Course</button></td>"
//            } else {
//                result += "<td><button onClick=\"enroll(" + i + ")\">Add Course</button></td>"
//            }
//
//
//            result += "</tr>"
//
//        }
//        document.getElementById("allCourses").innerHTML = result;
//    }
//    xhttp.send();
//}
