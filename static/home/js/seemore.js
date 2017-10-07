var status="less";
function myFunction() {
    if (status == "less") {
        document.getElementById("see").style.height="180px";
        document.getElementById("button").innerHTML = "See more...";
        status = "more";
    } else if (status == "more") {
        document.getElementById("see").style.height="100%";
        document.getElementById("button").innerHTML = "See Less..";
        status = "less"
    }
}