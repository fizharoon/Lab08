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

// function updateStudent() {
//     var studentName = document.getElementById("studentNameUp").value;
//     var studentGrade = document.getElementById("studentGradeUp").value;
//     document.getElementById("studentNameUp").value = "";
//     document.getElementById("studentGradeUp").value = "";
//     // var xhttp = new XMLHttpRequest();
//     var newUpUrl = url + "/" + studentName;
//     xhttp.open("PUT", newUpUrl);
//     xhttp.setRequestHeader("Content-Type", "application/json");
//     const body = {"name": studentName, "grade": studentGrade};
//     xhttp.onload = function() {}
//     xhttp.send(JSON.stringify(body));
//}

function updateGrades(grade, student_id) {
    // console.log('this is grade: ', grade, studentId)
    course_id = document.getElementById("course_id").innerText
    // student_id = document.getElementById("student_id").innerText
    console.log(course_id, student_id, grade);
    newUrl = url + '/updategrade';
    xhttp.open("PUT", newUrl);
    xhttp.onload = function(){
      
    }

    // console.log(document.)
    xhttp.setRequestHeader("Content-Type", "application/json");
    const body = {"student_id": student_id, "course_id": course_id, "grade": grade};
    xhttp.send(JSON.stringify(body));

}