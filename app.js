let jobModal = document.getElementById("job-modal");
let researchModal = document.getElementById("research-modal");
let jobBtn = document.getElementById("job-btn");
let researchBtn = document.getElementById("research-btn");

jobBtn.onclick = function() {
    jobModal.style.display = "block";
}

researchBtn.onclick = function() {
    researchModal.style.display = "block";
}

var closeBtns = document.getElementsByClassName("close");
console.log(closeBtns);

closeBtns[0].onclick = function() {
    jobModal.style.display = "none";
}

closeBtns[1].onclick = function() {
    researchModal.style.display = "none";
}


// When the user clicks outside the modal box, close it
window.onclick = function(event) {
    if (event.target == jobModal) {
        jobModal.style.display = "none";
    } else if (event.target == researchModal) {
        researchModal.style.display = "none";
    }
}

