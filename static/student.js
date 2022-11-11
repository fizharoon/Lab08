const xhttp = new XMLHttpRequest();
const method = "GET";  // Could be GET, POST, PUT, DELETE, etc.
const url = "http://127.0.0.1:5000"; 
const async = true;   // asynchronous (true) or synchronous (false) – don’t use synchronous


function openStudentCourses(evt, cityName) {
    var i, tabcontent, tablinks;
    tabcontent = document.getElementsByClassName("tabcontent");
    for (i = 0; i < tabcontent.length; i++) {
      tabcontent[i].style.display = "none";
    }
    tablinks = document.getElementsByClassName("tablinks");
    for (i = 0; i < tablinks.length; i++) {
      tablinks[i].className = tablinks[i].className.replace(" active", "");
    }
    document.getElementById(cityName).style.display = "block";
    evt.currentTarget.className += " active";
  
    getStudentCourses();
}

function openAllCourses(evt, cityName) {
    var i, tabcontent, tablinks;
    tabcontent = document.getElementsByClassName("tabcontent");
    for (i = 0; i < tabcontent.length; i++) {
      tabcontent[i].style.display = "none";
    }
    tablinks = document.getElementsByClassName("tablinks");
    for (i = 0; i < tablinks.length; i++) {
      tablinks[i].className = tablinks[i].className.replace(" active", "");
    }
    document.getElementById(cityName).style.display = "block";
    evt.currentTarget.className += " active";
  
    getAllCourses();
}

function enroll(course_id) {
    var newUrl = url + "/addstudent";
    var body = {'course_id': course_id};
    xhttp.open("POST", newUrl);
    xhttp.setRequestHeader("Content-Type", "application/json");
    xhttp.onload = function() {
        // console.log(this.response);
        getAllCourses();
    }
    xhttp.send(JSON.stringify(body));
}

function drop(course_id) {
    var newUrl = url + "/dropcourse";
    var body = {'course_id': course_id};
    xhttp.open("DELETE", newUrl);
    xhttp.setRequestHeader("Content-Type", "application/json");
    xhttp.onload = function() {
        // console.log(this.response);
        getAllCourses();
    }
    xhttp.send(JSON.stringify(body));
}

function getStudentCourses() {
    var newUrl = url + "/getstudentcourses";
    xhttp.open("GET", newUrl);
    xhttp.onload = function() {
        data = JSON.parse(this.response);
        // console.log(data);
        var result = "";
        for (i in data){
            result += "<tr>";
            for(j in data[i]){
                result += "<td>" + data[i][j] + "</td>";
            }   
            // result += "<td>"+ data[i][data[i].length-2] + '/' + data[i][data[i].length-1] + "</td>"
            result += "</tr>"

        }
        document.getElementById("studentCourses").innerHTML = result;
    }
    xhttp.send();
}

function getAllCourses() {
    var newUrl = url + "/getallcourses";
    xhttp.open("GET", newUrl);
    xhttp.onload = function() {
        data = JSON.parse(this.response);
        // console.log(data);
        var result = "";
        for (i in data){
            result += "<tr>";
            for(j=0;j<data[i].length-1;j++){
                result += "<td>"+data[i][j] + "</td>";
            }   
            if (data[i][data[i].length-1] == 'enrolled') {
                result += "<td><button onClick=\"drop(" + i +")\">Drop Course</button></td>"
            } else {
                result += "<td><button onClick=\"enroll(" + i + ")\">Add Course</button></td>"
            }
            

            result += "</tr>"

        }
        document.getElementById("allCourses").innerHTML = result;
    }
    xhttp.send();
}