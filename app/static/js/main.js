function checkNewJobs() {
    fetch("/jobs/check_new")
        .then(res => res.json())
        .then(data => {
            const icon = document.getElementById("jobNotify");

            if (data.new > 0) {
                icon.style.display = "inline-block";
                icon.innerText = data.new;
            } else {
                icon.style.display = "none";
            }
        });
}

setInterval(checkNewJobs, 30000); // 30 seconds
checkNewJobs();
